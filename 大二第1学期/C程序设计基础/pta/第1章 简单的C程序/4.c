#include <stdio.h>

int main() 
{ int x, y, t;

    x=30;
    y=60; 
    t = x;
    x = y;
    y = t;
    printf("%d\n%d\n",x,y);                 

    return 0;
}
