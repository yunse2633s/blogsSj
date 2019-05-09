#include <stdio.h>
 
int main ()
{
   int  var = 20;   /* 实际变量的声明 */
   int  *ip, *nip=NULL;        /* 指针变量的声明 */
	int  **pptr;
 
   ip = &var;  /* 在指针变量中存储 var 的地址 */
 	pptr=&ip;
   printf("Address of var variable: %p\n", &var  );
 
   /* 在指针变量中存储的地址 */
   printf("Address stored in ip variable: %p, it value %d\n", ip , *ip);
   /* 指向指针的指针 */ 
   printf("Address stored in pptr variable: %p, it value %d\n", pptr , *pptr);

 
   /* 使用指针变量访问值, 即使用指针变量中所存储的内存地址，访问内存中的所存数值 */
   printf("Value of *ip variable: %d\n", *ip );

   if(!nip){
   	printf("no %p\n", nip);
   }else{
	printf("yes");
   }
   int arr[]={10,2.23,'c',20}; // int将数组中的元素强转为整数,'a'可以，'abc'不可以
   printf("arr[1] %d" , arr[2]);
   printf("=====>\n");
   // （*p)[3] 与 *p[3] 的区别 ，从右向左读取; 
   int *pa[4];
   int i, (*pb)[4];

   // pa=&arr; //报错"error: assignment to expression with array type"
   // pb=&arr;
   printf("===2==>\n");
   for(i=0; i<4;i++){
      printf("===3==>\n");
      pa[i]=&arr[i];
      // pb[i]=&arr[i]; //报错"error: assignment to expression with array type"
      printf("pa[%d] %d %d\n",i, *pa[i], pa[i]);
   }
   // pb=arr; // 报错"warning: assignment from incompatible pointer type [-Wincompatible-pointer-types]"
   pb=&arr;
   printf("pb %d %d\n", pb, *pb);
   //
   return 0;
}