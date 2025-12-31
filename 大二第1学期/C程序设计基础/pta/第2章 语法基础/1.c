#include <stdio.h>

#define PI 3.14159
int main() 
{  float r,c,area;
   scanf("%f",&r);
   c=2*PI*r;
   area=PI*r*r;
   printf("%.2f\n%.2f\n", c, area) ;
   return 0;
}
