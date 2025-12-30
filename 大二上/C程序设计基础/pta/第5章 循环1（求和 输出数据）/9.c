#include <stdio.h>
#include <math.h>
int main()
{
	int k=1,x;
	double s=300;
	scanf("%d",&x);  //x为要超过的米数
	while(s<=x)
	{
		s=(1+1.0/8)*s;
		k++;
	 } 
	 printf("第%d天",k);
	return 0;
}
