import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 设置中文字体
font = FontProperties(fname=r"c:\windows\fonts\simhei.ttf", size=12)

# 数据
Im_mA = np.array([0, 100, 200, 300, 400, 500, 600]) # 励磁电流 (mA)
Im_A = Im_mA / 1000.0 # 转换为 A
B = np.array([0.0004, 0.0239, 0.0467, 0.0710, 0.0942, 0.1174, 0.1391]) # 磁场 (T)

# 线性拟合
# 忽略第一个点(0,0)以获得更好的线性拟合效果，因为电磁铁在低电流下可能存在非线性区域
p = np.polyfit(Im_A[1:], B[1:], 1)
Km = p[0]
b = p[1]
fit_line = Km * Im_A + b

# 绘图
plt.figure(figsize=(8, 6))
plt.plot(Im_A, B, 'o', label='实验数据点')
plt.plot(Im_A, fit_line, 'r-', label=f'线性拟合: B = {Km:.4f} * I_m + {b:.4f}')

plt.title('电磁铁的 B-I_m 励磁特性曲线', fontproperties=font)
plt.xlabel('励磁电流 $I_m$ (A)', fontproperties=font)
plt.ylabel('磁感应强度 B (T)', fontproperties=font)
plt.grid(True)
plt.legend(prop=font)

# 在图下方添加计算结果
caption = f"根据线性拟合结果，该电磁铁的励磁系数 $K_m$ (曲线斜率) 为: {Km:.4f} T/A"
plt.figtext(0.5, 0.01, caption, ha="center", fontsize=12, fontproperties=font)

plt.show()