# Diseño de cajas acústicas mediante herramientas de programación en python
## TI02 - ACUS225 - Cajas Acústicas
### Docente: Dr. Rodolfo Venegas
### Alumno: Diego Espejo

***
***

## Indice 
1. Introducción
1. Terminos Relacionados
    
    1. Parametros Thiele-Small
    1. Cajas Simples
        + Caja cerrada
            + Presencia de material poroso
        + Reflectores de bajo
            + Presencia de material poroso
            + Red de 2 puertos para un gabinete con reflector de bajos
                + Tipo 1.[2]
                + Tipo 2.[2]
        + Gabinete de linea de transmisión

1. Paquete `loudspeaker_box`
    1. `main`
    1. `closed_box`
    1. `JCAL`
    1. `utils`
    1. `mediciones`
1. Glosario de simbolos
1. Referencias Bibliograficas


## Introducción

+ Ya sea para

## Terminos Relacionados



### Caja Cerrada



## Paquete `loudspeaker_box`

        Disclaimer: Este paquete trabaja con la base de datos de VituixCAD

### `main`

|```class closed_box_simple:```| Descripción |
|----------------------------------|-|
|``` __init__(self,df)```| Inicialización de datos de altavoz. |
|```parametros_TS(self,Qtc=0.7071)``` | Extracción de parametros de Thiele-Small. |
|```dimensiones(self,d=None)``` | Definición de dimensiones de la caja cerrada. |
|``` impedancias(self)```| Calculo de impedancias |
|```NPS_m(self,r=1)```| Estimación de Nivel de presión sonora, por defecto a 1 metro |


|```class closed_box```| Descripción |
|----------------------|-------------|
|```__init__(self,df,phi,kappa0,theta0,alpha,lambda_ups,lambda_t)```| Inicialización de datos de altavoz y parametros de material porosos. |
|```parametros_TS(self,Qtc=0.7071)```| Extracción de parametros de Thiele-Small. |
|```dimensiones(self,d=None)```| Definición de dimensiones de la caja cerrada. |
|```JCAL(self)```| Consideración de material poroso mediante metodo JCAL.  |
|```impedancias(self)```| Calculo de impedancias. |
|```NPS_m(self,r=1)```| Estimación de Nivel de presión sonora, por defecto a 1 metro. |


| Función | Descripción |
|---------|-------------|
|```dataset(xls="Dataset_VituixCaD.xls")```| Lectura de base de datos. |


### `closed_box`

| Impedancias | Descripción |
|---------|-------------|
| `ZE(w,Re,Le,f_s,BL,RMS,QMS)` | Impedancia electrica a partir de parametros TS. |
| `Z_MD(w,R_ms,M_md,C_ms)` | Impedancia mecanica de radiación. |
| `Z_r(k0,Z0,a)` | Impedancia de radiación. |
| `Z_ab(Z0,k0,kc,lx,ly,lz,d,Zc=None,poro=False)` | Impedancia acústica de la caja. |
| `Z_e(w,Le,Re,BL,Z_MD,SD,Z_AB,Z_r)` | Impedancia electrica a partir de las otras impedancias. |


| Otros | Descripción |
|---------|-------------|
| `u_hat_c(p_out6,Z_AB)` | Velocidad de volumen. |
| `u_hat_ref(w,eg,BL,Sd,Mms,Re)` | Velocidad de volumen referencial. |
| `p_hat(w,u_hat_c,Vb,r)` | Presion sonora en campo lejano a distancia `r`. |
| `Bl(Re,ws,Qes,Qms)` | Producto entre la densidad de flujo magnetico y la longitud del cable mediante parametros TS. |
| `a(Sd)` | Radio efectivo del diafragma. |
| `RMS(BL,QES,RE,QMS)` | Resistencia mecanica de la suspensión. |
| `MMD(MMS,a)` | Masa mecanica del diafragma. |
| `Vb(Vas,Qtc,Qts)` | Volumen de la caja. |
| `p_out(w,Sd,BL,Z_e,Z_MD,Z_ab,Z_r,r=1)` | Presión de salida de la caja acústica. |
| `NPS_pref(w,u_hat_ref,r=1,pref=20e-6)` | Nivel de presion sonora de referencia. |

### `JCAL`

| Función | Descripción |
|---------|-------------|
| `X_Omega(w,X0,w_bar,M)` | Función de escalamiento. |
| `kappa_omega(w,phi,kappa0,alpha,lambda_ups)` | Permeabilidad dinamica viscosa. |
| `theta_omega(w,phi,theta0,lambda_t)` | Permeabilidad dinamica termica. |
| `C_omega` | Compresibilidad efectiva dinamica. |
| `Z_c(w,kappa_omega,C_omega)` | Impedancia caracteristica. |
| `c_w(w,kappa_omega,C_omega` | Velocidad del sonido del material poroso. |
| `k_c(w,c_w)` | Numero de onda en el material poroso. |

### `utils`

| Función | Descripción |
|---------|-------------|
| `k0(w)` | Numero de onda en el aire |
| `Z0()` | Impedancia caracteristica del aire |
| `NPS(p,pref=20e-6)` | Nivel de presión sonora |


### `mediciones`

| Función | Descripción |
|---------|-------------|
| `extraer_mediciones(filename)` | Extracción de datos de medicion de impedancia |
| `resonancia(data,mag_impedancia)` | Frecuencia y valor de resonancia mediante valores de impedancia |
| `bandwith(mag_impedancia,frecuency,threshold=12)` | Ancho de banda de la frecuencia de sampleo |
| `parametros_TS(imped_elec_mag,frecuency,f_s,f_1,f_2,Q,r_e,LE,masa)` | Parametros Thiele-Small mediante valores de medicion de impedancia |


## Referencias Bibliograficas

1. Beranek, L. L., & Mellow, T. (2012). Acoustics: sound fields and transducers. Academic Press.

1. Berkhoff, A. P. (1994). Impedance analysis of subwoofer systems. Journal of the Audio Engineering Society, 42(1/2), 4-14.

1. Venegas,R. (2020). Presentaciones del curso Cajas Acústicas,
Universidad Austral de Chile.
