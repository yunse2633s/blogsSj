#include <windows.h>
#include <time.h>
#include <stdio.h>

#define BEFORE 1
#define PLAYING 2
#define AFTER 3
#define UNIT 20　　//绘图的最小单元

typedef struct node {
    COORD cor;
    struct node *next;
}node;

COORD food;
node *head;
char len = 1;
COORD snake[100];
FILE *mem;
errno_t err;

int state = BEFORE;
int option = 1;
int old_dir = VK_RIGHT;
int cur_dir = VK_RIGHT;

RECT Client = { 200,100,1000,600 };　　//用户区大小
HBITMAP bg;
HDC hdc, hMemdc;
HFONT hFont;

void draw_options();
void choose(int,HWND);
int no_reverse();
void draw_game(void);
void move_snake();
void init_game();
int cor_cmp(COORD pt1, COORD pt2);
COORD generate_food(void);
int isalive(void);
void save();
void load();
void free_node(node *h);

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE, PWSTR pCmdLine, int nCmdShow)
{
    const wchar_t CLASS_NAME[] = L"Game Window Class";

    WNDCLASS wc = {};
    
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;

    RegisterClass(&wc);

    AdjustWindowRect(&Client, WS_OVERLAPPED, FALSE);　//根据用户区大小生成窗口大小

    HWND hwnd = CreateWindowEx(
        0,
        CLASS_NAME,
        L"Greedy Snake",
        WS_OVERLAPPEDWINDOW,
        Client.left, Client.top, Client.right-Client.left, Client.bottom - Client.top,
        NULL,
        NULL,
        hInstance,
        NULL
    );

    if (hwnd == NULL)
    {
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);

    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    switch (uMsg)
    {
    case WM_CREATE:
        hFont = CreateFont(40, 20, 0, 0, FW_BOLD, FALSE, FALSE, FALSE, DEFAULT_CHARSET, OUT_OUTLINE_PRECIS,
            CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY, VARIABLE_PITCH, TEXT("Impact"));　　//创造字体
        return 0;
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    case WM_PAINT:
    {
        PAINTSTRUCT ps;
        hdc = BeginPaint(hwnd, &ps);
        bg = (HBITMAP)LoadImage(NULL, _T("bg.bmp"), IMAGE_BITMAP, 0, 0, LR_LOADFROMFILE);　　//加载背景图
        hMemdc = CreateCompatibleDC(hdc);
        SelectObject(hMemdc, bg);
        BitBlt(hdc, 0, 0, Client.right, Client.bottom, hMemdc, 0, 0, SRCCOPY);　　//贴背景图
        SetBkMode(hdc, TRANSPARENT);　　//使文字透明

        if (state == BEFORE)
            draw_options();
        if (state == PLAYING)
            draw_game();

        EndPaint(hwnd, &ps);
    }
    return 0;
    case WM_KEYDOWN:
    {
        if (state == BEFORE)
            choose(wParam,hwnd);
        if (state == PLAYING) {
            if (wParam == VK_ESCAPE) {　　//退出保存
                save();
                free_node(head);
                DestroyWindow(hwnd);
            }
            if (wParam != VK_RETURN) {　　//这里不判断的话，初始方向会被读为VK_RETURN
                old_dir = cur_dir;
                cur_dir = wParam;
            }
        }
    }
    return 0; 
    case WM_TIMER:
    {
        if (wParam == 1) {
            move_snake();
            InvalidateRect(hwnd, NULL, TRUE);
            if (!isalive()) {
                free_node(head);
                DestroyWindow(hwnd);
            }
        }
    }
    return 0;
    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

void draw_options()
{
    SelectObject(hdc, hFont);
    SetTextColor(hdc, RGB(139, 0, 0));
    TextOut(hdc, 320, 180, _TEXT("新的游戏"), 4);
    TextOut(hdc, 320, 240, _TEXT("继续游戏"), 4);
    if (option == 1)
        TextOut(hdc, 280, 180, _TEXT("->"), 2);
    else
        TextOut(hdc, 280, 240, _TEXT("->"), 2);
}

void choose(int key,HWND h)
{
    if (key == VK_UP&&option > 1)
        option--;
    if (key == VK_DOWN&&option < 2)
        option++;
    if (key == VK_RETURN) {
        DeleteObject(hFont);　　//删除创造的字体
        state = PLAYING;
        if (option == 1)
            init_game();
        else
            load();
        SetTimer(h, 1, 100, NULL);
    }
        InvalidateRect(h, NULL, TRUE);
}

void draw_game(void)
{
    node *p = NULL;
    SelectObject(hdc, (HBRUSH)GetStockObject(GRAY_BRUSH));
    for (p = head; p != NULL; p = p->next)
        Rectangle(hdc, (p->cor.X)*UNIT, (p->cor.Y)*UNIT, (p->cor.X + 1)*UNIT, (p->cor.Y + 1)*UNIT);
    Ellipse(hdc, food.X*UNIT, food.Y*UNIT, (food.X + 1)*UNIT, (food.Y + 1)*UNIT);
}

void init_game()
{
    head = (node *)malloc(sizeof(node));
    head->cor.X = 3;
    head->cor.Y = 8;
    head->next = NULL;
    food = { 18,12 };
}

void move_snake()
{
    no_reverse();
    node *p, *t = NULL;
    node *newh = NULL;
    newh = (node *)malloc(sizeof(node));
    newh->cor = head->cor;
    newh->next = head;
    head = newh;
    int grow = 0;
    switch (cur_dir) {
    case VK_UP:
        head->cor.Y--;
        break;
    case VK_DOWN:
        head->cor.Y++;
        break;
    case VK_LEFT:
        head->cor.X--;
        break;
    case VK_RIGHT:
        head->cor.X++;
        break;
    }
    if (cor_cmp(head->cor, food)) {
        grow = 1;
        food = generate_food();
    }
    if (grow) {
        len++;
    }
    else {
        for (p = head; p->next->next != NULL; p = p->next)
            ;
        t = p->next;
        p->next = NULL;
        free(t);
    }
}

int no_reverse()
{
    int state;
    state = cur_dir - old_dir;
    if ((state == 2 || state == -2)&&len!=1)
        cur_dir = old_dir;
    return cur_dir;
}

int cor_cmp(COORD pt1, COORD pt2)
{
    return (pt1.X == pt2.X&&pt1.Y == pt2.Y);
}

COORD generate_food(void)
{
    COORD food_;
    node *p = NULL;
    int in_snake = 0;
    srand((unsigned int)time(NULL));
    do {
        food_.X = rand() % 40;
        food_.Y = rand() % 25;
        for (p = head; p != NULL; p = p->next)
            if (cor_cmp(food_, p->cor))
                in_snake = 1;
    } while (food_.X < 0 || food_.X > 38 || food_.Y < 0 || food_.Y > 22 || in_snake);
    return food_;
}

int isalive(void)
{
    int self_eat = 0;
    node *p = NULL;
    for (p = head->next; p != NULL; p = p->next)
        if (cor_cmp(p->cor, head->cor))
            self_eat = 1;
    return (head->cor.X < 0 || head->cor.X > 39 || head->cor.Y < 0 || head->cor.Y > 24 || self_eat) ? 0 : 1;
}
void save()
{
    node *p = NULL;
    if ((err = fopen_s(&mem, "memory.txt", "w+")) == NULL) {
        fwrite(&len, sizeof(len), 1, mem);
        fwrite(&cur_dir, sizeof(cur_dir), 1, mem);
        fwrite(&food, sizeof(food), 1, mem);
        for (p = head; p != NULL; p = p->next)
            fwrite(&(p->cor), sizeof(p->cor), 1, mem);
        fclose(mem);
    }
}
void load()
{
    node *p, *q;
    int i, j;
    if ((err = fopen_s(&mem, "memory.txt", "r")) == NULL) {
        fread(&len, sizeof(len), 1, mem);
        fread(&cur_dir, sizeof(cur_dir), 1, mem);
        fread(&food, sizeof(food), 1, mem);
        fread(snake, sizeof(COORD), len, mem);
        fclose(mem);
    }
    p = head = (node *)malloc(sizeof(node));
    p->cor = snake[0];
    for (i = 1; i < len; i++) {
        q = (node *)malloc(sizeof(node));
        q->cor = snake[i];
        p->next = q;
        p = q;
    }
    p->next = NULL;
}

void free_node(node *h)
{
    node *p, *q;
    for (p = h; p != NULL; p = q) {
        q = p->next;
        free(p);
    }
}