import matplotlib.pyplot as plt
import numpy as np
from src.l2_finder import find_L2_location
from src.simulation import run_simulation

# Sabitler
m_earth = 5.972e24
m_sun = 1.989e30
mu = m_earth / (m_sun + m_earth)

print("--- JWST SİMÜLASYONU BAŞLIYOR ---")

# 1. L2'yi Bul
L2_loc = find_L2_location(mu)
print(f"L2 Konumu: {L2_loc:.6f} AU")

# 2. Simülasyonu Yap
print("Yörünge hesaplanıyor...")
x_vals, y_vals = run_simulation(mu, L2_loc)

# 3. Çiz
plt.style.use('dark_background')
plt.figure(figsize=(10, 8))
plt.plot(-L2_loc, 0, 'yo', markersize=10, label='Gunes') # Temsili
plt.plot(L2_loc, 0, 'rx', markersize=8, label='L2 Noktasi')
plt.plot(x_vals, y_vals, 'c-', linewidth=1.5, label='JWST Halo Yorungesi')

plt.legend()
plt.title("James Webb - L2 Halo Yörüngesi")
plt.axis('equal')
plt.grid(True, alpha=0.3)

# Resmi Kaydet
plt.savefig("images/orbit_result.png")
print("Grafik kaydedildi: images/orbit_result.png")
plt.show()