clc;
clear;
T=600; %origin temperature
h=1; 

%define paramater
omega0 = 0.5;
omegaD = 0.175;
Vt = 56;
FA = 150;
CPA = 1046.75;
U = 45;
A = 25.3;
T1 = 390;
Cp_prime = 0.18;
DeltaHc = 4.64e7;
P = 188;
CE_prime = 0.8;
CL_prime = 30;

%target function
f =@(T) (1.767 * log(omega0/omegaD) / ((-0.2631125 + 0.0028958*T) * (omega0^(-0.2368125 + 0.000966*T)) * Vt)) * ...
        ((FA * CPA + U * A) * ((-0.2631125 + 0.0028958*T) * (omega0^(-0.2368125 + 0.000966*T)) - T1) * Cp_prime) / ...
        (DeltaHc + P * CE_prime + CL_prime);

%quasi newton optimization
f1=@(T) (f(T+h)-f(T))/(h);
f2=@(T) (f(T+2*h)-2*f(T+h)+f(T))/(h^2);
k=0;
tmp1=f1(T);
e=1e-10; %accuracy degree

tmp3=800;
while abs(f1(T))>=e
    tmp1=f1(T);
    tmp2=f2(T);
    if T>0
        tmp3=T;
    else
        break
    end
    T=T-tmp1/tmp2;
    k=k+1;
end

%draw the function plot
for i = 400:3000
    y=f(i);
    plot(i,y,'bo');
    hold on
end

%output result
disp('cycle times')
disp(k)
disp('final of optimization =')
disp(T)
disp('its function =')
disp(f(T))

%editor:chenjian 37420232204732