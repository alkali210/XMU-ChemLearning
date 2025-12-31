#include <stdio.h>
int main()
{ int i, j, n;
 char ch;
   scanf("%c", &ch);
   n = ch -'A';
   for(i = 1; i < 40; i++) putchar(' ');

   printf("A\n");
   for(i = 1; i < n; i++) {
       for(j = 1; j < 40 - i; j++) putchar(' ');
       putchar('A' + i);
       for(j = 1; j <= 2 * i - 1; j++) putchar(' ');
       printf("%c\n", 'A' + i);
   }
   for(i = 1; i <= 39 - n; i++) putchar(' ');
   for(i = 1; i <= 2 * n + 1; i++) putchar(ch);
   printf("\n");
 
   return 0;   
}