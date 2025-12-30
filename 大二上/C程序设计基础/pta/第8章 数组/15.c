#include <stdio.h>
int main()
{int a[100], b[201] = {0};
 int i, j, n, count = 0;
     scanf("%d", &n);
     for(i = 0; i < n; i++)
         scanf("%d", &a[i]);

     for(i = 0; i < n - 1; i++)
         for(j = i + 1; j < n; j++) 
             b[a[i] + a[j]] = 1;
      
     for(i = 0; i < n; i++) 
         if(b[a[i]] > 0) count++;
 
     printf("%d\n", count);
  
     return 0;
}

/*第二种答案
#include <stdio.h>
int main()
{int i, j, k, n, b[100], count = 0;
    scanf("%d", &n);
    for(i = 0; i < n; i++)
        scanf("%d", &b[i]);
    for(i = 0; i < n; i++) {
        for(j = 0; j < n - 1; j++) {
            if(j == i) continue;
            for(k = j + 1; k < n; k++) {
                if(k == i) continue;
                if(b[i] == b[j] + b[k]) break;
            }
            if(k < n) break;
        }
        if(j < n - 1) count++;
    }
    printf("%d\n",count);
    return 0;
}
*/