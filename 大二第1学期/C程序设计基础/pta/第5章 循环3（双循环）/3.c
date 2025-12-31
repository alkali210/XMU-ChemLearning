#include <stdio.h>
/*双循环的方法*/
int main() 
{ int i, j, n, sum = 0, temp;
    scanf("%d", &n);
    for(i = 1; i <= n; i++){
        temp = 1;
        for(j = 1; j <= i; j++)
            temp *= j;
        sum += temp;
    }
    printf("%d",sum);
    return 0;
}


/*单循环的方法: i! = (i-1)! * i
int main() 
{ int i, n,sum=0,temp=1;
    scanf("%d",&n);
    for( i=1; i<=n; i++){
        temp*=i;
        sum+=temp;
    }
    printf("%d",sum);
    return 0;
}
*/