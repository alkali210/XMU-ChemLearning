void triangle(int n)
{ int i, j;
    for(i = 1; i <= n; i++) {
        for(j = 1; j <= 2 * i - 1; j++)
            printf("*");
        printf("\n");
    }
}

void rectangle(int n)
{int i;
    for(i=1; i<=n; i++)
        printf("***\n");
}
