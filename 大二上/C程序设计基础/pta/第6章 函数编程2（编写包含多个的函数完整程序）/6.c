#include<stdio.h>
int main()
{
    int a,k;
    int fun(int a);
    scanf("%d",&a);
    k=fun(a);
    printf("%d的位数是%d\n",a,k);

}

int fun(int a)
{  int i=0;
   while(a)
   {
       a=a/10;
       i++;
   }
   return i;
}
