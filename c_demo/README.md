# 使用 MinGW 安装 c环境

# C 下实操

1, 将.c文件转未 .exe
gcc hello.c -o hello //将hello.c文件输出未hello可执行文件

2, printf中不能使用单引号
printf('') //更改为 printf("")

3, 定义变量值的时候不能使用双引号;
 exe :char c=""; //程序报错
 int c=2; 对
 char c='a'; 错
 char c; c="a"; 错

 char c; c='xc'; //def_conf.c:7:4: warning: multi-character character constant [-Wmultichar]

# 图形库的安装
1, ege + Mingw 的配合是c下拥有图形库 【该库发展时间不足。改选OpenGL】
2, 安装 openGL,

