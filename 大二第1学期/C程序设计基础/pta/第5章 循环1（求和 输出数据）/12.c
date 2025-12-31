#include<stdio.h>
int main()
{
int n,i,count = 0;
    scanf("%d",&n);
    for(i = 1; i < n; i++) 
        if(i % 5 == 0 || i % 7 == 0) {
            printf("%d ", i);
            count++;
            if( count % 8 == 0)
                printf("\n");
        }
	return 0;
}
