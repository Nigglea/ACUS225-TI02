## open_box.py ##

import numpy as np 
import scipy.signal as sp
from loudspeaker_box import utils


def QTS(QES,QMS):
    return (QES*QMS)/(QMS+QES)

def S_p(a_p):
    # area efectiva del puerto
    return np.pi*a_p**2

def a_2(S_p):
    # radio efectivo del puerto
    return np.sqrt(S_p/np.pi)

def M_aT(S_p,t):
    #masa acústica total del puerto
    rho0 = 1.2041 #densidad del aire kg/m^3
    r_s = rho0/S_p
    M_aT = r_s*(t+0.84*np.sqrt(S_p))
    return M_aT

def C_ab(V_ab):
    # compliancia acústica de la caja
    rho0 = 1.2041 #densidad del aire kg/m^3
    c0 = 343.23 #velocidad del sonido
    return V_ab/(rho0*c0**2)

def w_B(M_aT,C_ab):
    #frecuencia angular de resonancia de la caja
    return 1/np.sqrt(M_aT*C_ab)

def RAL(w_b,C_ab,QL=7):
    # Resistencia a fugas acústicas
    return QL/(w_b*C_ab)

class Gs:
    # Funcion de respuesta en frecuencia
    def __init__(self,w,w_s,w_b,QTS,QL,VAS,V_ab):
        self.w_s  = w_s
        self.w_b  = w_b 
        self.QTS  = QTS
        self.QL   = QL
        self.VAS  = VAS
        self.V_ab = V_ab
        self.jw   = w*1.j 

    def p_0(self):
        self.p0 = self.w_s**2*self.w_b**2
        
    def p_1(self):
        self.p1 = (self.w_s*self.w_b**2)/self.QTS + (self.w_b*self.w_s**2)/self.QL

    def p_2(self):
        self.p2 = (1+self.VAS/self.V_ab)*self.w_s**2 + self.w_b**2 + self.w_s*self.w_b / (self.QTS*self.QL)

    def p_3(self):
        self.p3 = self.w_s/self.QTS + self.w_b/self.QL

    def G_s(self):
        self.p_0()
        self.p_1()
        self.p_2()
        self.p_3()
        self.G_S = (self.jw**4)/((self.jw**4) + self.p3*(self.jw**3)+self.p2*(self.jw**2)+self.p1*self.jw + self.p0)

    def mag_G_s(self):
        self.G_s()
        self.mag_G = np.abs(self.G_S)

class NPS_m:
    # Nivel de presión sonora
    def __init__(self,BL,Sd,RE,MMS,r=1):
        self.BL  = BL
        self.Sd  = Sd
        self.RE  = RE
        self.MMS = MMS
        self.r   = r
        self.rho = 1.2041 #densidad del aire kg/m^3

    def Ps(self):
        self.PS = 2*np.pi*self.BL*self.Sd*self.rho/(self.RE*self.MMS*4*np.pi*self.r)

    def N_PS(self,mag_G):
        self.Ps()
        self.NP_S = 20*np.log10(self.PS*mag_G/20e-6)

class Z_e:
    #impedancia electrica
    def __init__(self,w,w_b,w_s,QMS,QES,QL,VAS,V_ab,RE):
        self.w_b  = w_b
        self.w_s  = w_s
        self.QMS  = QMS
        self.QES  = QES
        self.QL   = QL
        self.VAS  = VAS
        self.V_ab = V_ab 
        self.RE   = RE
        self.jw   = w*1.j

    def E_0(self):
        self.E0 = (self.w_s**2)*(self.w_b**2)

    def E_1(self):
        self.E1 = (self.w_s*self.w_b**2)/self.QMS + (self.w_b*self.w_s**2)/self.QL 

    def E_2(self):
        self.E2 = (1 + self.VAS/self.V_ab)*self.w_s**2 + self.w_b**2 + self.w_s*self.w_b/(self.QMS*self.QL)

    def E_3(self):
        self.E3 = self.w_s/self.QMS + self.w_b/self.QL

    def ZE(self):
        self.E_0()
        self.E_1()
        self.E_2()
        self.E_3()
        self.Ze = self.RE*(1+(self.jw*self.w_s/self.QES)*(self.jw**2 + (self.w_b/self.QL)*self.jw + self.w_b**2)/(self.jw**4+self.E3*self.jw**3+self.E2*self.jw**2+self.E1*self.jw+self.E0))

    def mag_ZE(self):
        self.ZE()
        self.mag_Ze = np.abs(self.Ze)

  