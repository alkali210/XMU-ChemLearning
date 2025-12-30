#include <stdio.h>
#include <math.h>

int main() 
{ int a, b, max;
   scanf("%d%d", &a, &b);
   max = (a + b + abs(a - b)) / 2;
   printf("%d\n", max);
   printf("%f\n", sqrt(max));
   return 0;
}
