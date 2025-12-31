#include <stdio.h>

int main()
{ int i, n = 10, max, pos, t, a[10];

    for(i = 0; i < n; i++) 
    	scanf("%d", &a[i]);
    	
	max = a[0]; pos = 0;
	for(i = 1; i < n; i++)
	    if(max < a[i]) {
	        max = a[i];
	        pos = i;
	    }
	    
	a[pos] = a[9];
	a[9] = max;
	
	for(i = 0; i < n; i++)
	    printf("%d ", a[i]);
	
	return 0;
}
