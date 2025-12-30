#include <stdio.h>
int main()
{int count=0;
 char c;
   while((c = getchar()) != '.')
       if(c != ' ')
           count++;
       else 
           if(count!=0) {
	       printf("%d ",count);
	       count=0;
    	   }
    if (count != 0) printf("%d ", count);
    return 0;
}
