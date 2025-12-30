#include<stdio.h>
int main()
{
	int n,i,count = 0;
	scanf("%d",&n);
	for(i = 1; i < n; i++) 
        if(i % 3 ==2 && i % 5 == 3 && i % 7 == 2) {
            printf("%5d", i);
            count++;
            if( count % 5 == 0)
                printf("\n");
        }
	return 0;
}
