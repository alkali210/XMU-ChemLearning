#include <stdio.h> 

int main()
{int a[20] = {0,80,70,90,100, 81,95,86,45,78,91}; 
 int i, sum = 0;
 float avg;
 
    /*刚开始编程时，可以把下面的这条for语句注释掉，并把一个测试例子写在上面的数组a的初始化中，可以方便调试。
	  省得每次调试时都要输入一大串数据。等调试好了，再删除测试样例并恢复使用scanf。 */ 
    for (i = 0; i < 20; i++)   
        scanf("%d", &a[i]);
 
    for (i = 0; i < 20; i++)   
        sum += a[i];	
    avg = sum / 20.0;
    printf("%.2f\n", avg);
 
    for (i = 0; i < 20; i++)   
        if (a[i] > avg ) printf("%d  ", a[i]);
 
    return 0; 
}
