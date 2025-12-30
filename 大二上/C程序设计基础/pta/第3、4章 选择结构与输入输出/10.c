#include <stdio.h>
int main()
{ int n, ge, bai;
    scanf("%d", &n);
    ge = n % 10;
    bai = n / 100 % 10;
    if (ge == bai)
        printf("回文数\n");
    else
        printf("不是回文数\n");
    return 0;
}
