#include <stdio.h>
int main()
{    
   int n,i,ge,bai ,count = 0; 
   scanf("%d",&n);
   for(i = 100 ; i <= n ; i++) {     
      ge=i%10;                    
      bai=i/100%10;                  
      if(ge+bai==9) {
           printf("%7d",i); 
           count++;  
           if(count%8==0) 
              printf("\n"); 
      }
   }
   return 0;
} 
