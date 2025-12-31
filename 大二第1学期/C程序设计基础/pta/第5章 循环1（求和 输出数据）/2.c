#include <stdio.h>
int main()
{ int i, s = 1, m, n, sum = 0;
    scanf("%d", &n);
    for(m = 1; m <= n; m+=2) {
        sum += m * s;
        s = -s;
    }
    printf("%d\n", sum);
    return 0;
}
