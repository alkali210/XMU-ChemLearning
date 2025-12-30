#include <stdio.h>
int main()
{int w, c;
 float price, cost;
	scanf("%d%d", &w, &c);
    if(w <= 1000) {
        if(c == 1)
            price = 4.5;
        else
            price = 7;
        if(w % 200 == 0)
            cost = w / 200 * price;
        else
            cost = (w / 200 + 1) * price;            
    }
    else {
        if(c == 1) {
            cost = 1000 / 200 * 4.5;
            price = 6;
        } else {
            cost = 1000 / 200 * 7;
            price = 8.5;
        }
        if((w - 1000) % 300 == 0)
            cost += (w - 1000) / 300 * price;
        else
            cost += ((w - 1000) / 300 + 1) * price;           
    }
    printf("%.2f\n", cost); 
	return 0;
 }
