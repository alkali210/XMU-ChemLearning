#include<stdio.h>
int main()
{
	int x,trees,j,n=0,sum=0;
	scanf("%d%d",&trees,&x);
    for(j=x;sum<trees;j*=3 ) {
    	sum+=j;
    	n++;
	}
	printf("%d",n);
	return 0;
}
