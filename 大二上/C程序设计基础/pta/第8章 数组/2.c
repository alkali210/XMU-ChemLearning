#include <stdio.h> 

int main()
{int a[10] = {1, 4, -1, 8, 9, 4, 7, -1, 12, -1}; 
 int i, min;
 
    /*刚开始编程时，可以把下面的这条for语句注释掉，并把一个测试例子写在上面的数组a的初始化中，可以方便调试。
	  省得每次调试时都要输入一大串数据。等调试好了，再删除测试样例并恢复使用scanf。 */ 
    for (i = 0; i < 10; i++)   
        scanf("%d", &a[i]);
 
    min = a[0]; /*把a[0]作为当前最小值,以后若有更小的，则替换之*/
    for (i = 1; i < 10; i++)    
        if (a[i] < min ) min = a[i];
 
    printf("%d\n", min);
    for (i = 0; i < 10; i++)  
        if (a[i] == min) printf("%d  ", i);
 
    return 0; 
}
