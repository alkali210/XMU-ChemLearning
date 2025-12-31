#include <stdio.h> 

int main()
{int i, day, num;
int b[13]={0,31,28,31,30,31,30,31,31,30,31,30,31};
 
    scanf("%d", &num);
    day = num;
    for(i = 1; i < 13; i++) {
        if(day <= b[i]) break;
        day -= b[i];
    }
    printf("第%d天是%d月%d日", num, i, day);

    return 0; 
}
