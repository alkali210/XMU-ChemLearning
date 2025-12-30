int qshu(int n, int k)
{ int i;
    for(i = 1; i < k; i++)
        n = n / 10;
    return n % 10;
}
