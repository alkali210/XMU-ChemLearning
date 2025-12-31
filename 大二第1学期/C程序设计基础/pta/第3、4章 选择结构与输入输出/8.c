#include <stdio.h>
int main()
{ int max, a, b, c, d;
    scanf("%d%d%d%d", &a, &b, &c, &d);
    max = a;
    if(max <= b) max = b;
    if(max <= c) max = c;
    if(max <= d) max = d;
    printf("%d\n", max);
    return 0;
}
