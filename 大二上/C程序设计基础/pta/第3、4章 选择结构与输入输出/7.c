#include <stdio.h>
int main()
{ int n;
    scanf("%d", &n);
    if(0 <= n && n <= 9)
        printf("1\n");
    else if(10 <= n && n <= 99)
        printf("2\n");
     else if(100 <= n && n <= 999)
        printf("3\n");
     else if(1000 <= n && n <= 9999)
        printf("4\n");
    return 0;
}
