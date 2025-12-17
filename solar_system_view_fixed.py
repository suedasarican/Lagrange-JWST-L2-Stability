import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src.l2_finder import solve_l2_position
from src.simulation import run_mission_simulation

# --- SABİTLER ---
M_EARTH = 5.972e24
M_SUN = 1.989e30
MU = M_EARTH / (M_SUN + M_EARTH)

def main():
    print("--- JAMES WEBB OTO-ZOOM (GARANTİLİ) ---")
    
    # 1. Simülasyonu Çalıştır
    l2_dist = solve_l2_position(MU)
    l2_abs = (1 - MU) + l2_dist
    
    start_state = np.array([l2_abs - 0.002, 0.0, 0.0, 0.012])
    duration = 3.2 
    dt = 0.015
    
    # Veriyi hesapla
    x_rot, y_rot = run_mission_simulation(MU, start_state, duration=duration, dt=dt)
    t_vals = np.linspace(0, duration, len(x_rot))

    # --- OTO-ZOOM HESAPLAMASI ---
    # Yörüngenin Y ekseninde (yukarı-aşağı) en çok nereye gittiğini buluyoruz.
    max_y_excursion = np.max(np.abs(y_rot))
    
    # Bu değere %50 "Güvenlik Payı" ekliyoruz.
    # Böylece yörünge ekranın kenarına yapışmaz, rahat sığar.
    safe_limit_y = max_y_excursion * 1.5
    
    print(f"-> Hesaplanan Maksimum Sapma: {max_y_excursion:.5f} AU")
    print(f"-> Ekran Limiti Ayarlanıyor: {safe_limit_y:.5f} AU (Garanti Sığar)")

    # 2. Koordinat Dönüşümleri
    jwst_inertial_x = x_rot * np.cos(t_vals) - y_rot * np.sin(t_vals)
    jwst_inertial_y = x_rot * np.sin(t_vals) + y_rot * np.cos(t_vals)
    l2_x_inertial = l2_abs * np.cos(t_vals)
    l2_y_inertial = l2_abs * np.sin(t_vals)
    earth_dist = 1 - MU
    earth_x = earth_dist * np.cos(t_vals)
    earth_y = earth_dist * np.sin(t_vals)

    # 3. GÖRSELLEŞTİRME
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    plt.style.use('dark_background')
    
    # --- SOL EKRAN ---
    ax1.set_title("1. GENEL BAKIŞ (Güneş - Dünya - L2)", color='lime')
    ax1.set_xlim(-1.3, 1.3)
    ax1.set_ylim(-1.3, 1.3)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.15)
    
    ax1.plot([0], [0], 'yo', markersize=15, label='Güneş', zorder=2)
    earth_plot_1, = ax1.plot([], [], 'bo', markersize=8, label='Dünya')
    l2_plot_1, = ax1.plot([], [], 'rx', markersize=6, label='L2')
    jwst_plot_1, = ax1.plot([], [], 'o', color='magenta', markersize=4, label='JWST')
    trail_1, = ax1.plot([], [], 'w-', linewidth=0.5, alpha=0.3)
    ax1.legend(loc='lower left', fontsize=8)

    # --- SAĞ EKRAN (OTO-ZOOM) ---
    ax2.set_title("2. HALO YÖRÜNGESİ (Otomatik Ölçekli)", color='cyan')
    
    # LİMİTLERİ BURADA OTOMATİK VERİYORUZ
    # Y ekseni: Hesapladığımız güvenli limit
    ax2.set_ylim(-safe_limit_y, safe_limit_y)
    
    # X ekseni: Dünya'yı (solda) ve Halo'nun sağını kapsayacak şekilde
    left_limit = -l2_dist - 0.005 # Dünya'nın biraz solu
    right_limit = (x_rot.max() - l2_abs) * 1.5 # Halo'nun sağının biraz fazlası
    ax2.set_xlim(left_limit, right_limit)
    
    ax2.set_aspect('equal') # Oran bozulmasın diye kare yapıyoruz
    ax2.grid(True, alpha=0.2)
    
    # Sabitler
    ax2.plot([0], [0], 'rx', markersize=10, markeredgewidth=2, label='L2 (Merkez)', zorder=5)
    earth_rel_x = -l2_dist
    ax2.plot([earth_rel_x], [0], 'bo', markersize=14, label='Dünya', zorder=5)
    ax2.plot([earth_rel_x], [0], 'b.', markersize=35, alpha=0.2)
    ax2.plot([earth_rel_x, 0], [0, 0], 'w--', linewidth=0.5, alpha=0.3)

    # Hareketliler
    jwst_plot_2, = ax2.plot([], [], 's', color='magenta', markersize=7, label='JWST', zorder=10)
    halo_trail, = ax2.plot([], [], 'c-', linewidth=2, alpha=0.8, label='Halo Yörüngesi')

    ax2.legend(loc='lower right', fontsize=9)

    def update(frame):
        # Sol
        e_x, e_y = earth_x[frame], earth_y[frame]
        l2_nx, l2_ny = l2_x_inertial[frame], l2_y_inertial[frame]
        j_x, j_y = jwst_inertial_x[frame], jwst_inertial_y[frame]
        
        earth_plot_1.set_data([e_x], [e_y])
        l2_plot_1.set_data([l2_nx], [l2_ny])
        jwst_plot_1.set_data([j_x], [j_y])
        trail_1.set_data(jwst_inertial_x[:frame], jwst_inertial_y[:frame])
        
        # Sağ
        rel_x = x_rot[frame] - l2_abs
        rel_y = y_rot[frame]
        
        jwst_plot_2.set_data([rel_x], [rel_y])
        halo_trail.set_data(x_rot[:frame] - l2_abs, y_rot[:frame])
        
        return earth_plot_1, l2_plot_1, jwst_plot_1, trail_1, jwst_plot_2, halo_trail

    ani = animation.FuncAnimation(fig, update, frames=len(t_vals), interval=25, blit=False)
    
    print("✅ Limitler hesaplandı ve pencere ona göre açıldı. ŞİMDİ SIĞACAK!")
    plt.show()

if __name__ == "__main__":
    main()