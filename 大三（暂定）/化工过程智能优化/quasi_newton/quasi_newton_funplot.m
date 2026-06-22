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




f =@(T) (1.767 * log(omega0/omegaD) / ((-0.2631125 + 0.0028958*T) * (omega0^(-0.2368125 + 0.000966*T)) * Vt)) * ...
        ((FA * CPA + U * A) * ((-0.2631125 + 0.0028958*T) * (omega0^(-0.2368125 + 0.000966*T)) - T1) * Cp_prime) / ...
        (DeltaHc + P * CE_prime + CL_prime);

for i = 400:3000
    y=f(i);
    plot(i,y,'bo');
    hold on
end

