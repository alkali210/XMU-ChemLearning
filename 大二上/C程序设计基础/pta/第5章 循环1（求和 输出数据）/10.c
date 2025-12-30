#include<stdio.h>
int main()
{ int i = 0, a,sum = 0;
	scanf("%d",&a); 
	while(a != -1){
		sum += a;
		i++;
        scanf("%d",&a);
	}
    printf("%d\n", i);
	printf("%f",(double)sum / i);
	return 0;
 }

