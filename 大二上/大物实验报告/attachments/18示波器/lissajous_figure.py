import numpy as np
import matplotlib.pyplot as plt

ampl1, ampl2 = 1, 1
freq1, freq2 = 3, 2 # 输入频率（或者频率的比）
delta = 0 * np.pi / 4 # 相位差

t = np.linspace(0, 2 * np.pi, 1000)
x = ampl1 * np.sin(freq1 * t + delta)
y = ampl2 * np.sin(freq2 * t)


plt.figure(figsize=(8, 6)) # 设置图形大小
plt.plot(x, y, linewidth = 4) # 设置linewidth的值来调整线宽
for spine in plt.gca().spines.values():
    spine.set_visible(False) # 隐藏外边框
plt.xticks([])
plt.yticks([]) # 隐藏轴刻度
plt.grid()
plt.show()