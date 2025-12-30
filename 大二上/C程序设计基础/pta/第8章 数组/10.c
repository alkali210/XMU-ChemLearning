#include <stdio.h>

int main()
{ int i, m, n, max, vote, a[11] = {0};

    scanf("%d", &n);
    scanf("%d", &m);
    for(i = 0; i < m; i++) {
    	scanf("%d", &vote);
    	a[vote]++;
	}
	max = a[1];
	for(i = 2; i <= n; i++)
	    if(max < a[i]) max = a[i];
	
	for(i = 1; i <= n; i++)
	    if( a[i] == max) printf("%d %d\n", i, a[i]);
	
	return 0;
}
