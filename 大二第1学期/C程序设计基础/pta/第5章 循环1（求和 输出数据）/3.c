#include <stdio.h>
int main()
{
    int i,a,n;
    scanf("%d %d",&a,&n);
    int sum,temp=a;
    for(i=0;i<n;i++){
        sum+=temp;
        temp=temp*10+a;
    }
    printf("s = %d",sum);
    return 0;
}
