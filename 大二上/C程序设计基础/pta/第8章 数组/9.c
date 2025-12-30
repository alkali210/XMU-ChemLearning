#include <stdio.h> 
#include <math.h>
int main()
{int i, min, money;
int a[19]={0,18,38,108,48,68,35,72,66,120,180,65,75,85,56,66,92,15,68};
 
    scanf("%d", &money);
    min = abs(money - a[1]);
    for(i = 2; i < 19; i++) 
        if(abs(money - a[i]) < min) min = abs(money - a[i]);
 
    for(i = 1; i < 19; i++) 
        if(abs(money - a[i]) == min) 
            printf("该客户可推荐%d号套餐，%d元\n", i, a[i]);

    return 0; 
}
