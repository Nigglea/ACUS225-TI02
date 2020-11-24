### main.py

from loudspeaker_box import utils, closed_box, JCAL
import numpy as np
import pandas as pd

np.seterr(all='warn')

class closed_box_poro:
    def __init__(self,df,phi,kappa0,theta0,alpha,lambda_ups,lambda_t):
        self.df = df
        self.phi = phi
        self.kappa0=kappa0
        self.theta0=theta0
        self.alpha = alpha
        self.lambda_ups = lambda_ups
        self.lambda_t = lambda_t
        self.w = 2*np.pi*np.linspace(1,20050, num=44100)
        self.k0= utils.k0(self.w)
        self.fs = self.df['fs [Hz]']
        

    def parametros_TS(self,Qtc=0.7071):
        self.Re = self.df['Re [ohm]']
        self.Le = self.df['Le [mH]']/1000
        self.R_ms = self.df['Rms [Ns/m]']
        self.C_ms = self.df['Cms [mm/N]']/1000.
        self.Mms = self.df['Mms [g]']/1000
        self.Sd = self.df['Sd [cm^2]']/10000.
        self.a = closed_box.a(self.Sd)
        self.M_md = closed_box.MMD(self.Mms,self.a)
        self.BL = self.df['BL [Tm]']
        self.Vas = self.df['Vas [L]']/1000.
        self.Qts = self.df['Qts']
        self.Qms = self.df['Qms']
        #Q_tc Butterworth
        self.Vb = closed_box.Vb(self.Vas,Qtc,self.Qts)
        

    def dimensiones(self,d=None):
        l = np.float_power(self.Vb*2,1/3)
        self.lx=l
        self.ly=l
        self.ld=l/2
        if d ==None:
            self.d=self.ld*0.2
        else:
            self.d=d
        self.lz=(self.ld-self.d)
        

    def JCAL(self):
        self.kappa_omega = JCAL.kappa_omega(self.w,self.phi,self.kappa0,self.alpha,self.lambda_ups)
        self.theta_omega = JCAL.theta_omega(self.w,self.phi,self.theta0,self.lambda_t)
        self.C_omega = JCAL.C_omega(self.w,self.phi,self.theta_omega)
        c_w = JCAL.c_w(self.w,self.kappa_omega,self.C_omega)
        self.k_c = JCAL.k_c(self.w,c_w)
        
    def impedancias(self):
        Z0 = utils.Z0()
        Z_c = JCAL.Z_c(self.w,self.kappa_omega,self.C_omega)
        self.Z_E = closed_box.Z_E(self.w,self.Re,self.Le)
        self.Z_MD = closed_box.Z_MD(self.w,self.R_ms,self.M_md,self.C_ms)
        self.Z_r = closed_box.Z_r(self.k0,Z0,self.a)
        self.Z_ab = closed_box.Z_ab(Z0,self.k0,self.k_c,self.lx,self.ly,self.lz,self.d,Z_c,poro=True)
        self.Z_e = closed_box.Z_e(self.Z_E,self.BL,self.Z_MD,self.Sd,self.Z_ab,self.Z_r)
        
    def matrices_de_transferencia(self):
        self.C,n = closed_box.C(self.Z_E)
        self.E = closed_box.E(self.BL,n)
        self.D = closed_box.D(self.Z_MD,n)
        self.M = closed_box.M(self.Sd,n)
        self.F = closed_box.F(self.Z_r,n)
        self.B = closed_box.B(self.Z_ab,n)
        self.A = closed_box.A(self.C,self.E,self.D,self.M,self.F,self.B)

    def NPS_1m(self):
        eg =2.83
        self.p_out6 = closed_box.p_out(self.w,self.Sd,self.BL,self.Z_e,self.Z_MD,self.Z_ab,self.Z_r,r=1)
        self.u_ref = closed_box.u_hat_ref(self.w,eg,self.BL,self.Sd,self.Mms,self.Re)
        self.NPS_ref = closed_box.NPS_pref(self.w,self.u_ref)
        self.NPS = utils.NPS(self.p_out6)
        self.NPS_n = self.NPS-self.NPS_ref
    
class closed_box_simple:
    def __init__(self,df):
        self.df = df
        self.w = 2*np.pi*np.linspace(1,20050, num=44100)
        self.k0= utils.k0(self.w)
        self.fs = self.df['fs [Hz]']
        

    def parametros_TS(self,Qtc=0.7071):
        self.Re = self.df['Re [ohm]']
        self.Le = self.df['Le [mH]']/1000
        self.R_ms = self.df['Rms [Ns/m]']
        self.C_ms = self.df['Cms [mm/N]']/1000.
        self.Mms = self.df['Mms [g]']/1000
        self.Sd = self.df['Sd [cm^2]']/10000.
        self.a = closed_box.a(self.Sd)
        self.M_md = closed_box.MMD(self.Mms,self.a)
        self.BL = self.df['BL [Tm]']
        self.Vas = self.df['Vas [L]']/1000.
        self.Qts = self.df['Qts']
        self.Qms = self.df['Qms']
        #Q_tc Butterworth
        self.Vb = closed_box.Vb(self.Vas,Qtc,self.Qts)
        

    def dimensiones(self,d=None):
        l = np.float_power(self.Vb*2,1/3)
        self.lx=l
        self.ly=l
        self.ld=l/2
        if d ==None:
            self.d=self.ld*0.2
        else:
            self.d=d
        self.lz=(self.ld-self.d)
        
        
    def impedancias(self):
        Z0 = utils.Z0()
        self.Z_E = closed_box.Z_E(self.w,self.Re,self.Le)
        self.Z_MD = closed_box.Z_MD(self.w,self.R_ms,self.M_md,self.C_ms)
        self.Z_r = closed_box.Z_r(self.k0,Z0,self.a)
        self.Z_ab = closed_box.Z_ab(Z0,self.k0,None,self.lx,self.ly,self.lz,self.d,poro=False)
        self.Z_e = closed_box.Z_e(self.Z_E,self.BL,self.Z_MD,self.Sd,self.Z_ab,self.Z_r)
        
    def matrices_de_transferencia(self):
        self.C,n = closed_box.C(self.Z_E)
        self.E = closed_box.E(self.BL,n)
        self.D = closed_box.D(self.Z_MD,n)
        self.M = closed_box.M(self.Sd,n)
        self.F = closed_box.F(self.Z_r,n)
        self.B = closed_box.B(self.Z_ab,n)
        self.A = closed_box.A(self.C,self.E,self.D,self.M,self.F,self.B)

    def NPS_1m(self):
        eg =2.83
        self.p_out6 = closed_box.p_out(self.w,self.Sd,self.BL,self.Z_e,self.Z_MD,self.Z_ab,self.Z_r,r=1)
        self.u_ref = closed_box.u_hat_ref(self.w,eg,self.BL,self.Sd,self.Mms,self.Re)
        self.NPS_ref = closed_box.NPS_pref(self.w,self.u_ref)
        self.NPS = utils.NPS(self.p_out6)
        self.NPS_n = self.NPS-self.NPS_ref

def dataset(xls="Dataset_VituixCaD.xls"):
    dataset = pd.read_excel(xls)
    dataset = dataset.set_index(["Manufacturer","Model"])
    return dataset