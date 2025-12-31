#include <stdio.h>
int main()
{ int a, b, c;
    scanf("%d%d%d", &a, &b, &c);
    if (a + b > c && a + c > b && b + c > a)
        printf("是三角形\n");
    else
        printf("不是三角形\n");
    return 0;
}
