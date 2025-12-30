#include <stdio.h>
int main()
{ int n;
    scanf("%d", &n);
    if (n % 2 == 0)
        printf("该数是偶数\n");
    else
        printf("该数是奇数\n");
    return 0;
}
