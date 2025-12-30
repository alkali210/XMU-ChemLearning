#include <stdio.h>
#include <math.h>
int main()
{ float x, f;
    scanf("%f", &x);
    if(x <= -1) 
        f = 2 * x * x * x - 1;
    else if(x <= 0) //注意：x <= -1为假且x <= 0为真
        f = x * x;
    else if(x <= 1)//注意：x <= -1为假且x <= 0为假且x <= 1为真
        f = sqrt(x);
    else //注意：x <= -1为假且x <= 0为假且x <= 1为假
        f = 3 * x + 2;
    printf("%.2f\n", f);
    return 0;
}
