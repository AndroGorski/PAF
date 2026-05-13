import numpy as np
import matplotlib.pyplot as plt

# Parametri
M = np.array([0.052, 0.124, 0.168, 0.236, 0.284, 0.336])  # Nm
phi = np.array([0.1745, 0.3491, 0.5236, 0.6981, 0.8727, 1.0472])  # rad

n = len(M)

# Formule linearne regresije: y = a*x + b, gdje je b = 0
# a = Σ(xy) / Σ(x²)
# σa = √((1/n) * (Σy² / Σx² - a²))

# Izračuni potrebnih suma
sum_xy = np.sum(phi * M)
sum_x2 = np.sum(phi**2)
sum_y2 = np.sum(M**2)

# Koeficijent a (modul torzije)
a = sum_xy / sum_x2
print(f"Modul torzije Dt = {a:.6f} Nm/rad")

# Standardna greška koeficijenta a
sigma_a = np.sqrt((1/n) * (sum_y2 / sum_x2 - a**2))
print(f"Standardna greška σa = {sigma_a:.6f}")

# Srednje vrijednosti
mean_phi = np.mean(phi)
mean_M = np.mean(M)

print(f"\nSrednja vrijednost φ = {mean_phi:.6f} rad")
print(f"Srednja vrijednost M = {mean_M:.6f} Nm")
print(f"Broj mjerenja n = {n}")

# Grafički prikaz
plt.figure(figsize=(10, 6))

# Eksperimentalni podaci
plt.scatter(phi, M, color='red', s=100, label='Eksperimentalni podaci', zorder=3)

# Linija linearne regresije (y = a*x + b, gdje je b = 0)
phi_line = np.linspace(0, max(phi)*1.1, 100)
M_line = a * phi_line

plt.plot(phi_line, M_line, 'b-', linewidth=2, label=f'Linearna regresija: M = {a:.6f}·φ')

# Oznake i naslov
plt.xlabel('Kut torzije φ (rad)', fontsize=12)
plt.ylabel('Moment torzije M (Nm)', fontsize=12)
plt.title(f'Određivanje modula torzije Dt = {a:.6f} Nm/rad', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)

# Prikazi rezultate na grafu
textstr = f'Dt = {a:.6f} ± {sigma_a:.6f} Nm/rad\nR² = {1 - np.sum((M - a*phi)**2)/np.sum((M - mean_M)**2):.6f}'
plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=11,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.show()