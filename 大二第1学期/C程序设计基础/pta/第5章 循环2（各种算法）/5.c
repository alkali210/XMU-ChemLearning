#include <stdio.h>
int main() {
  int a,wei = 0;
    scanf("%d", &a);
    if(a < 0) a = -a;
    do {
        wei++;
        a /= 10;
    }while(a != 0);
    printf("%d", wei);
    return 0;
}
