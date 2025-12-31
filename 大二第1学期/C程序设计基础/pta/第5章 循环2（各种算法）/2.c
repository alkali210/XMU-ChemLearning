#include<stdio.h>
#include<math.h>
int main()
{
    float real,vict,x;
    int i=1,k;
    scanf("%f",&real);
    scanf("%f",&vict);
    for(k=2;k<=8;k++) {
      scanf("%f",&x);
      if(fabs(x-real)<fabs(vict-real)) {
      	vict=x;
        i=k;
      }
    }
    printf("%d\n",i);
    printf("%.1f",vict);
    return 0;
}
