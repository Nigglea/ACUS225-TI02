### utils.py

import numpy as np

def k0(w):
    ### numero de onda en aire ###
    c0 = 343.23 #velocidad del sonido
    k0 = np.divide(w,c0)
    return k0

def Z0():
    ### impedancia caracteristica del aire
    rho0 = 1.2041 #densidad del aire kg/m^3
    c0 = 343.23 #velocidad del sonido
    Z0 = rho0*c0
    return Z0

def NPS(p,pref=20e-6):
    ### Nivel de presion sonora ###
    
    NPS=20*np.log10(np.divide(np.abs(p),pref))
    return NPS