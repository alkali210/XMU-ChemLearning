import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 设置中文字体
font = FontProperties(fname=r"c:\windows\fonts\simhei.ttf", size=12)

# 数据
Is = np.array([0.00, 0.50, 1.00, 1.50, 2.00, 2.50, 3.00]) # 控制电流 (mA)
UH = np.array([0.00, 1.60, 3.20, 4.85, 6.40, 8.00, 9.60]) # 霍尔电压 (mV)
KH = 23.0 # 霍尔元件灵敏度 mV/(mA·T)
Im = 0.600 # 励磁电流 (A)

# 线性拟合
p = np.polyfit(Is, UH, 1)
slope_k = p[0]
intercept = p[1]
fit_line = slope_k * Is + intercept

# 计算 B 和 Km
B_calc = slope_k / KH
Km_calc = B_calc / Im

# 绘图
plt.figure(figsize=(8, 6))
plt.plot(Is, UH, 'o', label='实验数据点')
plt.plot(Is, fit_line, 'r-', label=f'线性拟合: U_H = {slope_k:.4f} * I_s + {intercept:.4f}')

plt.title('霍尔电压与控制电流关系的 $U_H-I_s$ 特性曲线', fontproperties=font)
plt.xlabel('控制电流 $I_s$ (mA)', fontproperties=font)
plt.ylabel('霍尔电压 $U_H$ (mV)', fontproperties=font)
plt.grid(True)
plt.legend(prop=font)

# 在图下方添加计算结果
caption = (
    f"k = {slope_k:.4f} mV/mA。\n"
    f"由 $B = k / K_H$ 计算出气隙中心磁感应强度 B = {slope_k:.4f} / {KH} = {B_calc:.4f} T。\n"
    f"由 $K_m = B / I_m$ 计算出励磁系数 $K_m$ = {B_calc:.4f} / {Im} = {Km_calc:.4f} T/A。"
)
plt.figtext(0.5, 0.05, caption, ha="center", fontsize=12, fontproperties=font, linespacing=1)

plt.subplots_adjust(bottom=0.25)
plt.show()