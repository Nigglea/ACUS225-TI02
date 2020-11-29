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
    1. `measurements`
1. Glosario de simbolos
1. Referencias Bibliograficas


## Introducción

+ Ya sea para

## Terminos Relacionados



### Caja Cerrada



## Paquete `loudspeaker_box`

        Disclaimer: Este paquete trabaja con la base de datos de VituixCAD

### `main`

|```class closed_box_simple:```| |
|----------------------------------|-|
|``` __init__(self,df)```| |
|```parametros_TS(self,Qtc=0.7071)``` | |
|```dimensiones(self,d=None)``` | |
|``` impedancias(self)```| |
|```NPS_m(self,r=1)```| |


|```class closed_box```| |
|----------------------|-|
|```__init__(self,df,phi,kappa0,theta0,alpha,lambda_ups,lambda_t)```| |
|```parametros_TS(self,Qtc=0.7071)```| |
|```dimensiones(self,d=None)```| |
|```JCAL(self)```| |
|```impedancias(self)```| |
|```NPS_m(self,r=1)```| |

| | |
|--------|-|
|```dataset(xls="Dataset_VituixCaD.xls")```| |

## Referencias Bibliograficas

1. Beranek, L. L., & Mellow, T. (2012). Acoustics: sound fields and transducers. Academic Press.

1. Berkhoff, A. P. (1994). Impedance analysis of subwoofer systems. Journal of the Audio Engineering Society, 42(1/2), 4-14.

1. Venegas,R. (2020). Presentaciones del curso Cajas Acústicas,
Universidad Austral de Chile.
