import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from math import log as ln

plt.rcParams.update({'font.family': 'serif'})

m = np.array([220.00, 320.05, 419.71, 520.15])
m1 = m * 10**-3
T_squared = np.array([2.3192, 3.3507, 4.3706, 5.4010])

slope, intercept, r_value, p_value, std_err = stats.linregress(m1, T_squared)

line = slope * m1 + intercept

plt.figure(figsize=(10, 6))
plt.scatter(m1, T_squared, s=50, alpha=0.7, label='Data points')
plt.plot(m1, line, 'c-', linewidth=2, label=f'$T^2$ = {slope:.4f}$m_1$ + {intercept:.4f}')

plt.xlabel(r'$m_1$ (kg)', fontsize=12)
plt.ylabel('$T^2$ ($s^2$)', fontsize=12)
plt.legend()

plt.text(0.05, 0.95, f'r = {r_value:.6f}', 
         transform=plt.gca().transAxes, 
         fontsize=11,
         bbox=dict(facecolor='white', alpha=0.8))

print(f'intercept (α) = {intercept:.6f}')
print(f'slope (β) = {slope:.6f}')
print(f'r = {r_value:.6f}')
print(f'p-value = {p_value:.6e}')
print(f'std_err = {std_err:.6e}')

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()