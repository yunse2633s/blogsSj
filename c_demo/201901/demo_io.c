#include <stdio.h>      // 执行 printf() 函数需要该库
int main()
{
	float f;
	printf("Enter a number:");  //显示引号中的内容
	scanf("%f", &f);
    printf("Value = %f", f); 
    return 0;
}