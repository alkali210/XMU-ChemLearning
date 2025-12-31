#include <stdio.h>
#include <math.h>
int main() {
  int p, q, a, b,  m;
    scanf("%d%d",&p, &q);
    m = sqrt(q);
    for(a=1; a<=m; a++) 
        if(q % a == 0) {
            b = q / a;
            if(a + b == p) {
                printf("(x+%d)(x+%d)", a, b);
                return 0;
            }
        }
    printf("无分解式");
    return 0;
}
