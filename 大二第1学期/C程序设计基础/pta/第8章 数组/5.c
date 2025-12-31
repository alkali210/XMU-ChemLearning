#include <stdio.h> 

int main()
{int i, j, sum;
 int a[4][4] = {{1,2,3,4},{5,7,8,1},{4,2,7,98},{71,8,5,65}}; 
 
    /*刚开始编程时，可以把下面的这条for语句注释掉，并把一个测试例子写在上面的数组a的初始化中，可以方便调试。
	  省得每次调试时都要输入一大串数据。等调试好了，再删除测试样例并恢复使用scanf。 */ 
    for(i = 0; i < 4; i++)   
        for(j = 0; j < 4; j++)
            scanf("%d", &a[i][j]);
    
    sum = 0;    
    for(i = 0; i < 4; i++) 
    	for(j = i + 1; j < 4; j++) 
    		sum += a[i][j];
    printf("%d\n", sum);

    return 0; 
}
