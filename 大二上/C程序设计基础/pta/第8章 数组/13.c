#include <stdio.h>
int main()
{ int i = 0, num_flag = 0, odd_flag = 0;
 char ch, str[100];
     scanf("%s",str);/*注意，PTA对这道题的输入测试样例没有以'\n'结尾*/ 
     for(i = 0; str[i] != '\0'; i++) 
     	 if (i >= 5) {
     	     printf("非法输入\n"); 
             return 0;
         } else if (str[i]>='0' && str[i]<='9') {
             num_flag = 1;
             odd_flag = (str[i] - '0') % 2;
         } else if ( str[i] < 'A' || str[i] > 'Z') {
                 printf("非法输入\n"); 
                 return 0;
         }
     
     if(i <= 4 || num_flag == 0) {
         printf("非法输入\n"); return 0;
     }
     if(odd_flag == 1)
         printf("限行\n");
     else
         printf("通行\n");
     return 0;
}

/* 另一种答案：
#include <stdio.h>
int main()
{ int i = 0, too_long_flag=0, num_flag = 0, odd_flag = 0, other_char_flag = 0;
 char ch, str[100];
     scanf("%s",str);/*注意，PTA对这道题的输入测试样例没有以'\n'结尾*/ 
     for(i=0; str[i]!='\0'; i++) {
     	 if(i >= 5) {
     	 	too_long_flag = 1; break;
         }
         if(str[i]>='0' && str[i]<='9') {
             num_flag = 1;
             odd_flag = (str[i]-'0')%2;
         }
         else if( str[i]<'A' || str[i]>'Z') {
                 other_char_flag = 1; break;
         }
     }
     if(too_long_flag==1 || num_flag==0 || other_char_flag==1) {
         printf("非法输入\n"); return 0;
     }
     if(odd_flag==1)
         printf("限行\n");
     else
         printf("通行\n");
     return 0;
}
*/

/*问：为什么str[i]-'0'要-'0'呢？
答：因为str[i]里面存放的是字符的ascii码，比如字符'A'的ASCII码是65，字符‘0’的ascii码是48，字符‘2’的ascii码是50。str[i]-'0'就能算出它保存的字符和字符'0'差了多少。比如'2'-'0'就等于50-48，就等于2，就相当于把它保存的字符'2'变成整数2.
假设str[i]保存的是字符‘2’，而你直接使用它进行整数运算，那么str[i]+3 就是'2'+3,就是50+3，就是53，就是字符'5'的ascii码。
假设str[i]保存的是字符‘2’, 如果你要str[i]%2,那么就是50%2，为0。在这里恰好也可以，但是不是正道。如果'2'的ascii码万一是奇数，那就错了，当然'2'的ascii码是偶数，但考试的时候你也不记得它的ascii码是多少。
str[i]-'0'写成str[i]-48也行，但不是好的编程方法，因为别人不一定知道48是'0'的ascii码，还是写成str[i]-'0'比较好，再说万一你记错了'0'的ascii码呢。



*/

