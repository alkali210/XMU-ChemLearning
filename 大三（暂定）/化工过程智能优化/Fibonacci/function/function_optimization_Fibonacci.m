disp('optimization function:[x,result]=Fibonacci(f,e)')
disp('f=goal function')
disp('e=minimum optimization interval')
disp('x=independent variable of the minimum value')
disp('result=the result of optimization')



function [x,result]=Fibonacci(f,e)

%determine the optimization interval[a,b]

x0=3; %a ramdom x to start
h=0.2;
m=2;
if f(x0+h)>f(x0) %go back
    if f(x0-h)<f(x0) %the minvalue is back of x0
        while f(x0-h*(2^m-1))<f(x0-h*(2^(m-1)-1)) %the minvalue is back of this , continnue to go back
            m=m+1;
        end
        a=x0-h*(2^m-1);b=x0-h*(2^(m-1)-1); %the optimization interval [a,b]
    else
        a=x0-h;b=x0; %the optimition interval [a,b]
    end
elseif f(x0+h)<f(x0) %go ahead
    if f(x0+h)<f(x0)
        while f(x0+h*(2^m-1))<f(x0+h*(2^(m-1)-1)) %the minvalue is in front of this,go ahead
            m=m+1;
        end
        a=x0+h*(2^m-1);b=x0+h*(2^(m-1)-1); %the optimization interval [a,b]
    else
        a=x0;b=x0+h; %the optimition interval [a,b]
    end
else
    a=x0;b=x0+h; %the minvalue is in the [x0,xo+h],no need to check,the optimization interval [a,b]
end

%get the appropriate Febonacci series

F=[1,1]; %the initial Febonacci series
n=3; %add Febonacci number to the list F start with F3
while F(1)/F(end)<e/(b-a); %determine the maxvalue of n 
    F(n)=F(n-1)+F(n-2); 
    n=n+1;
end

%shrink the interval and determin the min-value

n=n-1; 
x1=a+(F(n-2)/F(n))*(b-a);
x2=a+(F(n-1)/F(n))*(b-a);
f1=f(x1); 
f2=f(x2); 
k=0;%get the initial value in the interval
while n>3; %out the cycle when n is blow to 3
    k=k+1; n=n-1;
    if f1>f2 %take the right part
        a=x1; 
        x1=x2; 
        f1=f2; 
        x2=a+(F(n-1)/F(n))*(b-a); 
        f2=f(x2); %set new interval and value in it 
    elseif f1==f2 %take the middle part
        a=x1; 
        b=x2; 
        x1=a+(F(n-2)/F(n))*(b-a); 
        x2=a+(F(n-1)/F(n))*(b-a); %set new interval and value in it 
    else %take the left part
        b=x2; 
        x2=x1; 
        f2=f1; 
        x1=a+(F(n-2)/F(n))*(b-a);
        f1=f(x1); %set new interval and value in it 
    end
end

%output the result

x=(a+b)/2; result=f(x);
disp("the minimum value =");disp(result)
disp ("its independent variable =");disp(x)
end


