#include <stdio.h>
#include <math.h>

int main() 
{ int n, a, b, c, d, e, sum;
   scanf("%d", &n);
   a = n % 10;
   b = n / 10 % 10;
   c = n / 100 % 10;
   d = n / 1000 % 10;
   e = n / 10000 % 10;
   sum = a + b + c + d + e;
   printf("%d(%d+%d+%d+%d+%d=%d)\n", sum, e, d, c, b, a, sum);
   return 0;
}
