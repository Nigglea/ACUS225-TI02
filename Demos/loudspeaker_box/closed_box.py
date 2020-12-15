### closed_box.py

import numpy as np
import scipy.special as sp
from loudspeaker_box import utils

## Impedancias

def ZE(w,Re,Le,f_s,BL,RMS,QMS):
    ### impedancia de entrada o electrica ###
    ### a partir de parametros TS ###
    ws= 2*np.pi*f_s
    wws=w/ws
    wws2=wws**2
    jq = (1.j)/QMS
    jqww = jq*wws
    Z_E = Re+(w*Le*1.0j) + ((BL**2)/RMS)*np.divide(jqww,1-(wws2)+jqww)

    return Z_E

def Z_MD(w,R_ms,M_md,C_ms):
    ### impedancia mecanica ###
    
    Z_MD = R_ms + w*M_md*1.0j + np.divide(1,w*C_ms*1.0j)
    return Z_MD

def Z_r(k0,Z0,a):
    ### impedancia de radiación ###
    

    Z0 = utils.Z0()
    k0a = k0*a
    J = sp.jv(1,2*k0a)
    H = sp.struve(1,2*k0a)
    Rr = np.multiply(Z0,(1-np.divide(J,k0a)))
    Xr = Z0*np.divide(H,k0a)
    Z_r = Rr+np.multiply(Xr,1.0j)
    return Z_r

def Z_ab(Z0,k0,kc,lx,ly,lz,d,Zc=None,poro=False):
    ###Impedancia acústica ###
    
    if poro==True:
        ### con material poroso ###
        Zwa = -np.divide(Z0,(np.tan(k0*lz)))*1.0j
        Zwp = -np.divide(Zc,np.tan(kc*d))*1.0j
        l = 1/(lx*ly)
        Z_ab = l*np.divide(Zwa*Zwp+np.power(Z0,2),Zwp+Zwa)
    else:
        Z_ab = -np.divide(np.divide(Z0,lx*ly),np.tan(k0*(lz+d)))*1.0j
    return Z_ab

def Z_e(w,Le,Re,BL,Z_MD,SD,Z_AB,Z_r):
    ### impedancia de la bobina ###
    ### a partir de la matriz de transferencia ###
    Z_E = Re+(w*Le*1.0j) 
    div = Z_MD+(Z_AB+Z_r)*SD**2
    Z_e = Z_E + (BL**2)/div
    return Z_e



## Otros

def u_hat_c(p_out6,Z_AB):
    ### velocidad de volumen con presencia de material poroso ###
    u_hat_c = np.divide(p_out6,Z_AB)
    return u_hat_c

def u_hat_ref(w,eg,BL,Sd,Mms,Re):
    u_hat_ref = (eg*BL*Sd)/(w*Mms*Re)
    return u_hat_ref

def p_hat(w,u_hat_c,Vb,r):
    ### presion sonora en campo lejano a distancia r ###
    rho0 = 1.2041 #densidad del aire kg/m^3
    k0 = utils.k0(w)
    # R = (3*Vb/4*np.pi)**(1/3)
    p = -rho0*w*u_hat_c*np.divide(np.exp(-k0*r*1.0j),4*np.pi*r)*1.0j
    return p

def Bl(Re,ws,Qes,Qms):
    ### Producto entre la densidad de flujo magnetico y la longitud del cable 
    ### mediante parametros TS 
    
    Bl=np.sqrt(np.divide(Re,ws*Qes*Qms))
    return Bl

def a(Sd):
    ### Radio efectivo del diafragma
    a = np.sqrt(Sd/np.pi) 
    return a

def RMS(BL,QES,RE,QMS):
    BL2=BL**2
    RMS = (BL2*QES)/(RE*QMS)
    return RMS

def MMD(MMS,a):
    ### Masa mecanica ###
    rho0 = 1.2041 #densidad del aire kg/m^3
    MMD = MMS - 2*(8*rho0*np.power(a,3))/3
    return MMD

def Vb(Vas,Qtc,Qts):
    Vb = Vas/((Qtc/Qts)**2+1)
    return Vb


def p_out(w,Sd,BL,Z_e,Z_MD,Z_ab,Z_r,r=1):
    eg = 2.83 #volts
    rho0 = 1.2041 #densidad del aire kg/m^3
    k0 = utils.k0(w)
    num1 = -1.0j*rho0*Sd*eg*np.exp(-1.0j*k0*r)
    div1 = 4*np.pi*r*BL
    div2 = 1 + (Z_e/BL**2)*(Z_MD+(Z_ab+Z_r)*Sd**2)
    p_out = np.divide(num1,div1) * np.divide(w,div2)
    return p_out

def NPS_pref(w,u_hat_ref,r=1,pref=20e-6):
    rho0 = 1.2041 #densidad del aire kg/m^3
    k0 = utils.k0(w)
    num = np.abs(-(1.j)*rho0*w*u_hat_ref*(np.exp(-1.j*k0*r)/(4*np.pi*r)))
    NPS_pref = 20*np.log10(num/pref)
    return NPS_pref
