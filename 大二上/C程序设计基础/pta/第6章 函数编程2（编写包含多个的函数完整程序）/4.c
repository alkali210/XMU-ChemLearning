#include <stdio.h>

long fact(int n)
{long f = 1;
 int i;
 for(i = 1; i <= n; i++) f *= i;
 return f;    
}

int main()
{int n, a, b, c;
    scanf("%d", &n);
    a = n % 10;
    b = n / 10 % 10;
    c = n / 100 % 10;
    if(n == fact(a) + fact(b) + fact(c))
        printf("是阶乘和数");
    else
        printf("不是阶乘和数");
    return 0;
}
