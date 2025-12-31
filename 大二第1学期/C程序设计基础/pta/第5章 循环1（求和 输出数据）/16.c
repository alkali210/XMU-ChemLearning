#include <stdio.h>
int main(){
    int i,n;
    scanf("%d",&n);
    for(i = 0; i < n; i++){
    	printf("%c ",'A' + i);
    	if((i+1)%8==0)
    	    printf("\n");
    }
    return 0;
}
