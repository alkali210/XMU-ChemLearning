#include <stdio.h>
int main()
{ int a, b, c;
    scanf("%d%d%d", &a, &b, &c);
    if(a*a+b*b==c*c || a*a+c*c==b*b || b*b+c*c==a*a)
        printf("是直角三角形\n");
    else
        printf("不是直角三角形\n");
    return 0;
}
