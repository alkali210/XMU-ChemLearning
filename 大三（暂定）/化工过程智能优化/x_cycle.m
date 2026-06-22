%坐标轮换法（变量轮换法）
%将多变量转为多个单变量进行搜索
%每个变量都有各自的方向和最优步长，并且各方向彼此正交
%当所有维数都优化一次（做一组循环）后，将最初的x与结束时的x作差
%范数norm小于给定精度epsilon时结束循环，完成优化
%反之进行下一轮优化

%优点：
%思路清晰，简单
%沿坐标轴方向进行搜索
%缺点：
%收敛速度低
%搜索效率低

clc;clear;

epsilon=0.0001;
x=[0;0];


f=@(x) x(1)^2+x(2)^2-x(1)*x(2)-10*x(1)-4*x(2)+60;



while 1
    lambda=0;
    xp=x;

    e1=[1;0];
    l=-7; %set the minimum value of the interval as l(lower)
    u=7; %set the maximum value of the interval as u(upper)

    e=0.0001;%set minimum interval length as e
    while ((u-l)>=e)%the length of the interval to be optimized is less than the set value
        % take optimization
        a1=l+0.5*(u-l);%Take the median value'function value
        if f(xp+a1*e1)<=min(f(xp+l*e1),f(xp+u*e1)) %the median value'function value f(a1) is lower than f(l) and f(u)
            if f(xp+l*e1)<f(xp+u*e1)
                l=l;
                u=a1; %interval (l,u)->(l,a1),keep the left part
            else
                u=u;
                l=a1; %interval (l,u)->(a1,u),keep the right part
            end
        elseif f(xp+a1*e1)>min(f(xp+l*e1),f(xp+u*e1)) && f(xp+a1*e1)<=max(f(xp+l*e1),f(xp+u*e1)) %the median value'function value f(a1) is between f(l) and f(u)
            if f(xp+l*e1)>f(xp+u*e1) 
                l=a1;
                u=u; %interval (l,u)->(l,a1),keep the right part
            else
                l=l;
                u=a1; %interval (l,u)->(a1,u),keep the left part
            end
        else %the median value'function value f(a1) is upper than f(l) and f(u)
            if f(xp+l*e1)>f(xp+u*e1)
                u=u;
                l=a1; %interval (l,u)->(a1,u),keep the right part
            else
                l=l;
                u=a1; %interval (l,u)->(l,a1),keep the left part
            end
        end
    end %optimization finished
    lambda=(l+u)/2; %take the midian value X and its function value f(X) of the final inerval
    xp=xp+lambda*e1;

    l=-7; %set the minimum value of the interval as l(lower)
    u=7; %set the maximum value of the interval as u(upper)
    e2=[0;1];

    e=0.0001;%set minimum interval length as e
    while ((u-l)>=e)%the length of the interval to be optimized is less than the set value
        % take optimization
        a1=l+0.5*(u-l);%Take the median value'function value
        if f(xp+a1*e2)<=min(f(xp+l*e2),f(xp+u*e2)) %the median value'function value f(a1) is lower than f(l) and f(u)
            if f(xp+l*e2)<f(xp+u*e2)
                l=l;
                u=a1; %interval (l,u)->(l,a1),keep the left part
            else
                u=u;
                l=a1; %interval (l,u)->(a1,u),keep the right part
            end
        elseif f(xp+a1*e2)>min(f(xp+l*e2),f(xp+u*e2)) && f(xp+a1*e2)<=max(f(xp+l*e2),f(xp+u*e2)) %the median value'function value f(a1) is between f(l) and f(u)
            if f(xp+l*e2)>f(xp+u*e2) 
                l=a1;
                u=u; %interval (l,u)->(l,a1),keep the right part
            else
                l=l;
                u=a1; %interval (l,u)->(a1,u),keep the left part
            end
        else %the median value'function value f(a1) is upper than f(l) and f(u)
            if f(xp+l*e2)>f(xp+u*e2)
                u=u;
                l=a1; %interval (l,u)->(a1,u),keep the right part
            else
                l=l;
                u=a1; %interval (l,u)->(l,a1),keep the left part
            end
        end
    end %optimization finished
    lambda=(l+u)/2; %take the midian value X and its function value f(X) of the final inerval
    xp=xp+lambda*e2;


    if norm(x-xp)<epsilon
        x=xp
        break
    else
        x=xp;
    end

    
end
x
f(x)