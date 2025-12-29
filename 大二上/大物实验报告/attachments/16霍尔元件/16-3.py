import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 设置中文字体
font = FontProperties(fname=r"c:\windows\fonts\simhei.ttf", size=12)

# 数据
X = np.array([30.0, 29.0, 28.0, 26.0, 25.0, 24.0, 23.0, 22.0, 20.0, 15.0, 10.0, 0.0, -10.0, -14.0, -16.0, -17.0, -18.0, -19.0, -21.0, -23.0, -25.0, -27.0, -30.0]) # 位置 (mm)
B = np.array([0.0630, 0.0739, 0.0797, 0.1072, 0.1174, 0.1290, 0.1333, 0.1377, 0.1391, 0.1391, 0.1377, 0.1362, 0.1348, 0.1203, 0.1000, 0.0906, 0.0812, 0.0710, 0.0565, 0.0478, 0.0413, 0.0362, 0.0319]) # 磁场 (T)

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(X, B, 'o-')

plt.title('电磁铁气隙间的 B-X 磁场分布曲线', fontproperties=font)
plt.xlabel('霍尔元件位置 X (mm)', fontproperties=font)
plt.ylabel('磁感应强度 B (T)', fontproperties=font)
plt.grid(True)

# 在图下方添加说明
caption = ""
plt.figtext(0.5, 0.01, caption, ha="center", fontsize=12, fontproperties=font)

plt.show()