f=@(x) x(1)-x(2)+2*x(1)^2+2*x(1)*x(2)+x(2)^2;%target function
e0=1e-7;%degree of accuracy
x=[0;0];%initial x

%gradient and hessian martrix
g = @(x)[1+4*x(1)+2*x(2);-1+2*x(1)+2*x(2)];%gradient of f(x)
h = [4,2;2,2];%hessian martrix
x0=[0;0];
epsilon=1e-6;

%optimization on 2D
while true
    p=-inv(h)*g(x);
    lamda=1;
    s=1;
    %optimization to step(1D,lamda) 
    while f(x+lamda*p)>f(x)+(1e-4)*lamda*g(x)'*p
        lamda=lamda*0.5;
    end
    x=x+lamda*p;
    if norm(g(x)) < epsilon
        break
    end

end

%output optimization
f(x)
x

%editor chenjian 37420232204732