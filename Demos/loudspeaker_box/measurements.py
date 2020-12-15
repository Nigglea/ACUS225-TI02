# measurements.py

import numpy as np
import pandas as pd
from loudspeaker_box import utils

def read_measurements(filename):
    data = pd.read_csv( filename,sep='\t', header=0, names=['Freq', 'Impedance', 'Phase'])
    mag_impedance = data['Impedance'].to_numpy()
    phase = data['Phase'].to_numpy()
    impedancia = mag_impedance * np.exp(1.j * phase)
    data.insert(3, "Impedancia", impedancia, True)
    return data,mag_impedance, impedancia, phase

def resonance(data,mag_impedance):
    imped_elec_mag = data['Impedance'].to_numpy()
    frequency = data['Freq'].to_numpy()
    f_s = round(frequency[np.argmax(imped_elec_mag[frequency < 8000])],2)
    r_e = round(mag_impedance[0],2)
    z_s = round(np.max(imped_elec_mag[frequency < 8000]), 2)


    print("R_e = " + str(r_e) + ' ohms')
    print("f_s = " + str(f_s) + ' Hz')
    print("Impedancia de la frec de resonancia: " + str(z_s) + ' ohms.')
    return imped_elec_mag,frequency,f_s,r_e,z_s

def bandwith(mag_impedance,frequency,threshold=12):

    freq_under_threshold = mag_impedance < threshold
    above_threshold = [v_idx for v_idx, v in enumerate(freq_under_threshold[frequency < 4000]) if v == False]
    

    f_1 = frequency[above_threshold[0] - 1]
    f_2 = frequency[above_threshold[-1] + 1]
    Q = f_2 - f_1
    print("f_1 = " + str(round(f_1, 2))+' Hz')
    print("f_2 = " + str(round(f_2, 2))+' Hz')
    print("Q = " + str(round(Q, 2)))
    return f_1,f_2,Q,above_threshold

def TS_parameters(imped_elec_mag,frequency,f_s,f_1,f_2,Q,r_e,LE,mass):
    
    r_0 = np.max(imped_elec_mag[frequency < 8000])/(round(r_e, 2))
    r_1 = np.sqrt(r_0) 
    a = (2*np.pi*f_s)**2
    rad = 0.0889
    rho0 = 1.18
    c0 = 344
    w_s = 2*np.pi*f_s
    f = f_2/f_1
    f_cuad = f**2 
    w_s2 = w_s**2

    #TS
    QMS = (f_s*r_1)/(Q)
    QES = (QMS)/(r_0-1)
    R_ES = (r_e)*(r_0-1)
    CMES = (QMS)/((w_s*R_ES)) #farads
    if LE==None:
        LE = 1/(a*CMES)
    BL = np.sqrt(LE/CMES) #ohm
    RMS = BL**2/R_ES #ohm
    SD = rad**2*np.pi
    MMS = mass/(f_cuad -1)
    MAS = MMS/SD**2
    w_mas = w_s2*MAS
    CAS = 1/w_mas
    VAS = CAS*rho0*(c0**2) 

    #print values
    print('Re =',r_e,'Ohms')
    print('Q_es =',round(QES,2))
    print('Q_ms =',round(QMS,2))
    print('fs = ',round(f_s,2),'Hz')
    print('BL = ',round(BL,1),'T*m')
    print('R_ms =',round(RMS,2),'Ohms')
    print('SD =',round(SD,4),'m^2')
    print('V_AS =',round(VAS,3),'m^3')

    return QMS,QES,R_ES,CMES,BL,RMS,SD,VAS
