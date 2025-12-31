#include <stdio.h>
int main()
{ int m, i, sum = 0;
    scanf("%d", &m);
    for(i = 1; i < m; i++)
        if(m%i == 0) 
            sum += i;
    if(m == sum)
        printf("是完数");
    else
        printf("不是完数");
    return 0;    
}
