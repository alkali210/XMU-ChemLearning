#include<stdio.h>
#include<math.h>
int main()
{ int i = 0,a,b,sum = 0,t = 10;
	scanf("%d%d",&a,&b); /*返程车费和每日生活费*/
	while(sum < (a + i * b)){
		sum+=t;
		i++;
        t *= 2;
	}
	printf("%d",i);
	return 0;
 }
