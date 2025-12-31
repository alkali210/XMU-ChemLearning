#include <stdio.h>
int main()
{ int i;
 float price, t, sum;
    scanf("%f", &price);
    sum = t = price * 0.02;
    for(i = 1; sum <= 10.0; i++) {
        t *= 1.5;
        sum += t;
    }
    printf("%d", i);
    return 0;
}
