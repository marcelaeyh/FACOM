#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 18:51:09 2022

@author: luisa
"""

#------------------------------------------------------------------------------

#1. IMPORTAR LIBRERIAS
import pandas as pd
import  numpy as np
import matplotlib.pyplot as plt #Para graficar
from datetime import datetime
import scipy 
from scipy import stats
from scipy import signal
import scaleogram as scg 
import random
from random import gauss
from tqdm import tqdm # libreria para saber el tiempo de ejecución

#------------------------------------------------------------------------------

#2. LECTURA DE DATOS
P1=np.loadtxt("/home/luisa/Escritorio/Semestre_Actual/2. Analisis de datos/T3/pcp_2_mon_1984-2015.txt")
P2=np.loadtxt("/home/luisa/Escritorio/Semestre_Actual/2. Analisis de datos/T3/precip_erai_mon_1980-2015.txt")

#2.1 INFORMACIÓN INICIAL DE LOS ARCHIVOS
n1=len(P1)
n2=len(P2)

print("La longitud de P1=", n1)
print("La longitud de P2=", n2)

# Se selecciona un n que define a ambas muestras
n=n1

# se generan las etiquetas para los años y los meses
ti=1984  #Año inicial
year_st = np.zeros(n)
year_st[0] = ti
for i in range(n-1):
    year_st[i+1] = year_st[i] + 1/12 


meses=np.array(["Ene","Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", 
                "Sep","Oct", "Nov", "Dic"])
#------------------------------------------------------------------------------

#3. FUNCIONES
#3.1 Organizar
def organizarmM(vector):     
    Vector=list(vector)
    for i in range(1,len(Vector)):     # Metodo de incersión
        actual = Vector[i]
        j = i
        #Desplazamiento de los elementos de la matriz }
        while j>0 and Vector[j-1]>actual:
            Vector[j]=Vector[j-1]
            j = j-1
        #insertar el elemento en su lugar
        Vector[j]=actual
    return(Vector)


#3.2 MAD
def mad(vector):
    iqr05=np.quantile(vector, 0.5)
    suma=0
    for i in range(len(vector)):
        av=abs(vector[i]-iqr05)
        suma=suma+av
    me=np.median(suma)
    return(me)

#3.3 SKEWNESS
def skewness(vector):
    media=np.mean(vector)
    n=len(vector)
    desviacionestandar=np.std(vector)
    suma=0
    suma1=0
    for i in range(n):
        suma1=(vector[i]-media)**3
        suma=suma+suma1
    gamma=(((1)/(n-1))*(suma))/(desviacionestandar**3)
    return(gamma)


#3.4 YULE KENDALL
def yulekendall(vector):
    q025=np.quantile(vector,0.25)
    q050=np.quantile(vector,0.5)
    q075=np.quantile(vector,0.75)
    iqr=q075-q025
    gammaYK=(q025- (2*q050) + q075 )/(iqr)
    return(gammaYK)

#3.4 Ciclo Medio Anual
def C1_12(V):
    n=len(V)
    c_iterada=[]
    i=0
    j=0
    print("inicia proceso de crear la columna con los números de los meses")
    for i in range(n):
        if(j>=12):
            j=0
        c_iterada.append(j)
        j=j+1
    #print(c_iterada)       
    df=pd.DataFrame(V)
    df_1=pd.DataFrame(c_iterada)
    d = pd.concat([df, df_1], axis=1)
    d.columns = ['valor','mes']
    CMA=[]
    
    for i in range(0,12):
        suma=0
        count=0
        for index, row in d.iterrows():
            if(row['mes']==i):
                suma=row["valor"]+suma
                count=count+1
        CMA.append(suma/count)
    return(CMA)   

#3.5 Anomalías

def anomaliaJ(vector,CMA):
    n=len(vector)
    cont = 0
    A=np.zeros(n)
    for i in range(n):
        A[i] = (vector[i] - CMA[cont])
        cont = cont + 1

        if cont == 12:
            cont = 0
    return(A)

#3.6 PENDIENTE PARAMETRICA
def pendienteParametrica(vector,Ainicial,Anomalia):
    n=len(vector)
    ti=Ainicial  #Año inicial
    A=Anomalia
    year_st = np.zeros(n)
    year_st[0] = ti
    for i in range(n-1):
        year_st[i+1] = year_st[i] + 1/12 
    
    year_pendiente=year_st

    #Estadisticos
    me_V=np.mean(A)
    M_year_pendiente=np.mean(year_pendiente)
    #Paso 1: crear los  vectores e iniciar las variables
    p1_V=np.zeros(n)
    #pasos de tiempo
    V_dx=0
    dx=0
    V_e=0
    #Paso 2:
    for i in range(n):
        V_dx  = V_dx + (year_pendiente[i] -M_year_pendiente )*(A[i] - me_V)
        dx =  dx + (year_pendiente[i] -M_year_pendiente )**2     
    p2_V = V_dx / dx
    #Paso 3:
    for i in range(n):
        p1_V[i] = p2_V*year_pendiente[i] + (me_V - p2_V * M_year_pendiente)
    #Paso 4:
    for i in range(n):
        V_e = V_e + (A[i] - p1_V[i])**2
    #Paso 5:
    P_V = (p2_V*((dx)**(1/2)))/((1/(n-2))*V_e) # t para la pendiente de P

    return(P_V,p1_V)

#3.7 PENDIENTE NO PARAMETRICA (TENDENCIAS)
def tendencia(Anomalia,Ainicial):
    n=len(Anomalia)
    ti=Ainicial  #Año inicial
    A=Anomalia
    year_st = np.zeros(n)
    year_st[0] = ti
    for i in range(n-1):
        year_st[i+1] = year_st[i] + 1/12 
    
    tam=n
    tp=Anomalia
    año=year_st
    ta = int((tam*(tam - 1))/2)
    bmktp = np.zeros(ta)
    sigtp = np.zeros(ta)
    j = tam - 1
    k = 0
    for i in range(tam):
        while i != j:
            fi = tp[j] - tp[i]
            if fi > 0:
                f = 1
            if 0 > fi:
                f = -1
            if fi == 0:
                f = 0
            sigtp[k] = f
            bmktp[k] = (tp[j] - tp[i])/(año[j] - año[i])
            j = j - 1
            k = k + 1
        j = tam-1
    suma = sum(sigtp)
    g,s,ss,corr  = 0,1,0,0
    pp,tt = np.zeros(ta),np.zeros(ta)
    bmkttp = np.median(bmktp)
    j = tam-1
    for i in range(tam):
        while i != j:
            if tp[i] == tp[j]:
                s = s + 1
            j = j - 1
        if s > 1:
            for k in range(tam):
                if tp[i] == pp[k]:
                    ss = 1
            if ss == 0:
                pp[g] = tp[i]
                tt[g] = s
                g = g + 1
        s,ss = 1,0
        j = tam - 1
    for i in range(g):
        corr = tt[i]*(tt[i] - 1)*(2*tt[i] + 5) + corr
        varS = (1/18)*(tam*(tam - 1)*(2*tam + 5) - corr)

    if suma == 0:
        zmktp = 0

    if suma > 0:
        zmktp = (suma - 1)/((varS)**(1/2))

    if 0 > suma:
        zmktp = (suma + 1)/((varS)**(1/2))
    Zmk=zmktp
    tendencia= bmkttp #Estimado de pendiente
    return(tendencia,Zmk)
#3.8 
def obtenermayorespercentil(anomalia,limitemax,year):
    y=year
    A=anomalia
    n=len(A)
    Lm=limitemax
    percentil=np.percentile(A,Lm)
    atipicos=np.zeros((n,2))
        
    for i in range(n):
        if(A[i]>=percentil):
            atipicos[i][0]=y[i]
            atipicos[i][1]=A[i] 
        else:
            atipicos[i][0]=y[i]
            atipicos[i][1]="Nan"
                            
    return(atipicos,percentil)
#3.9 
def obtenermenorespercentil(anomalia,limitemin,year):
    y=year
    A=anomalia
    n=len(A)
    Lm=limitemin
    percentil=np.percentile(A,Lm)
    atipicos=np.zeros((n,2))
        
    for i in range(n):
        if(A[i]<=percentil):
            atipicos[i][0]=y[i]
            atipicos[i][1]=A[i] 
        else:
            atipicos[i][0]=y[i]
            atipicos[i][1]="Nan"
                            
    return(atipicos,percentil)

#3.10

#La frecuencia del tiempo entre la fecha inicial y final se da con 
# el freq de el pd.date_range, para este caso se da en meses

#El tiempo final debe darse como n+1, por ejemplo, si el año final es 2015, se
#debe poner 2016 para que la función cree los años hasta el 2015
def extraercolumn_Pandas(vector,inicio,final,ti,tf):
    df=pd.DataFrame(vector)
    df["fechas"]=pd.date_range(start=inicio, end=final, freq='M')
    df["fechas_MA"]=pd.to_datetime(df['fechas']).dt.strftime("%m-%Y")
    df["year"]=pd.to_datetime(df['fechas']).dt.year
    df=df.drop(["fechas"], axis=1)
    df=df.drop(["fechas_MA"], axis=1)
    df.columns=["P","year"]
    
    #Creación del vector de años
    t=ti
    y=[]
    while t!=tf :
        y.append(t)
        t=t+1

    #Se crea un vector donde se almacenan los max
    maximos=[]
    
    for i in (y):
        m=df.P[df.year==i]
        m1=np.max(m)
        maximos.append(m1)

    return(maximos,y)

#Autocorrelación
def autocorrelacion(vector):
    A1=[] #Matriz con los valores originales 
    A2=[] #Matriz corrida un espacio, sirve para hacer la autocorrelación
    for i in range(n-1):
        A1.append(vector[i])
        A2.append(vector[i+1])
    M_A1=np.mean(A1)
    M_A2=np.mean(A2)

    #Hallamos ahora la Autocorrelación
    s1, s2, s3 = 0,0,0
    for i in range(n-1):
        s1 = ((vector[i] - M_A1)*(vector[i+1] - M_A2)) + s1
        s2 = (vector[i] - M_A1)**2 + s2
        s3 = (vector[i] - M_A2)**2 + s3
    ro = s1/((s2*s3)**(1/2))
    print('La Autocorrelación de la variable delta es=',ro)
    return(ro)

def AR(mu,fi,n,sigma,xo):
    X=np.zeros(n)
    #print(X)
    X[0]=xo
    for i in range(n-1):
        X[i+1]=mu+(fi*(mu+X[i]))+gauss(0,sigma)
    return(X)



#------------------------------------------------------------------------------


#4. PRIMER EJERCICIO
print("PRIMERA PARTE- ESTADISTICOS")
#(a) Calcule medidas de locación, dispersión y simetría para cada conjunto de datos.

#4.1 MEDIDAS DE LOCACIÓN
print("MEDIDAS DE LOCACIÓN")

#4.1.1 QUANTILES

print("1. QUANTILES")
Q_025_P1=np.quantile(P1, 0.25)
Q_05_P1=np.quantile(P1, 0.5)
Q_075_P1=np.quantile(P1, 0.75)
Q_025_P2=np.quantile(P2, 0.25)
Q_05_P2=np.quantile(P2, 0.5)
Q_075_P2=np.quantile(P2, 0.75)

print(" *Los cuantiles para P1=")
print("   0.25=",Q_025_P1)
print("   0.5=",Q_05_P1)
print("   0.75=",Q_075_P1)

print(" *Los cuantiles para P2=")
print("   0.25=",Q_025_P2)
print("   0.5=",Q_05_P2)
print("   0.75=",Q_075_P2)

#4.1.2 MEDIA
print("2. PROMEDIO")
Me_P1=np.mean(P1)
Me_P2=np.mean(P2)

print(" *El promedio para P1=")
print("   Me_P1=",Me_P1)

print(" *El promedio para P2=")
print("   Me_P2=",Me_P2)

#4.1.3 MEDIANA
print("3. MEDIANA")
Ma_P1=np.median(P1)
Ma_P2=np.median(P2)

print(" *La mediana para P1=")
print("   Ma_P1=",Ma_P1)

print(" *El mediana para P2=")
print("   Me_P2=",Ma_P2)

#4.1.4 TRIMEDIANA
print("4. TRIMEDIA")
Tri_P1=(Q_025_P1+(2*Q_05_P1)+Q_075_P1)/(4)
Tri_P2=(Q_025_P2+(2*Q_05_P2)+Q_075_P2)/(4)

print(" *La trimedia para P1=")
print("   Tri_P1=",Tri_P1)

print(" *La trimedia para P2=")
print("   Tri_P2=",Tri_P2)


#4.2 MEDIDAS DE DISPERSIÓN
print("MEDIDAS DE DISPERSIÓN")

#4.2.1 RANGO
print("5. RANGO")

mM_P1=organizarmM(P1)
mM_P2=organizarmM(P2)
PD_P1=mM_P1[0]
UD_P1=mM_P1[n-1]
PD_P2=mM_P2[0]
UD_P2=mM_P2[n-1]

print(" *El rango para P1=")
print("   El primer dato=",PD_P1)
print("   El último dato=",UD_P1)

print(" *El rango para P2=")
print("   El primer dato=",PD_P2)
print("   El último dato=",UD_P2)

#4.2.2 RANGO INTERQUANTIL [IQR]
print("6. IQR")
IQR_P1=Q_075_P1-Q_025_P1
IQR_P2=Q_075_P2-Q_025_P2

print(" *El rango intercuantil para P1=")
print("   IQR_P1=",IQR_P1)
print(" *El rango intercuantil para P2=")
print("   IQR_P2=",IQR_P2)

#4.2.3 DESVIACIÓN ESTÁNDAR
print("7. DESVIACIÓN ESTÁNDAR")
DES_P1=np.std(P1)
DES_P2=np.std(P2)

print(" *La desviación estpandar para P1=")
print("   desviaciónE P1=",DES_P1)

print(" *La desviación estpandar para P2=")
print("   desviaciónE P2=",DES_P2)

#4.2.4 VARIANZA
print("8. VARIANZA")
VAR_P1=np.var(P1)   
VAR_P2=np.var(P2)

print(" *La varianza para P1=")
print("   Varianza P1=",VAR_P1)

print(" *La varianza para P2=")
print("   Varianza P2=",VAR_P2)
      
#4.2.5 MEDIANA DE LAS DIFERENCIAS ABSOLUTAS [MAD]
print("6. MAD")
MAD_P1= mad(P1)
MAD_P2= mad(P2)

print(" *El MAD para P1=")
print("   MAD P1=",MAD_P1)

print(" *El MAD para P2=")
print("   MAD P2=",MAD_P2)

#4.3 MEDIDAS DE ASIMETRIA
print("MEDIDAS DE ASIMETRÍA")

#4.3.1 SKEWNESS
gamma_P1=skewness(P1)
gamma_P2=skewness(P2)

print(" *El skewness para P1=")
print("   gamma P1=",gamma_P1)

print(" *El skewness para P2=")
print("   gamma P2=",gamma_P2)

#4.3.2 YULE KENDALL
gammaYK_P1=yulekendall(P1)
gammaYK_P2=yulekendall(P2)

print(" *El yule kendall para P1=")
print("   gammayk P1=",gammaYK_P1)

print(" *El yule kendall para P2=")
print("   gammayk P2=",gammaYK_P2)
#------------------------------------------------------------------------------
#5. CICLO MEDIO ANUAL

#5.1 CICLOS MEDIOS ANUALES
CMA_P1=C1_12(P1)
CMA_P2=C1_12(P2)

#5.2 GŔAFICOS
plt.figure(figsize=(10,5))
plt.title("Ciclo Medio Anual - Precipitación", fontsize=15)
#Muestra 1

plt.plot(meses,CMA_P2, color="cornflowerblue",label="P2")
plt.plot(meses,CMA_P1, color="palegreen",label="P1")
#Valores adicionales
plt.axhline(y=Me_P1,color="k",linewidth=1.0,linestyle="--",
            label=("Media_P1",round(Me_P1,3),"mm/día"))
plt.axhline(y=Me_P2,color="k",linewidth=1.3,linestyle=":",
            label=("Media_P2",round(Me_P2,3),"mm/día"))
#Diseño del gráfico
plt.xticks(rotation=90)
plt.legend()
plt.minorticks_on()
plt.ylabel("Precipitación [mm / día ]", fontsize=15)
plt.xlabel("Meses ", fontsize=15)
plt.grid(color='lightgrey', linewidth=1.0)
plt.savefig(
    '/home/luisa/Escritorio/Semestre_Actual/2. Analisis de datos/T3/graficos/CMA'+'.png')

plt.show

print("P2")
print("precipitación junio CMA=",(round(CMA_P2[5],3)))
print("precipitación julio CMA=",(round(CMA_P2[6],3)))
print("precipitación noviembre CMA=",(round(CMA_P2[10],3)))

print("P1")
print("precipitación Abril CMA=",(round(CMA_P1[3],3)))
print("precipitación Mayo CMA=",(round(CMA_P1[4],3)))
print("precipitación enero CMA=",(round(CMA_P1[0],3)))

#5.3 HISTOGRAMAS GRAFICOS

num_bins = 20
plt.figure(figsize=(10,5))
plt.suptitle("Histogramas de Precipitación para ambas muestras P1 y P2"" \n 1984-2015",
             fontsize=15)
plt.subplot(1, 2, 1)
plt.hist(P1, num_bins,facecolor = "palegreen", alpha=0.75,label="P1",edgecolor = "gray")
plt.axvline(x=Me_P1,color="black",linewidth=1.0,linestyle='-',
            label=('Media_P1'))
plt.axvline(x=Ma_P1,color="black",linewidth=1.0,linestyle='--',
            label=('Mediana_P1'))
plt.ylabel("Frecuencia (pr)", fontsize=10)
plt.xlabel("Precipitación [mm/día]", fontsize=10)
#plt.title("Muestra 1")
plt.grid(color='lightgrey',linewidth=1.0)
plt.text(1, 65, 'A', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.minorticks_on()
plt.legend()
plt.subplot(1, 2, 2)
plt.hist(P2, num_bins,facecolor = "cornflowerblue", alpha=0.75,label="P2",
         edgecolor = "steelblue")
plt.axvline(x=Me_P2,color="black",linewidth=1.0,linestyle='-',
            label=('Media_P2'))
plt.axvline(x=Ma_P2,color="black",linewidth=1.0,linestyle='--',
            label=('Mediana_P2'))
plt.ylabel("Frecuencia (pr)", fontsize=10)
#plt.title("Muestra 2")
plt.xlabel("Precipitación [mm/día]", fontsize=10)
plt.grid(color='lightgrey',linewidth=1.0)
plt.text(1, 51.5, 'B', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.minorticks_on()
plt.legend()
plt.savefig(
    '/home/luisa/Escritorio/Semestre_Actual/2. Analisis de datos/T3/graficos/Histogramas'+'.png')
#------------------------------------------------------------------------------
#6. ANOMALÍAS e histogramas

#6.1 ANOMALÍAS
A_P1=anomaliaJ(P1,CMA_P1)

A_P2=anomaliaJ(P2,CMA_P2)
#se crean dos data frame con la información de las anomalais
A_P1_df=pd.DataFrame(A_P1)
A_P2_df=pd.DataFrame(A_P2)



#Se les agrega a ambas una columna con las fechas
inicio='1/1/1984'
final="31/12/2015"
A_P1_df["fechas"]=pd.date_range(start=inicio, end=final, freq='M')
A_P2_df["fechas"]=pd.date_range(start=inicio, end=final, freq='M')
#Se cambia el nombre de las columnas
A_P1_df.columns=["p","fecha"]
A_P2_df.columns=["p","fecha"]
#Convertimos la columna de fecha en datatime
A_P1_df["fechas_MA"]=pd.to_datetime(A_P1_df['fecha']).dt.strftime("%m-%Y")
A_P1_df["year"]=pd.to_datetime(A_P1_df['fechas_MA']).dt.year
A_P1_df["month"]=pd.to_datetime(A_P1_df['fechas_MA']).dt.month

A_P2_df["fechas_MA"]=pd.to_datetime(A_P2_df['fecha']).dt.strftime("%m-%Y")
A_P2_df["year"]=pd.to_datetime(A_P2_df['fechas_MA']).dt.year
A_P2_df["month"]=pd.to_datetime(A_P2_df['fechas_MA']).dt.month



A_P2_df.head()
#Se encuentra la información de interes
AP1_1998=A_P1_df[A_P1_df.year==(2000 and 2001)]
print(AP1_1998)
AP1_2010=A_P1_df[A_P1_df.year==2001]
print(AP1_2010)

AP2_2005=A_P2_df[A_P2_df.year==2008]
print(AP2_2005)
AP1_2006=A_P2_df[A_P2_df.year==2006]
print(AP1_2006)

dato1=A_P1_df[A_P1_df.p== -5.956551406250001]
print(dato1)

dato2=A_P2_df[A_P2_df.p==-10.42020530356243]
print(dato2)

max_P1=A_P1.max()
min_P1=A_P1.min()
print("El maximo valor de las anomalias en P1 es=",max_P1)
print("El mínimo valor de las anomalias en P1 es=",min_P1)

max_P2=A_P2.max()
min_P2=A_P2.min()
print("El maximo valor de las anomalias en P2 es=",max_P2)
print("El mínimo valor de las anomalias en P2 es=",min_P2)
#------------------------------------------------------------------------------
#7. TENDENCIAS

n=len(A_P1)
ti=1984  #Año inicial
A=A_P1
year_st = np.zeros(n)
year_st[0] = ti
for i in range(n-1):
    year_st[i+1] = year_st[i] + 1/12 

tam=n
tp=A_P1
año=year_st
ta = int((tam*(tam - 1))/2)
bmktp = np.zeros(ta)
sigtp = np.zeros(ta)
j = tam - 1
k = 0
for i in range(tam):
    while i != j:
        fi = tp[j] - tp[i]
        if fi > 0:
            f = 1
        if 0 > fi:
            f = -1
        if fi == 0:
            f = 0
        sigtp[k] = f
        bmktp[k] = (tp[j] - tp[i])/(año[j] - año[i])
        j = j - 1
        k = k + 1
    j = tam-1
suma = sum(sigtp)
g,s,ss,corr  = 0,1,0,0
pp,tt = np.zeros(ta),np.zeros(ta)
bmkttp = np.median(bmktp)
j = tam-1
for i in range(tam):
    while i != j:
        if tp[i] == tp[j]:
            s = s + 1
        j = j - 1
    if s > 1:
        for k in range(tam):
            if tp[i] == pp[k]:
                ss = 1
        if ss == 0:
            pp[g] = tp[i]
            tt[g] = s
            g = g + 1
    s,ss = 1,0
    j = tam - 1
for i in range(g):
    corr = tt[i]*(tt[i] - 1)*(2*tt[i] + 5) + corr
    varS = (1/18)*(tam*(tam - 1)*(2*tam + 5) - corr)

if suma == 0:
    zmktp = 0

if suma > 0:
    zmktp = (suma - 1)/((varS)**(1/2))

if 0 > suma:
    zmktp = (suma + 1)/((varS)**(1/2))
Zmk_P1=zmktp
T_P1= bmkttp #Estimado de pendiente

n=len(A_P2)
ti=1984  #Año inicial
A=A_P2
year_st = np.zeros(n)
year_st[0] = ti
for i in range(n-1):
    year_st[i+1] = year_st[i] + 1/12 

tam=n
tp=A_P2
año=year_st
ta = int((tam*(tam - 1))/2)
bmktp = np.zeros(ta)
sigtp = np.zeros(ta)
j = tam - 1
k = 0
for i in range(tam):
    while i != j:
        fi = tp[j] - tp[i]
        if fi > 0:
            f = 1
        if 0 > fi:
            f = -1
        if fi == 0:
            f = 0
        sigtp[k] = f
        bmktp[k] = (tp[j] - tp[i])/(año[j] - año[i])
        j = j - 1
        k = k + 1
    j = tam-1
suma = sum(sigtp)
g,s,ss,corr  = 0,1,0,0
pp,tt = np.zeros(ta),np.zeros(ta)
bmkttp = np.median(bmktp)
j = tam-1
for i in range(tam):
    while i != j:
        if tp[i] == tp[j]:
            s = s + 1
        j = j - 1
    if s > 1:
        for k in range(tam):
            if tp[i] == pp[k]:
                ss = 1
        if ss == 0:
            pp[g] = tp[i]
            tt[g] = s
            g = g + 1
    s,ss = 1,0
    j = tam - 1
for i in range(g):
    corr = tt[i]*(tt[i] - 1)*(2*tt[i] + 5) + corr
    varS = (1/18)*(tam*(tam - 1)*(2*tam + 5) - corr)

if suma == 0:
    zmktp = 0

if suma > 0:
    zmktp = (suma - 1)/((varS)**(1/2))

if 0 > suma:
    zmktp = (suma + 1)/((varS)**(1/2))
Zmk_P2=zmktp
T_P2= bmkttp #Estimado de pendiente
#7.1FORMA PARAMETRICA REGRESIÓN LINEAL CON MC
P_P1,p_P1=pendienteParametrica(P1,1984,A_P1)
P_P2,p_P2=pendienteParametrica(P2,1984,A_P2)
#7.2 MANN-KENDALL

print("La pendiente parametrica para P1=", P_P1)
print("La pendiente parametrica para P2=", P_P2)

print("La tendencia (pendiente no parametrica) para P1=", T_P1)
print("La tendencia (pendiente no parametrica) para P2=", T_P2)

tsen_p1=0.05218143095463007
tsen_p2=4.879464706722665

#7.3 GRAFICOS
plt.figure(figsize=(10,5))
plt.suptitle("Anomalías- Precipitación", fontsize=15)
#Muestra 1
plt.subplot(2, 1, 1)
#plt.ylabel('Common X-Axis', fontsize=15, fontweight='bold')
plt.plot(year_st,A_P1, color="palegreen",label="P1")
#Valores adicionales
plt.plot( year_st, p_P1, color = 'black', alpha=0.8,label="Pendiente_P1")
plt.axhline(y=0,color="midnightblue",linewidth=0.5,linestyle="--")

#Diseño del gráfico
plt.text(1986, 10, 'A', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
#plt.text(1996, -8, '-5.903 mm/día', fontsize = 10)
#plt.text(2008, -8, '-5.654 mm/día', fontsize = 10)
#plt.text(2000, 20, '-5.903 mm/día', fontsize = 10)
plt.xticks(rotation=0)
plt.legend()
plt.minorticks_on()
plt.ylabel("Precipitación [mm / día ]", fontsize=10)
plt.grid(color="lightgray")
plt.ylim(-10,25)
#Muestra 2
plt.subplot(2, 1, 2)
plt.plot(year_st,A_P2, color="cornflowerblue",label="P2")
#Valores adicionales
plt.axhline(y=0,color="midnightblue",linewidth=0.5,linestyle="--")
#texto
plt.plot( year_st, p_P2, color = 'black', alpha=0.8,
         label="Pendiente_P2")
#Diseño del gráfico
plt.text(1986, 15, 'B', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
#plt.text(2005, 26, '25,949 mm/día', fontsize = 10)
#plt.text(1985, -16, ' -12,795 mm/día', fontsize = 10)
plt.ylabel("Precipitación [mm / día ]", fontsize=10)
plt.xlabel("Tiempo (meses)", fontsize=10)
plt.xticks(rotation=0)
plt.minorticks_on()
plt.legend()
plt.grid(color="lightgray",linewidth=1.0)
plt.ylim(-20,30)

plt.savefig(
    '/home/luisa/Escritorio/Semestre_Actual/2. Analisis de datos/T3/graficos/Anomalias-Tendencias'+'.png')
plt.show()

#------------------------------------------------------------------------------
#8. CORRELACIONES
#8.1 VALORES DE CORRELACIÓN PARA SPEARMAN Y PEARSON
person_P1P2=scipy.stats.pearsonr(P1,P2)[0]
spearman_P1P2=scipy.stats.spearmanr(P1,P2)[0]

A_person_P1P2=scipy.stats.pearsonr(A_P1,A_P2)[0]
A_spearman_P1P2=scipy.stats.spearmanr(A_P1,A_P2)[0]

print("Correlación de pearson=", person_P1P2)
print("Correlación de Spearman=", spearman_P1P2)
print("Correlación de pearson para las anomalías=", A_person_P1P2)
print("Correlación de Spearman para las anomalias=", A_spearman_P1P2)

#8.2 SCATTER PLOT
plt.figure(figsize=(10,8))
plt.suptitle("Scatter Plot \n P1 vs P2  y A_P1 vs AP2¨", fontsize=15)
plt.subplot(2, 2, 1)
plt.plot(P1,P2,'palegreen', linewidth=0,marker=".")
#Otras variables
plt.axhline(y=Me_P1,color="black",linewidth=1.0,label="Media_P1")
plt.axvline(x=Me_P2,color="k",linewidth=1.0,linestyle="--",label="Media_P2")
#Diseño
plt.text(1, 33, 'A', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
#plt.title("Datos originales", fontsize=15)
plt.xlabel("Muestra 2 de precipitación [mm/día]")
plt.ylabel("Muestra 1 de precipitación [mm/día]")
plt.minorticks_on()
plt.legend()
plt.grid()
plt.subplot(2, 2, 2)
plt.plot(A_P1,A_P2,'cornflowerblue', linewidth=0,marker=".")
#Otras variables

plt.axhline(y=0,color="k",linewidth=1.0)
plt.axvline(x=0,color="k",linewidth=1.0)
#Diseño
plt.text(-5, 17, 'B', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
#plt.title("Anomalías", fontsize=15)
plt.xlabel("Anomalias P2 de precipitación [mm/día]")
plt.ylabel("Anomalias P1 de precipitación [mm/día]")
plt.minorticks_on()
plt.legend()
plt.grid()
plt.savefig(
    '/home/luisa/Escritorio/Semestre_Actual/2. Analisis de datos/T3/graficos/Correlaciones'+'.png')
plt.show()


#------------------------------------------------------------------------------
#9. TERCER EJERCICIO
print("SEGUNDA PARTE- VALORES EXTREMOS")
#2. Valores “extremos”. Para este análisis es necesario remover el ciclo anual antes de proceder a
#analizar los valores extremos.

#(a) Seleccione los valores extremos de tal manera que sea el 10% de valores más grandes de los datos
#(este es un porcentaje muy alto, pero se usa acá solo con fines ilustrativos). Grafique estos máximos
#ordenados en el tiempo. Cualitativamente, ve usted alguna tendencia?.

#(b) Ahora escoja los valores extremos simplemente como el conjunto de valores máximos para cada
#año. Es decir, para cada año escoja el valor máximo. El conjunto de estos valores máximos será su
#nuevo conjunto de valores extremos. Grafique estos datos en función del tiempo. Cualitativamente, ve
#usted alguna tendencia? De un análisis de tendencia paramétrico: es la tendencia significativa?
print("PARTE A")

#9.1 VALORES ATIPICOS MAYORES AL 90% DE LOS DATOS Y MENORES AL 10%  

#MUESTRA 1
Atipicos_90_P1,per_90_P1=obtenermayorespercentil(A_P1,90,year_st)
Atipicos_10_P1,per_10_P1=obtenermenorespercentil(A_P1,10,year_st)
df_A90_P1=pd.DataFrame(Atipicos_90_P1)
df_A10_P1=pd.DataFrame(Atipicos_10_P1) 


print(" El percentil 10 para P1, es=",per_10_P1)
print(" El percentil 90 para P1, es=",per_90_P1)

#MUESTRA 2
Atipicos_90_P2,per_90_P2=obtenermayorespercentil(A_P2,90,year_st)
Atipicos_10_P2,per_10_P2=obtenermenorespercentil(A_P2,10,year_st)
df_A90_P2=pd.DataFrame(Atipicos_90_P2)
df_A10_P2=pd.DataFrame(Atipicos_10_P2) 

print(" El percentil 10 para P2, es=",per_10_P2)
print(" El percentil 90 para P2, es=",per_90_P2)


#GRAFICOS
#Muestra 1 de precipitación
plt.figure(figsize=(10,5))
plt.suptitle("Serie de tiempo para los datos extremos")
plt.subplot(2,1,1) 
plt.plot(year_st,A_P1, color="palegreen") 
#Otras variables
plt.plot(df_A90_P1[0],df_A90_P1[1], 'yo',color="darkslategray", MarkerSize = 4,
         label="máx y mín")
plt.plot(df_A10_P1[0],df_A10_P1[1], 'yo',color="darkslategray", MarkerSize = 4)
x1=np.percentile(A_P1,90)
x2=np.percentile(A_P1,10)
plt.axhline(y=x1,color="gray",linewidth=1.0,linestyle='--',label=('Limites'))
plt.axhline(y=x2,color="gray",linewidth=1.0,linestyle='--')
#Diseño del grafico
plt.text(1986, 10, 'A', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
#plt.title("Muestra 1", fontsize=10)
#plt.xlabel("Años")
plt.ylabel("Precipitación [mm/día]")
plt.minorticks_on()
plt.legend()
plt.grid(color="lightgray")

plt.subplot(2,1,2)
#Muestra 2 de precipitación
plt.plot(year_st,A_P2, color="plum") 
#Otras variables
plt.plot(df_A90_P2[0],df_A90_P2[1], 'yo',color="maroon", MarkerSize = 4,
         label="máx y mín")
plt.plot(df_A10_P2[0],df_A10_P2[1], 'yo',color="maroon", MarkerSize = 4)
x1=np.percentile(A_P2,90)
x2=np.percentile(A_P2,10)
plt.axhline(y=x1,color="gray",linewidth=1.0,linestyle='--',label=("limites"))
plt.axhline(y=x2,color="gray",linewidth=1.0,linestyle='--')
#Diseño del grafico
plt.text(1986, 15, 'B', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
#plt.title("Muestra 2", fontsize=10)
plt.xlabel("Tiempo(meses)")
plt.ylabel("Precipitación [mm/día]")
plt.minorticks_on()
plt.legend()
plt.grid(color="lightgray")
plt.savefig(
    '/home/luisa/Escritorio/Semestre_Actual/2. Analisis de datos/T3/graficos/ST-Datosatipicos'+'.png')
plt.show()
  
print("PARTE B")
#Aquí empezaremos a usar pandas para mejorar el analisis
#9.2 DATOS MAXICOS POR AÑO

inicio='1/1/1984'
final="31/12/2015"
P1_max,y=extraercolumn_Pandas(P1,inicio,final,1984,2016)
P2_max,y=extraercolumn_Pandas(P2,inicio,final,1984,2016)      

#Series de tiempo para los datos maximos

#Ciclo medio anual
CMA_P1_max=C1_12(P1_max) 
CMA_P2_max=C1_12(P2_max)    

#Anomalías
A_P1_max=anomaliaJ(P1_max,CMA_P1_max)
A_P2_max=anomaliaJ(P2_max,CMA_P2_max)

guardar=np.transpose([A_P1_max,A_P2_max])
guardar=pd.DataFrame(guardar)
guardar.to_csv(r'/home/luisa/Escritorio/Semestre_Actual/2. Analisis de datos/T3/documentos/max.csv',
                   sep=',')


#Pendientes
P_P1_max,p_P1_max=pendienteParametrica(P1_max,1984,A_P1_max)
P_P2_max,p_P2_max=pendienteParametrica(P2_max,1984,A_P2_max)

print("La pendiente parametrica para P1max=", P_P1_max)
print("La pendiente parametrica para P2max=", P_P2_max)

#guardamos datos
#Graficos

plt.figure(figsize=(10,5))
plt.suptitle("Series de tiempo- Precipitación \n Valores máximos anuales de anomalías", fontsize=15)
#Muestra 1
plt.subplot(2, 1, 1)
#plt.ylabel('Common X-Axis', fontsize=15, fontweight='bold')
plt.plot(y,A_P1_max, color="palegreen",label="P1_A")
#plt.plot(y,maxminmedio["P1_max"], color="springgreen",label="P1")
#Valores adicionales
plt.plot( y,p_P1_max, color = 'black', alpha=0.8,label="Pendiente P1 = \n -0,092 mm/día")
plt.axhline(y=0,color="midnightblue",linewidth=0.5,linestyle="--")
#Diseño del gráfico
plt.text(1986, 5, 'A', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.xticks(rotation=0)
plt.legend(loc=1)
plt.minorticks_on()
plt.ylabel("Precipitación [mm / día ]", fontsize=10)
plt.grid(color="lightgray")

#Muestra 2
plt.subplot(2, 1, 2)
plt.plot(y,A_P2_max, color="cornflowerblue",label="P2_A")
#Valores adicionales
plt.axhline(y=0,color="midnightblue",linewidth=0.5,linestyle="--")
plt.plot( y, p_P2_max, color = 'black', alpha=0.8,
         label="Pendiente P2 = \n 1,245 mm/día")
#Diseño del gráfico
plt.text(1986, 7, 'B', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.ylabel("Precipitación [mm / día ]", fontsize=10)
plt.xlabel("Tiempo(años)")
plt.xticks(rotation=0)
plt.minorticks_on()
plt.legend(loc=4)
plt.grid(color="lightgray")
plt.savefig(
    '/home/luisa/Escritorio/Semestre_Actual/2. Analisis de datos/T3/graficos/ST-Valoresmaximos'+'.png')
plt.show()



#Significancia.




nu=n-1
alfa=0.1
alfa_medio=alfa/2
q = 1-alfa / 2
tc = scipy.stats.t.ppf(q,nu)


tsen_p1=0.05218143095463007
tsen_p2=4.879464706722665

# Graficando T-Student

t = stats.t(nu)
x_pendiente = np.linspace(t.ppf(alfa_medio),t.ppf(1-alfa_medio), 100)
fp = t.pdf(x_pendiente) # Función de Probabilidad
plt.plot(x_pendiente, fp, color="silver")
#Limite para la significancia
#Curva parametrica T-Student
plt.axvline(x=-tc,linewidth=1.0,linestyle='--',color="silver",label="tc")
plt.axvline(x=tc,linewidth=1.0,linestyle='--',color="silver")
#Variables 
print(P_P1_max)
print(P_P2_max)
plt.axvline(x=P_P1_max,color="indigo",linewidth=1.0,label="P1 max")
plt.axvline(x=tsen_p1,color="darkgreen",linewidth=1.0,label="P1 sen")
plt.axvline(x=P_P1,color="indigo",linestyle="--",linewidth=1.0,label="P1")
plt.axvline(x=P_P2,color="slateblue",linestyle="--",linewidth=1.0,label="P2")
plt.axvline(x=P_P2_max,color="slateblue",linewidth=1.0,label="P2 max")
plt.axvline(x=tsen_p2,color="indianred",linewidth=1.0,label="P2 sen")
#Diseño
plt.grid(color='lightgrey', linewidth=0.5)
plt.minorticks_on()
plt.legend(loc=1,facecolor="w")
plt.title('Distribución T-Student para pendientes \n Valores máximos por año',fontsize=15)
plt.ylabel('Probabilidad(Pr)',fontsize=12)
plt.xlabel('Valores',fontsize=12)
#plt.savefig( 'E:\AD\T2\Graficos\pendientessignificancia'+'.png')
plt.savefig(
    '/home/luisa/Escritorio/Semestre_Actual/2. Analisis de datos/T3/graficos/Significancia_VM'+'.png')
plt.show()


#------------------------------------------------------------------------------
#3. Espectros de potencias.
#(a) Sin remover el ciclo anual, estime el espectro de potencias, para cada serie 
#de precipitación P1 y P2.
#Cuáles son las frecuencias o periodos dominantes en cada serie? Se parecen 
#estos espectros de potencia entre sí?
#(b) Ahora repita (a), pero removiendo antes el ciclo anual. Compare con el punto (a).


print("PARTE A")
#scipy.signal.espectrograma
#Ref:https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
#Funcionalidad: Los espectrogramas se pueden utilizar como una forma de visualizar
# el cambio del contenido de frecuencia de una señal no estacionaria a lo largo del tiempo.
#Devoluciones
#f ndarray=Matriz de frecuencias de muestra.
#t ndarray= Matriz de tiempos de segmento.
#sxx ​​ndarray=Espectrograma de x. Por defecto, el último eje de Sxx 
#   corresponde a los tiempos del segmento.


A_P1=anomaliaJ(P1,CMA_P1)
A_P2=anomaliaJ(P2,CMA_P2)

f_P1,t_P1,sxx_P1 =scipy.signal.spectrogram(P1)
f_P2,t_P2,sxx_P2 = scipy.signal.spectrogram(P2)


periodo_P1=[]
periodo_P2=[]
for i in range(len(f_P1)):
    periodo_P1.append(1/f_P1[i])
    periodo_P2.append(1/f_P2[i])


#graficos
plt.figure(figsize=(10,8))
plt.suptitle("Espectro de potencias- Precipitación", fontsize=15)
#Muestra 1
plt.subplot(2, 2, 1)
plt.plot(f_P1,sxx_P1, color="mediumorchid",label="P1")
#Diseño del gráfico
plt.text(0.45, 350, 'A', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))

plt.title("Muestra de precipitación 1")
plt.xticks(rotation=0)
plt.legend()
plt.minorticks_on()
plt.ylabel("Potencia", fontsize=10)
plt.xlabel("Frecuencia", fontsize=10)
plt.grid(color="lightgray")

plt.subplot(2, 2, 3)
plt.plot(periodo_P1,sxx_P1, color="mediumorchid",label="P1")
#Diseño del gráfico
plt.text(35, 10,  'B', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))

plt.yscale("log")
plt.xticks(rotation=0)
plt.legend()
plt.minorticks_on()
plt.ylabel("Potencia", fontsize=10)
plt.xlabel("Periodo", fontsize=10)
plt.grid(color="lightgray")
plt.xlim(0,40)
#Muestra 2
plt.subplot(2, 2, 2)
plt.plot(f_P2,sxx_P2,color="tomato",label="P2")
#Diseño del gráfico
plt.text(0.45, 550, 'C', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.title("Muestra de precipitación 2")
plt.ylabel("Potencia", fontsize=10)
plt.xlabel("Frecuencia", fontsize=10)
plt.xticks(rotation=0)
plt.minorticks_on()
plt.legend()

plt.grid(color="lightgray")
plt.subplot(2, 2, 4)
plt.plot(periodo_P2,sxx_P2,color="tomato",label="P2")
#Diseño del gráfico
plt.text(80, 60,'D', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.yscale("log")
plt.ylabel("Potencia", fontsize=10)
plt.xlabel("Periodo", fontsize=10)
plt.xticks(rotation=0)
plt.minorticks_on()
plt.legend()
plt.xlim(0,100)
plt.grid(color="lightgray")
plt.savefig(
    '/home/luisa/Escritorio/Semestre_Actual/2. Analisis de datos/T3/graficos/EspectroPotencias_orginales'+'.png')
plt.show()


print("PARTE B")
#Se generan los datos con la función del spectograma 
f_P1_A,t_P1_A, sxx_P1_A = scipy.signal.spectrogram(A_P1)
f_P2_A,t_P2_A, sxx_P2_A = scipy.signal.spectrogram(A_P2)

ntim = 100         # número de datos 
ti = 0.            # tiempo inicial
tf = 50.           # tiempo final
dt = (tf-ti)/ntim  # intervalo de tiempo entre datos

print(A_P1)

plt.plot(f_P2,sxx_P2)
print(sxx_P1_A)

#Se crean los vectores que contiene la información del periodo
periodo_P1_A=[]
periodo_P2_A=[]
for i in range(len(f_P1_A)):
    periodo_P1_A.append(1/f_P1_A[i])
    periodo_P2_A.append(1/f_P2_A[i])

#graficos
plt.figure(figsize=(10,7))
plt.suptitle("Espectro de potencias- Anomalias de Precipitación", fontsize=15)

#Muestra 1
plt.subplot(2, 2, 1)
plt.plot(f_P1_A,sxx_P1_A, color="mediumorchid",label="P1")
#Diseño del gráfico
plt.text(0.45, 280, 'A', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.title("Anomalías de precipitación Muestra 1")
plt.xticks(rotation=0)
plt.legend()
plt.minorticks_on()
plt.ylabel("Potencia", fontsize=10)
plt.xlabel("Frecuencia", fontsize=10)
plt.grid(color="lightgray")
plt.subplot(2, 2, 3)
plt.plot(periodo_P1_A,sxx_P1_A, color="mediumorchid",label="P1")
#Diseño del gráfico
plt.text(35, 10, 'B', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.yscale("log")
plt.xticks(rotation=0)
plt.legend()
plt.minorticks_on()
plt.ylabel("Potencia", fontsize=10)
plt.xlabel("Periodo", fontsize=10)
plt.grid(color="lightgray")
plt.xlim(0,40)
#Muestra 2
plt.subplot(2, 2, 2)
plt.plot(f_P2_A,sxx_P2_A,color="tomato",label="P2")
#Diseño del gráfico
plt.text(0.45, 330, 'C', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.title("Anomalías de precipitación Muestra 2")
plt.ylabel("Potencia", fontsize=10)
plt.xlabel("Frecuencia", fontsize=10)
plt.xticks(rotation=0)
plt.minorticks_on()
plt.legend()
plt.grid(color="lightgray")
plt.subplot(2, 2, 4)
plt.plot(periodo_P2_A,sxx_P2_A,color="tomato",label="P2")
#Diseño del gráfico
plt.text(80, 60, 'D', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.yscale("log")
plt.ylabel("Potencia", fontsize=10)
plt.xlabel("Periodo", fontsize=10)
plt.xticks(rotation=0)
plt.minorticks_on()
plt.legend()
plt.grid(color="lightgray")
plt.xlim(0,100)
plt.savefig(
    '/home/luisa/Escritorio/Semestre_Actual/2. Analisis de datos/T3/graficos/Espectropotencias-Anomalias'+'.png')
plt.show()

print("PARTE C")
#mu es el valor medio de los datos que se quieren emular
#fi, es la persistencia y depende de la autocorrelación de los datos a emular.
#Xo, es el valor inicial 
#epsilon= el valor aleatorio que depende de una distribución 

#Para la aleatoriedad de epsilo nos guiamos 
#https://www.geeksforgeeks.org/random-gauss-function-in-python/

#Muestra 1
xo_P1=P1[0]      
ro_P1=autocorrelacion(P1)
fi_P1=ro_P1
sigma_P1=(((n - 1)/(n - 2))*(1 - fi_P1**2)*(DES_P1**2))
#Muestra 2
xo_P2=P2[0]      
ro_P2=autocorrelacion(P2)
fi_P2=ro_P2
sigma_P2=(((n - 1)/(n - 2))*(1 - fi_P2**2)*(DES_P2**2))

P1_AR=AR(Ma_P1,fi_P1,n,sigma_P1,xo_P1)  
P2_AR=AR(Ma_P2,fi_P2,n,sigma_P2,xo_P2)  

#------------------------------------------------------------------------------
#4. Obtenga el espectro de onditas para cada una de las series de precipitación. 
#Puede adaptar los ejemplos de scripts proporcionados en clase. Compare los 
#espectros obtenidos para las dos series. Compare además con los resultados 
#obtenidos en el punto 3.
año = np.zeros(n)
año[0] = ti
for i in range(n-1):
    año[i+1] = año[i] + 1/12

#scales = np.logspace(1.2, 3.1, num=200, dtype=np.int32)


scales = scg.periods2scales(np.arange(1,40))
ax = scg.cws(año,P1, figsize=(5, 5), xlabel="Años", ylabel="Periodo",cbar="vertical",
             title="Espectro de onditas para la muestra 1")
ax = scg.cws(año,P2, figsize=(5, 5), xlabel="Años", ylabel="Periodo",cbar="vertical",
             title="Espectro de onditas para la muestra 2")





