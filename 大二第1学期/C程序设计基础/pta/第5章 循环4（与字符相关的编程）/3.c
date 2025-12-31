#include <stdio.h>
int main()
{ char ch;
  int count = 0;
    scanf("%c", &ch);
    if(ch == 'A' || ch == 'E' || ch == 'I' || ch == 'O' || ch == 'U') {
        count = 1;
        printf("ÊÇ\n");
    }
    else 
        printf("²»ÊÇ\n");
    while(ch != '.') {
        if(ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') count++;
        scanf("%c", &ch);
    }
    printf("%d", count);
    return 0;
}
