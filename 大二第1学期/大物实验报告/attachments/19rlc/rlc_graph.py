import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
from scipy.signal import find_peaks
import time

start = time.time()

plt.rc('text', usetex=True) # 使用tex渲染文字
plt.rc('font', family='serif')

def spl(x, y):
    return make_interp_spline(x, y, k=3)

f = np.array([
    1.4000, 1.5000, 1.6000, 1.7000, 1.8000, 1.9000, 2.0000, 2.0500, 2.1000, 2.1500, 2.2000, 2.2500, 2.3000, 2.3500, 2.4000, 2.4500, 2.5000, 2.6000, 2.7000, 2.8000, 2.9000, 3.0000, 3.1000
])

L, r_L, C, U = 0.100, 16.0, 0.0500, 0.900
R0, R0_prime = 100.0, 216.0
    
# —— 输入测得的数据 ——
U_R0 = np.array([
    65, 80, 98, 115, 148, 192, 260, 330, 410, 510, 660, 740, 660, 
    520, 420, 340, 270, 220, 175, 155, 120, 110, 98
])
U_R0_prime = np.array([
    140, 175, 210, 240, 295, 370, 510, 570, 640, 740, 800, 820, 
    800, 720, 670, 600, 530, 420, 340, 280, 240, 220, 190
])
# ———————————————————

I_R0 = U_R0 / R0 # mA
I_R0_prime = U_R0_prime / R0_prime # mA

if __name__ == '__main__':
    try:
        f_interp = np.linspace(f.min(), f.max(), 500)
        
        spline_R0 = spl(f, I_R0)
        I_interp = spline_R0(f_interp)
        
        spline_R0_prime = spl(f, I_R0_prime)
        I_prime_interp = spline_R0_prime(f_interp)

        # 找到顶点
        peak_idx = np.argmax(I_interp)
        f_peak = f_interp[peak_idx]
        I_peak = I_interp[peak_idx]

        peak_idx_prime = np.argmax(I_prime_interp)
        f_peak_prime = f_interp[peak_idx_prime]
        I_peak_prime = I_prime_interp[peak_idx_prime]

        # 找到半高点
        max_avg = I_peak / np.sqrt(2)
        max_avg_prime = I_peak_prime / np.sqrt(2)

        # 寻找半高线交点
        # 左侧
        left_idx = np.argmin(np.abs(I_interp[:peak_idx] - max_avg))
        # 右侧
        right_idx = np.argmin(np.abs(I_interp[peak_idx:] - max_avg)) + peak_idx
        
        # 左侧
        left_idx_prime = np.argmin(np.abs(I_prime_interp[:peak_idx_prime] - max_avg_prime))
        # 右侧
        right_idx_prime = np.argmin(np.abs(I_prime_interp[peak_idx_prime:] - max_avg_prime)) + peak_idx_prime

        # 标记顶点和半高点
        plt.plot(f_peak, I_peak, 'x', color='red')
        plt.plot(f_interp[left_idx], I_interp[left_idx], 'o', color='red')
        plt.plot(f_interp[right_idx], I_interp[right_idx], 'o', color='red')
        
        plt.plot(f_peak_prime, I_peak_prime, 'x', color='blue')
        plt.plot(f_interp[left_idx_prime], I_prime_interp[left_idx_prime], 'o', color='blue')
        plt.plot(f_interp[right_idx_prime], I_prime_interp[right_idx_prime], 'o', color='blue')
        
        # 标注特殊点坐标
        plt.text(f_peak, I_peak, rf'$f_0={f_peak:.3f}$', ha='center', va='bottom')
        plt.text(f_interp[left_idx], I_interp[left_idx], rf'$f_1={f_interp[left_idx]:.3f}$', ha='right', va='bottom')
        plt.text(f_interp[right_idx], I_interp[right_idx], rf'$f_2={f_interp[right_idx]:.3f}$', ha='left', va='bottom')

        plt.text(f_peak_prime, I_peak_prime, rf'$f_0^\prime={f_peak_prime:.3f}$', ha='center', va='bottom')
        plt.text(f_interp[left_idx_prime], I_prime_interp[left_idx_prime], rf'$f_1^\prime={f_interp[left_idx_prime]:.3f}$', ha='right', va='bottom')
        plt.text(f_interp[right_idx_prime], I_prime_interp[right_idx_prime], rf'$f_2^\prime={f_interp[right_idx_prime]:.3f}$', ha='left', va='bottom')

        # 绘制半高线
        plt.axhline(y=max_avg, color='red', linestyle='--', linewidth=0.75)
        plt.axhline(y=max_avg_prime, color='blue', linestyle='--', linewidth=0.75)
        
        # 绘制原始点
        plt.plot(f, I_R0, 'o', markersize=4, label=r'R_0 = 100 $\Omega$ (measured)')
        plt.plot(f, I_R0_prime, 's', markersize=4, label=r'R_0$^\prime$ = 216 $\Omega$ (measured)')
        
        # 绘制插值曲线
        plt.plot(f_interp, I_interp, linewidth=0.75, label=r'R_0 = 100 $\Omega$ (spline)')
        plt.plot(f_interp, I_prime_interp, linewidth=0.75, label=r'R_0$^\prime$ = 216 $\Omega$ (spline)')
        
        plt.legend()
        plt.grid()

        plt.xlabel(rf'$f$ (kHz)')
        plt.ylabel(rf'$I$ (mA)')
        plt.title(rf'$I-f$ Curve')
        
        end = time.time()
        print(f'绘图使用了 {end - start:.4f} s.')
        
        plt.show()
        
    except Exception as e:
        print(e)