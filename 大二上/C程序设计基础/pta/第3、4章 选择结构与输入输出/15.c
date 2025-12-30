#include<stdio.h>
int main( )
{
    int n, a1, a2, a3;

        scanf("%d", &n);
        a1 = n % 10;
        a2 = n /10 %10;
        a3 = n /100 % 10;

        if (a1 == a2 && a3 != 0)      
              printf("符合条件\n");
        else 
              printf("不符合条件\n");
       return 0;
}
