#include <stdio.h>
int main()
{int x;
	scanf("%d",&x);
    if(x < 0)
	  printf("error");
    else if(x <= 230)
	  printf("%.1f\n",x*0.54);
	else
	  printf("%.1f\n",230*0.54+(x-230)*0.84);
    
	return 0;
 }
