int sxhs(int x)
{ int a, b, c;
    a = x % 10;
    b = x / 10 % 10;
    c = x / 100 % 10;
    return a*a*a + b*b*b + c*c*c == x;
}
