#include <stdio.h>
#include <stdlib.h>
 
int main()
{
 
    enum day
    {
        saturday,
        sunday,
        monday,
        tuesday,
        wednesday,
        thursday,
        friday
    } workday;
 
    int a = 1;
    enum day weekend; //weekend=内存位置
    // weekend = ( enum day ) a;  //类型转换
    //weekend = a; //错误
    // weekend=monday; //weekend=2
    printf("weekend:%d, workday: %d",weekend, &workday); // %d 与 %p 的区别进制不一样
    return 0;
}