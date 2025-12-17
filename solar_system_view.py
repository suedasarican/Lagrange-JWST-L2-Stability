import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src.l2_finder import solve_l2_position
from src.simulation import run_mission_simulation

# --- AYARLAR ---
M_EARTH = 5.972e24
M_SUN = 1.989e30
MU = M_EARTH / (M_SUN + M_EARTH)

# GÖRSEL HİLE (ÖNEMLİ!):
# Gerçek ölçekte çizersek James Webb, Güneş'in yanında toz zerresi gibi kalır.
# Görselde "Spiral" hareketi görebilmek için L2 mesafesini ve Halo yörüngesini
# biraz abartarak (büyüterek) çiziyoruz ki gözüksün.
EXAGGERATION_FACTOR = 150 # Görünürlük için 150 kat büyütme

def rotate_coordinates(x_rot, y_rot, t):
    """
    Dönen Çerçeveden (Rotating Frame) -> Sabit Çerçeveye (Inertial Frame) Geçiş.
    Bu matematiksel işlem, L2'ye sabitlenmiş kamerayı GÜNEŞ'e sabitler.
    """
    # Dönüş Matrisi (Rotation Matrix)
    x_inertial = x_rot * np.cos(t) - y_rot * np.sin(t)
    y_inertial = x_rot * np.sin(t) + y_rot * np.cos(t)
    return x_inertial, y_inertial

def main():
    print("--- GÜNEŞ SİSTEMİ BÜYÜK RESİM SİMÜLASYONU ---")
    
    # 1. Önce Halo Yörüngesini Hesapla (Eski bildiğimiz işlem)
    l2_dist = solve_l2_position(MU)
    l2_abs = (1 - MU) + l2_dist
    
    # Başlangıç (Hafif kaydırılmış L2 konumu)
    start_state = np.array([l2_abs - 0.002, 0.0, 0.0, 0.012])
    
    # Simülasyon (Yaklaşık 1 tam yıl = 2*pi süresince)
    print("-> Yörünge verisi üretiliyor...")
    duration = 2 * np.pi * 0.8 # 0.8 Yıl
    dt = 0.01
    x_rot, y_rot = run_mission_simulation(MU, start_state, duration=duration, dt=dt)
    
    # Zaman dizisi
    t_vals = np.linspace(0, duration, len(x_rot))

    # 2. Koordinat Dönüşümü (Dönen -> Sabit)
    # Burada "Abartı Faktörü"nü kullanarak hareketi görünür kılıyoruz.
    
    # Güneş (Merkez)
    sun_x, sun_y = 0, 0
    
    # Dünya'nın Hareketi (1 AU yarıçaplı çember)
    earth_x = np.cos(t_vals) * (1 - MU)
    earth_y = np.sin(t_vals) * (1 - MU)
    
    # James Webb'in Halo Hareketi (L2 etrafındaki yerel hareket)
    # Önce L2 merkezli hale getiriyoruz:
    jwst_local_x = (x_rot - l2_abs) * EXAGGERATION_FACTOR
    jwst_local_y = y_rot * EXAGGERATION_FACTOR
    
    # Şimdi bu yerel hareketi, dönen Dünya'nın ucuna ekliyoruz
    # L2 noktası da Dünya ile beraber dönüyor:
    l2_orbit_radius = (1 - MU) + l2_dist
    l2_inertial_x = l2_orbit_radius * np.cos(t_vals)
    l2_inertial_y = l2_orbit_radius * np.sin(t_vals)
    
    # Dönüşü uygula (Spiral Etkisi İçin)
    jwst_spiral_x = l2_inertial_x + (jwst_local_x * np.cos(t_vals) - jwst_local_y * np.sin(t_vals))
    jwst_spiral_y = l2_inertial_y + (jwst_local_x * np.sin(t_vals) + jwst_local_y * np.cos(t_vals))

    # 3. ANİMASYON KURULUMU
    print("-> Animasyon hazırlanıyor...")
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.style.use('dark_background')
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    ax.set_title("James Webb'in Gerçek Uzay Hareketi\n(Hem Güneş Etrafında, Hem L2 Etrafında Dönüş)", fontsize=14)

    # Çizilecek Nesneler
    sun_dot, = ax.plot([0], [0], 'yo', markersize=20, label='Güneş') # Güneş
    earth_dot, = ax.plot([], [], 'bo', markersize=10, label='Dünya') # Dünya
    path_line, = ax.plot([], [], 'c-', linewidth=1.5, alpha=0.8, label='JWST Yörüngesi (Spiral)') # İz
    jwst_dot, = ax.plot([], [], 'ws', markersize=5, label='James Webb') # Uydu

    ax.legend(loc='upper right')
    
    # Animasyon Fonksiyonu
    def update(frame):
        # Dünya Konumu
        earth_dot.set_data([earth_x[frame]], [earth_y[frame]])
        
        # JWST Konumu
        jwst_dot.set_data([jwst_spiral_x[frame]], [jwst_spiral_y[frame]])
        
        # JWST'nin geride bıraktığı iz (Trail)
        # Sadece son 50 kareyi değil, başından beri olan tüm izi çizelim ki spiral görünsün
        path_line.set_data(jwst_spiral_x[:frame], jwst_spiral_y[:frame])
        
        return earth_dot, jwst_dot, path_line

    ani = animation.FuncAnimation(fig, update, frames=len(t_vals), interval=20, blit=True)
    
    print("✅ Animasyon oynatılıyor! (Pencere açılacak)")
    plt.show()

if __name__ == "__main__":
    main()