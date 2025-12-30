#include <stdio.h> 

int main()
{int i, j, elem, num;
int a[10] = {1,3,5,7,9,11,13,15,17,19};
 
    scanf("%d", &num);
    for(i = 0; i < num; i++) {
        scanf("%d", &elem);
        for(j = 0; j < 10; j++)
            if(elem == a[j]) printf("%d ", elem);
    }

    return 0; 
}
