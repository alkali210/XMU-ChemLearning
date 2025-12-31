float max, min;

float statistic(int num)
{int i;
 float score, sum = 0.0;
   scanf("%f", &score);
   sum = max = min = score;
   for (i = 1; i < num; i++) {
       scanf("%f", &score);
       if(score > max) max = score;
       if(score < min) min = score;
       sum += score;
   }
   return sum / num;
}

void print_m( )
{
    printf("最高分是%.2f\n", max);
    printf("最低分是%.2f\n", min);
}
