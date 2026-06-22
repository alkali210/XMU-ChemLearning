clear;clc
l=1; %set the minimum value of the interval as l(lower)
u=7; %set the maximum value of the interval as u(upper)
f=@(x)x^2-7*x+10; %the goal function
e=0.0001;%set minimum interval length as e
while ((u-l)>=e)%the length of the interval to be optimized is less than the set value
    % take optimization
    a1=l+0.5*(u-l);%Take the median value'function value
    if f(a1)<=min(f(l),f(u)) %the median value'function value f(a1) is lower than f(l) and f(u)
        if f(l)<f(u)
            l=l;
            u=a1; %interval (l,u)->(l,a1),keep the left part
        else
            u=u;
            l=a1; %interval (l,u)->(a1,u),keep the right part
        end
    elseif f(a1)>min(f(l),f(u)) && f(a1)<=max(f(l),f(u)) %the median value'function value f(a1) is between f(l) and f(u)
        if f(l)>f(u) 
            l=a1;
            u=u; %interval (l,u)->(l,a1),keep the right part
        else
            l=l;
            u=a1; %interval (l,u)->(a1,u),keep the left part
        end
    else %the median value'function value f(a1) is upper than f(l) and f(u)
        if f(l)>f(u)
            u=u;
            l=a1; %interval (l,u)->(a1,u),keep the right part
        else
            l=l;
            u=a1 %interval (l,u)->(l,a1),keep the left part
        end
    end
end %optimization finished
X=(l+u)/2; %take the midian value X and its function value f(X) of the final inerval
disp(['optimal solution:X=',num2str(X)]);
disp(['optimal value:f(X)=',num2str(f(X))]);
%editor chen jian 37420232204732