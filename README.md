# 🛰️ James Webb Space Telescope: L2 Lagrange Point Stability Analysis

Bu proje, **MAT353 Nümerik Analiz** dersi kapsamında geliştirilmiştir. 

## 🎯 Projenin Amacı
Kısıtlı Üç Cisim Problemi (CR3BP) modelini kullanarak:
1.  Dünya-Güneş sistemindeki **Lagrange Noktalarının (L1-L5)** konumlarını Nümerik Yöntemlerle (Newton-Raphson) tespit etmek.
2.  **James Webb Uzay Teleskobu'nun (JWST)** bulunduğu L2 noktasının yörünge kararlılığını **Özdeğer Analizi (Eigenvalue Analysis)** ile incelemek.
3.  L2 noktasındaki kararsızlığı (instability) simüle etmek.

## 🛠️ Kullanılan Teknolojiler ve Yöntemler
* **Dil:** Python 3.9+
* **Kütüphaneler:** NumPy, SciPy, Matplotlib
* **Nümerik Yöntemler:** * Kök Bulma: Newton-Raphson Metodu
    * Diferansiyel Denklem Çözümü: Runge-Kutta (RK45)
    * Lineer Cebir: Jacobian Matrisi ve Özdeğer Hesabı

## 🚀 Kurulum
```bash
pip install -r requirements.txt
python src/simulation.py