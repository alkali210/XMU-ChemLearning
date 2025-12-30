#include <stdio.h>
int wanshu(int x)
{int i, sum = 0;
    for(i = 1; i < x; i++)
        if(x % i == 0) sum += i;
    return sum == x;
}

int main()
{int i, n;
    scanf("%d", &n);
    for(i=1; i<=n; i++) 
        if(wanshu(i)==1) 
            printf("%d\n", i);
    return 0;
}
