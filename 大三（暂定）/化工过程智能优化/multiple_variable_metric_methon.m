%变尺度法
%牛顿法的缺点：每次迭代都需要计算逆矩阵，计算量大
%基本思想：构造一系列不含二阶偏导数的尺度矩阵
%来近似牛顿法的hessian矩阵的逆阵
%一般尺度矩阵的初值是单位矩阵，维数与X维数相同
f=@(x) x(1)^2-x(1)*x(2)+x(2)^2+2*x(1)-4*x(2);%target function

x=[2;2];%initial x

%gradient and hessian martrix
g = @(x)[2*x(1)-x(2)+2;-x(1)+2*x(2)-4];%gradient of f(x)
h = [1,0;0,1];%quasi_hessian martrix

epsilon=0.01;%degree of accuracy

%optimization on 2D
while true
    p=-h*g(x);
    lamda=1;
    %optimization to step(on 1D,for lamda) 
    while f(x+lamda*p)>f(x)+(1e-4)*lamda*g(x)'*p
        lamda=lamda*0.5;
    end
    x=x+lamda*p;
    deltaG=g(x)-g(x-lamda*p);
    h=h+(lamda^2*p*(p'))/(lamda*(p')*deltaG)-(h*deltaG*(deltaG')*(h'))/((deltaG')*h*deltaG);
    if norm(g(x))<epsilon
        break
    end

end

%output optimization
f(x)
x

%editor chenjian 37420232204732