#include <stdio.h>
#include <string.h> 
int main()
{
   FILE *fp = NULL;
 
   fp = fopen("g:/work/c/201901/fs.txt", "a+"); // w+ a+
   printf("plear intpu string");
   char str[20];
   // scanf("%s", &str);
   gets(str); //读取一行到所指向的缓冲区，直到一个终止符或 EOF。
   // fprintf(fp, "This is testing for fprintf...\n");
   // fputs("This is testing for fputs...\n", fp); 
   // fputs(s,fp) 把字符串写入到 fp 所指向的输出流中
   // fprintf 写把一个字符串写入到文件中
   printf("input content: %s", str); //如何避免空格
   
   // fputs(str, fp);strcat(str,"\n")
   strcat(str,"\n"); // 使用字符串拼接，增加一个换行符
   fputs(str, fp);
   fclose(fp);
}