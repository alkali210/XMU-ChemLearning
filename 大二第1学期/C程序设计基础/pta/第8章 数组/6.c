#include <stdio.h> 

int main()
{int i, tree_num;
int b[19]={0,28,30,25,20,35,50,20,25,36,33,27,27,28,28,29,30,33,26};
 
    scanf("%d", &tree_num);
 
    for(i = 1; i < 19; i++) {
        if( tree_num <= b[i]) break;
        tree_num -= b[i];
    }

    printf("第%d位员工管理的第%d棵树\n", i, tree_num);

    return 0; 
}
