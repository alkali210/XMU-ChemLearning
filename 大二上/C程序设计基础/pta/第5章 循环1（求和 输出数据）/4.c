#include <stdio.h>
int main()
{ int i, s = 1, n = 1;
  double t =1, sum = 0;
    while(fabs(t)>=1e-6) {
        sum += t;
        s = -s;
        n += 2;
        t = (double)s/n;      
    }
    printf("%f\n", sum);
    return 0;
}
