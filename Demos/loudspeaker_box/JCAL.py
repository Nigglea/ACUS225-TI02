### JCAL.py

import numpy as np
import math


def X_omega(w,X0,w_bar,M):
    ### funcion de escalamiento ###
    W = np.multiply(np.divide(w,w_bar),1.0j)
    X_omega = X0*np.float_power(W + np.sqrt([1+W*(M/2)]),-1)
    return X_omega

def kappa_omega(w,phi,kappa0,alpha,lambda_ups):
    ### permeabilidad dinamica viscosa ###
    
    eta = 1.74e-5 #viscosidad dinamica del aire Pa*s
    rho0 = 1.2041 #densidad del aire kg/m^3
    M_ups = (8.*kappa0*alpha)/(phi*lambda_ups**2)
    w_ups = (phi*eta)/(rho0*kappa0*alpha)
    kappa_omega = X_omega(w,kappa0,w_ups,M_ups)
    return kappa_omega
    
def theta_omega(w,phi,theta0,lambda_t):
    ### permeabilidad dinamica termica ###
    
    k = 0.024 #conduccion termica del aire W/(m*K)
    rho0 = 1.2041 #densidad del aire kg/m^3
    cp = 1000. #calor especifico del aire J/(kg*ºC)
    M_t = np.divide((8.*theta0),(phi*lambda_t**2))
    w_t = (phi*k)/(rho0*cp*theta0)
    theta_omega = X_omega(w,theta0,w_t,M_t)
    return theta_omega

def C_omega(w,phi,theta_omega):
    ###### Compresibilidad efectiva dinamica ######
    
    gamma = 1.4 #razon de calores especificos aire
    cp = 1000. #calor especifico del aire J/(kg*ºC)
    rho0 = 1.2041 #densidad del aire kg/m^3
    k = 0.024 #conduccion termica del aire W/(m*K)
    P0 = 101325. #[Pa]: Presión de equilibrio
    div_gamma = (gamma-1)/gamma
    t_kphi = np.divide(theta_omega,(k*phi))
    C_omega = (phi/P0)*(1.-np.multiply(w,rho0*cp*div_gamma*t_kphi*1.0j))
    return C_omega

def Z_c(w,kappa_omega,C_omega):
    ### impedancia caracteristica ###
    eta = 1.74e-5 #viscosidad dinamica del aire Pa*s
    Z_c = np.sqrt(eta/(w*kappa_omega*C_omega*1.0j))
    return Z_c

def c_w(w,kappa_omega,C_omega):
    ### velocidad del sonido ###
    eta = 1.74e-5 #viscosidad dinamica del aire Pa*s

    c_w = np.sqrt((w*kappa_omega*1.0j)/(eta*C_omega))
    return c_w
    
def k_c(w,c_w):
    ### numero de onda ###
    k_c=w/c_w
    return k_c