% 频率 f (kHz)
f = [
    1.4000; 1.5000; 1.6000; 1.7000; 1.8000; 1.9000; 2.0000; 2.0500; 
    2.1000; 2.1500; 2.2000; 2.2500; 2.3000; 2.3500; 2.4000; 2.4500; 
    2.5000; 2.6000; 2.7000; 2.8000; 2.9000; 3.0000; 3.1000
];

% =================================
% U_R0 (mV) 在此输入测得的数据
U_R0 = [
    65; 80; 98; 115; 148; 192; 260; 330; 410; 510; 660; 740; 660; 
    520; 420; 340; 270; 220; 175; 155; 120; 110; 98
];
% =================================

% I (mA)
I = [
    0.65; 0.80; 0.98; 1.15; 1.48; 1.92; 2.60; 3.3; 4.1; 5.1; 6.6; 
    7.4; 6.6; 5.2; 4.2; 3.4; 2.70; 2.20; 1.75; 1.55; 1.20; 1.10; 0.98
];

% =================================
% U_R0_prime (mV) 在此输入测得的数据
U_R0_prime = [
    140; 175; 210; 240; 295; 370; 510; 570; 640; 740; 800; 820; 
    800; 720; 670; 600; 530; 420; 340; 280; 240; 220; 190
];
% =================================

% I_prime (mA)
I_prime = [
    0.65; 0.810; 0.972; 1.11; 1.37; 1.7; 2.4; 2.6; 3.0; 3.4; 3.7; 
    3.8; 3.7; 3.3; 3.1; 2.8; 2.5; 1.9; 1.6; 1.30; 1.11; 1.02; 0.880
];

% 将所有数据合并为一个矩阵
all_data = [f, U_R0, I, U_R0_prime, I_prime];

% 创建一个更密集的频率点用于插值，以获得平滑曲线
f_interp = linspace(min(f), max(f), 1000);

% 使用 'spline' 方法进行三次样条插值
I_interp = interp1(f, I, f_interp, 'spline');
I_prime_interp = interp1(f, I_prime, f_interp, 'spline');

figure; 

% 绘制原始数据点（可选，用以对比）
% plot(f, I, 'bo', f, I_prime, 'ro'); 

hold on; % 保持当前图像，以便在其上添加新的曲线

% 绘制插值后的曲线
plot(f_interp, I_interp, 'LineWidth', 1.5);
plot(f_interp, I_prime_interp, 'LineWidth', 1.5);

% --- 处理第一条曲线 (I_interp) ---
% 找到顶点
[I_interp_max, idx_max] = max(I_interp);
f_max = f_interp(idx_max);
% 标记顶点
plot(f_max, I_interp_max, 'k^', 'MarkerFaceColor', 'b');
text(f_max, I_interp_max, sprintf('  (%.3f, %.2f)', f_max, I_interp_max), 'VerticalAlignment', 'bottom');

% 计算半高宽并绘制水平线
half_max_I = I_interp_max / 2;
plot(get(gca, 'XLim'), [half_max_I, half_max_I], 'b--');

% 找到与半高宽线的交点
intersections_I = f_interp(diff(I_interp > half_max_I) ~= 0);
f1 = intersections_I(1);
f2 = intersections_I(2);
% 标记交点
plot([f1, f2], [half_max_I, half_max_I], 'bo', 'MarkerFaceColor', 'b');
text(f1, half_max_I, sprintf('f_1=%.3f ', f1), 'HorizontalAlignment', 'right');
text(f2, half_max_I, sprintf(' f_2=%.3f', f2), 'HorizontalAlignment', 'left');

% --- 处理第二条曲线 (I_prime_interp) ---
% 找到顶点
[I_prime_interp_max, idx_prime_max] = max(I_prime_interp);
f_prime_max = f_interp(idx_prime_max);
% 标记顶点
plot(f_prime_max, I_prime_interp_max, 'k^', 'MarkerFaceColor', 'r');
text(f_prime_max, I_prime_interp_max, sprintf('  (%.3f, %.2f)', f_prime_max, I_prime_interp_max), 'VerticalAlignment', 'bottom');

% 计算半高宽并绘制水平线
half_max_I_prime = I_prime_interp_max / 2;
plot(get(gca, 'XLim'), [half_max_I_prime, half_max_I_prime], 'r--');

% 找到与半高宽线的交点
intersections_I_prime = f_interp(diff(I_prime_interp > half_max_I_prime) ~= 0);
f1_prime = intersections_I_prime(1);
f2_prime = intersections_I_prime(2);
% 标记交点
plot([f1_prime, f2_prime], [half_max_I_prime, half_max_I_prime], 'ro', 'MarkerFaceColor', 'r');
text(f1_prime, half_max_I_prime, sprintf('f''_1=%.3f ', f1_prime), 'HorizontalAlignment', 'right');
text(f2_prime, half_max_I_prime, sprintf(' f''_2=%.3f', f2_prime), 'HorizontalAlignment', 'left');

% --- 整理图像 ---
hold off; 
title('谐振曲线 I-f');
xlabel('频率 f (kHz)');
ylabel('电流 I (mA)');
legend('I (R_0 = 100.0 \Omega)', 'I'' (R''_0 = 216.0 \Omega)');
grid on;
xtickformat('%.4f')
axis tight; % 调整坐标轴范围以适应数据