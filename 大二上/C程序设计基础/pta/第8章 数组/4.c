#include <stdio.h> 

int main()
{int i, j, k, max;
 int score[11] = {0,80,70,90,100, 81,95,86,45,78,91}; 
 int no[11] = {0, 1, 2, 1, 2, 2, 1, 4, 4, 4, 4};
 
    /*刚开始编程时，可以把下面的这条for语句注释掉，并把一个测试例子写在上面的数组no的初始化中，可以方便调试。
	  省得每次调试时都要输入一大串数据。等调试好了，再删除测试样例并恢复使用scanf。 */ 
    for(i=1;i<11;i++)   
        scanf("%d",&no[i]);
        
    for(i=1;i<=4;i++) {
    	max = -1; k = -1;
    	for(j=1;j<11;j++) 
    		if(no[j]==i && score[j]>max) {
    			max = score[j]; 
				k = j;
			}
    	if( k > 0 )  //说明有人选中该课
		    printf("%d号课程录取第%d位学生%d分\n", i, k, max);
		else 
		    printf("%d号课程无人报\n", i);
	}
	
    return 0; 
}
