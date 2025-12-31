#include <stdio.h>
int main() {
  int m, n, a;
    scanf("%d%d", &m, &n);
    a =(m > n )? m : n;
    while(a%m != 0 || a%n!= 0) a++;
    printf("%d", a);
    return 0;    
}
