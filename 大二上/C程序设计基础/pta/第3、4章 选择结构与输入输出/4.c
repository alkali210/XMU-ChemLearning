#include <stdio.h>
int main()
{ int hour, minute;
    scanf("%d:%d", &hour, &minute);
    if (6 <= hour && hour <= 11)
        printf("上午好\n");
    else if (12 <= hour && hour <= 17)
        printf("下午好\n");
    else if (18 <= hour && hour <= 24 || 0 <= hour && hour <= 5)
        printf("晚上好\n");
    return 0;
}
