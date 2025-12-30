#include <stdio.h>

int main()
{ int i, n, a[10] = {0};

    scanf("%d", &n);
    do {
    	a[n % 10]++;
    	n /= 10;
	} while(n != 0);
	
    for(i = 0; i <= 9; i++) 
        printf("数字%d出现:%d次\n", i, a[i]);
	
	return 0;
}
