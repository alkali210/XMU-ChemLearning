#include <stdio.h> 

int main()
{int a[10]; 
 int i, n, m;  
    scanf("%d", &n);
    if (n < 0) n = -n;
 
    m = 0;
    do {
      a[m++] = n % 10;
      n /= 10;
    } while(n != 0);

    for (i = m - 1; i > 0; i--)  
        printf("%d,", a[i]);
    printf("%d", a[0]); 
 
    return 0; 
}
