#include <stdio.h>
 
int main()
{
   FILE *fp = NULL;
   char buff[255];
 
   fp = fopen("g:/work/c/201901/fs.txt", "r");

   // fscanf从文件中读取字符串，但是在遇到第一个空格字符时，它会停止读取
   fscanf(fp, "%s", buff);
   printf("1: %s\n", buff );
 
   fgets(buff, 255, (FILE*)fp);
   printf("2: %s\n", buff );
   
   fgets(buff, 255, (FILE*)fp);
   printf("3: %s\n", buff );

   fgets(buff, 255, (FILE*)fp);
   printf("4: %s\n", buff );

   // fp 的结束位置是否可以判断呢;
   // 
   fclose(fp);
 
}