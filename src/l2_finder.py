import numpy as np

def solve_l2_position(mu):
    """
    Newton-Raphson yöntemi ile L2 Lagrange noktasının konumunu bulur.
    """
    # Başlangıç tahmini
    r = (mu / 3)**(1/3) 
    
    # İterasyon ayarları
    tolerance = 1e-12
    max_iter = 100
    
    for i in range(max_iter):
        # Euler'in 5. Derece Denklemi
        f_val = (r**5 + (3-mu)*r**4 + (3-2*mu)*r**3 - mu*r**2 - 2*mu*r - mu)
        # Türevi
        df_val = (5*r**4 + 4*(3-mu)*r**3 + 3*(3-2*mu)*r**2 - 2*mu*r - 2*mu)
        
        if abs(f_val) < tolerance:
            return r
        
        r = r - f_val / df_val
        
    return r