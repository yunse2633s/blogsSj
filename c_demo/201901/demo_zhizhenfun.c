#include <stdio.h>
#include <time.h>
#include <stdlib.h> 
 
/* 要生成和返回随机数的函数 */
int * getRandom( )
{
   //这是一个返回指针的函数
   static int  r[10];
   int i;
 
   /* 设置种子 */
   srand( (unsigned)time( NULL ) );
   for ( i = 0; i < 10; ++i)
   {
      r[i] = rand();
      printf("%d - %d\n", i , r[i] );
   }
   printf("%p - %d -%d \n", &r, r[1], r); //r返回值为内存地址的十进制
   return r;
}
 
/* 要调用上面定义函数的主函数 */
int main ()
{
   /* 一个指向整数的指针 */
   int *p;
   int i;
 
   p = getRandom();
   printf("p %d, add %p\n", p, &p);
   for ( i = 0; i < 10; i++ )
   {
       // printf("*(p + [%d]) : %d\n", i, *(p + i) );
       // p指针变量的值是数组的第一个元素内存地址
       printf("*(p + [%d]) : %d\n", i, *p); 
   }
 
   return 0;
}