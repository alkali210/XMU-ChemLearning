#include <stdio.h>
#include <math.h>
int main() 
{ int i, j, n, lim, count=0;
    scanf("%d",&n);
    for(i = 2; i <= n; i++){
        lim = sqrt(i);
        for(j = 2; j <= lim; j++)
            if(i%j==0) break;
        if(j>lim)
            count+=1;
    } 
    printf("%d",count);
    return 0;
}
