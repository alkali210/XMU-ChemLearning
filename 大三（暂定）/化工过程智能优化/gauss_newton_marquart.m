%高斯牛顿法
%对于位置关系的x和y
%通过实验得到n个数据点
%作图得到一条曲线,通过比较选择一条带有k个参数的函数模型y=f(x)
%把k个参数是做未知量，将n个实验点带入得到一个nX1的向量
%用s=(1->n)Σ(f(x)-y)^2  (残差和）评价拟合程度
%当s取最小值时拟合效果最好

%马夸特法的修正
%步骤
%1.给定初始值，精度，初始阻尼因子λ，阻尼放大倍数μ，一个维数为k的单位阵E
%2.求n个实验点的残差向量f(x)
%3.对于给定的函数模型，求jabobian矩阵
%4.dx=-inv((j)'*j+λ*E)*(j)'*(f(x))
%6.目标函数z(x)=f(x)'*f(x)
%7.令xp=x+lambda*dx 
%8.如果z(xp)<z(x)时把xp赋给x
%9.反之λ=λ/μ，重复上述过程，直到z(xp)<z(x)为止
%5.当norm(dx)小于给定精度时完成优化

%jacobian阵的使用
%定义符号变量 smys
%含参矩阵f=[....(a,b,c)]
%j=jacobian(f,[a,b,c])
%带入指定值 x=[1;2;3]
%j_at_value=eval(subs(j,{a,b,c},{x(1),x(2),x(3)}

clc;clear


x=[0.5;-0.1;0.001];

miu=2;


re=[4658 5820 6525 7400 9045 10350 11050 11820 12850 13840];
lmd=[0.0399 0.0386 0.0368 0.0362 0.0349 0.0339 0.0341 0.0323 0.0324 0.0321];

syms a b c

E=eye(3);

e=1e-3;
f=[a*re(1)^b+c-lmd(1);a*re(2)^b+c-lmd(2);a*re(3)^b+c-lmd(3);a*re(4)^b+c-lmd(4);
    a*re(5)^b+c-lmd(5);a*re(6)^b+c-lmd(6);a*re(7)^b+c-lmd(7);a*re(8)^b+c-lmd(8);a*re(9)^b+c-lmd(9);a*re(10)^b+c-lmd(10)];

j=jacobian(f,[a,b,c]);

z=(f')*f;



while true
    ld=0.1;

    jatv=eval(subs(j,{a,b,c},{x(1),x(2),x(3)})); 
    
    fatv=eval(subs(f,{a,b,c},{x(1),x(2),x(3)}));
    

    dx=-inv((jatv)'*jatv+ld*E)*(jatv)'*(fatv);
    
    xp=x+ld*dx;
    

    zatv=eval(subs(z,{a,b,c},{x(1),x(2),x(3)}));
    zatvp=eval(subs(z,{a,b,c},{xp(1),xp(2),xp(3)})); 

    while zatvp>zatv
        ld=ld*miu;

        dx=-inv((jatv)'*jatv+ld*E)*(jatv)'*(fatv);
        xp=xp+ld*dx;

        zatv=eval(subs(z,{a,b,c},{x(1),x(2),x(3)}));
        zatvp=eval(subs(z,{a,b,c},{xp(1),xp(2),xp(3)}));
    end

    x=xp;

    if norm(dx)<e
        break
    end
end
    
x

%editor chenjian 37420232204732









    
