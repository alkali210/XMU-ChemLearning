#include <stdio.h>
int main()
{ int man, woman, child;
    for(man = 1; man <= 50/3; man++)
        for(woman = 1; woman <= 50/2; woman++) {
            child = 30 - man - woman;
            if(man*3+woman*2+child==50)
                printf("man=%d,woman=%d,child=%d\n", man, woman, child);
        }
    return 0;
}
