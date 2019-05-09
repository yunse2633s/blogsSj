#include <stdio.h>

#define WID 5

int main(){
	char c;
	c='x';
	const int LEN=3;
	// c='cc';
	// printf("music",c);
	printf("music , %d",c); 
	int area=WID*LEN;
	//int area; area = WID*LEN;
	printf("changliang: %d", area);
	//c='a', out:music,97
	//c='\a', out:music,7

	/*
		return 0;
	 */
}