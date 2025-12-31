#include <stdio.h>
int fun2(int x, int y)
{int k;
    k = (x > y) ? x : y;
    while(k % x != 0 || k % y != 0) k++;
    return k;
}

int main()
{int m, n;
    scanf("%d%d", &m, &n);
    printf("%d\n", fun2(m, n));
    return 0;
}
