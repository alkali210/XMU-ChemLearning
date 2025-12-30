int fun(long n)
{ long m;
    m = n * n;
    while(n != 0) {
        if(n % 10 != m % 10) return 0;
        n /= 10;
        m /= 10;
    }
    return 1;
}
