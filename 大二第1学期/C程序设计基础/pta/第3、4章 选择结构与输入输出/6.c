#include <stdio.h>
int main()
{ int hour, minute;
    scanf("%d:%d", &hour, &minute);
    if(0 <= hour && hour <= 11)
        printf("%d:%02dAM\n", hour, minute);
    else if(12 <= hour && hour <= 23)
        printf("%d:%02dPM\n", hour - 12, minute);
    return 0;
}
