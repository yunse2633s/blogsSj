#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct LNode
{
    int data;
    struct LNode *next;
}L;

L *creat_node(int data);
void print_list(L *pH);
void tail_insert(L *pH,L *new);

int main()
{
    int i,n,j;
    L *head=creat_node(0);
    printf("��������Ҫ�����ڵ�ĸ�����");
    scanf("%d",&n);
    for(i=1;i<=n;i++)
    {
        printf("��%d���ڵ�����ݣ�",i);
        scanf("%d",&j);
        tail_insert(head,creat_node(j));
    }
    print_list(head);
    return 0;
}

//�����ڵ�
L *creat_node(int data)
{
    L *p=malloc(sizeof(L));
    if(NULL==p)
    {
        printf("malloc error!\n");
        return NULL;
    }
    memset(p,0,sizeof(L));
    p->data=data;
    p->next=NULL;
    return p;
}

//β�巨
void tail_insert(L *pH,L *new)
{
    L *p=pH;
    while(NULL!=p->next)
    {
        p=p->next;
    }
    p->next=new;
}

//��ӡ����
void print_list(L *pH)
{
    L *p=pH;
    printf("***************************\n");
    printf("�ոմ���������\n");
    while(NULL!=p->next)
    {
        p=p->next;
        printf("data=%d\n",p->data);
    }
}