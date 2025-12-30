#include <stdio.h>

int fun1(int m,int n)
{ int k;
    k = (m < n) ? m : n;
    while(m % k != 0 || n % k != 0) k--;
    return k;    
}

int main()
{int m, n;
     scanf("%d%d", &m, &n);
     printf("%d", fun1(m, n));
     return 0;    
}
