#include <stdio.h>

int shushu(int m)
{int i, k;
 k = sqrt(m);
 for(i = 2; i <= k; i++) 
     if(m % i == 0) break;
 if(i > k)
     return 1;    
 else 
     return 0;
}

int main()
{int n, a;
    scanf("%d", &n);
    for(a = 100; a <= n; a++)
        if(shushu(a) == 1) printf("%d,", a);
    return 0;
}
