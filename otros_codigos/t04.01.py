#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 13:10:06 2022
@author: Luisa Fernanda Buriticá Ruíz & Danny Esteban Giraldo Mesa
"""
#1. LIBRERIAS
import pandas as pd
import  numpy as np
from datetime import datetime
import matplotlib.pyplot as plt #Para graficar
from tqdm import tqdm # libreria para saber el tiempo de ejecución
import scaleogram as scg 
import scipy 
from scipy import stats
from scipy import signal

#2. DATOS
direccion_E12="/home/luisa/Documentos/Semestre_Actual/2. Analisis de datos/T4/12_CA_2014-2021.csv"
direccion_E31="/home/luisa/Documentos/Semestre_Actual/2. Analisis de datos/T4/31_CA_2014-2021.csv"
direccion_E38="/home/luisa/Documentos/Semestre_Actual/2. Analisis de datos/T4/38_CA_2014-2021.csv"

E12=pd.read_csv(direccion_E12,na_values="NaN")
E31=pd.read_csv(direccion_E31,na_values="NaN")
E38=pd.read_csv(direccion_E38,na_values="NaN")


#---------------------------------------------------------------------------------------
#3. FUNCIONES

#3.1 CONVERTIR DATOS DUDOSOS A NaN
def dudosos(vector):
    n=len(vector)
    for i in range(n):
        if vector["calidad"][i]>= 2.6:
            vector["pm25"][i]="NaN"
        if vector["pm25"][i]<0:
            vector["pm25"][i]="NaN"
    return(vector)
    
#3.2 Ciclo medio mensual
def Ciclomedio_m_y(vector):
    m=vector
    m.columns=["C","fecha","pm25","calidad"]
    m["fechas"]=pd.to_datetime(m['fecha']).dt.strftime("%d/%m/%Y %X")
    m=m.drop(["C","fecha"],axis=1)
    #Creamos las 4 columnas con año, mes, día y hora
    m["year"]=pd.to_datetime(m['fechas']).dt.year 
    m["month"]=pd.to_datetime(m['fechas']).dt.month 
    m["day"]=pd.to_datetime(m['fechas']).dt.day
    m["hour"]=pd.to_datetime(m['fechas']).dt.hour 
    #creamos las lista con los dates
    h=list(m["hour"].unique())
    h.sort()
    d=list(m["day"].unique())
    d.sort()
    month=list(m["month"].unique())
    month.sort()
    y=list(m["year"].unique())
    y.sort()
    # modificamos los datos dudosos a NaN
    m=dudosos(m)
    #se cran los vectores para guardar los promedios
    Ma_year=[]
    Ma_mes=[]
    #Ciclo medio anual
    for i in tqdm(y):
        year=m[m.year==i]
        mean_y=year.pm25.mean(skipna=True)
        Ma_year.append(mean_y)
        print("Ingresa el promedio del año",i)
    #Ciclo medio mensual
    for i in tqdm(month):
        mes=m[m.month==i]
        mean_m=mes.pm25.mean(skipna=True)
        Ma_mes.append(mean_m)
        print("Ingresa el promedio del mes",i)
    
    return(Ma_mes,Ma_year,h,d,month,y)
        
#3.3 PROMEDIOS MENSUALES MULTIANUALES
def PromediosM_Multianuales(direccion):
    m=pd.read_csv(direccion,na_values="NaN")
    m.columns=["C","fecha","pm25","calidad"]
    m["fechas"]=pd.to_datetime(m['fecha']).dt.strftime("%d/%m/%Y %X")
    m=m.drop(["C","fecha"],axis=1)
    #Creamos las 4 columnas con año, mes, día y hora
    m["year"]=pd.to_datetime(m['fechas']).dt.year 
    m["month"]=pd.to_datetime(m['fechas']).dt.month 
    m["day"]=pd.to_datetime(m['fechas']).dt.day
    m["hour"]=pd.to_datetime(m['fechas']).dt.hour

    #creamos las lista con los dates
    h=list(m["hour"].unique())
    h.sort()
    d=list(m["day"].unique())
    d.sort()
    month=list(m["month"].unique())
    month.sort()
    y=list(m["year"].unique())
    y.sort()
    m=dudosos(m) 
    
    CMmultianual=[]
    for i in tqdm(y):
        year=m[m.year==i]
        for j in tqdm(month):
            mes=year[year.month==j]
            mean_m=mes.pm25.mean(skipna=True)
            CMmultianual.append(mean_m)
    CMmultianual_df=pd.DataFrame(CMmultianual) 
    CMmultianual_df.columns=["pm25"]
    inicio='1/1/2014'
    final="31/12/2021"  
    CMmultianual_df["fechas"]=pd.date_range(start=inicio, end=final, freq='M')
    CMmultianual_df["fecha"]=pd.to_datetime(CMmultianual_df['fechas']).dt.strftime("%m/%Y")
    
    
    return(CMmultianual_df)


def Promediosdiarios(direccion):
    m=pd.read_csv(direccion,na_values="NaN")
    m.columns=["C","fecha","pm25","calidad"]
    m["fechas"]=pd.to_datetime(m['fecha']).dt.strftime("%d/%m/%Y %X")
    m=m.drop(["C","fecha"],axis=1)
    #Creamos las 4 columnas con año, mes, día y hora
    m["year"]=pd.to_datetime(m['fechas']).dt.year 
    m["month"]=pd.to_datetime(m['fechas']).dt.month 
    m["day"]=pd.to_datetime(m['fechas']).dt.day
    m["hour"]=pd.to_datetime(m['fechas']).dt.hour

    #creamos las lista con los dates
    h=list(m["hour"].unique())
    h.sort()
    d=list(m["day"].unique())
    d.sort()
    month=list(m["month"].unique())
    month.sort()
    y=list(m["year"].unique())
    y.sort()
    m=dudosos(m)
    diario=[]
    for i in tqdm(h):
        dia=m[m.hour==i]
        media=dia.pm25.mean(skipna=True)
        diario.append(media)
    diario=pd.DataFrame(diario)
    diario.columns=["pm25"]
        
    return(diario)

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

#iniciamos las variables
def marzo_julio_horario(vector,v_horario):
    #MarzoJulio=[]
    vector_m=vector[vector.month==2]
    #print(vector_m.pm25.mean())
    vector_j=vector[vector.month==6]
    v=pd.concat([vector_m,vector_j],axis=0)
    MARZO=[]
    JULIO=[]
    marzo=0
    julio=0
    media_m=0
    media_j=0
    for i in tqdm(h_12):
        marzo=vector_m[vector_m.hour==i]
        julio=vector_j[vector_j.hour==i]
        media_m=marzo.pm25.mean()
        media_j=julio.pm25.mean()
        MARZO.append(media_m)
        JULIO.append(media_j)
    return(MARZO,JULIO,v)

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
#----------------------------------------------------------------------------------         

#4.ciclo medio anual y promedios anuales,
#4.1 Ciclos medios anuales
#además se extrae la información de cantidad de días, meses, años y horas
# si se presenta un error de que las variables son menos que las que solicita
#la función, cerrar y volver a abrir spyder 
E12_CMA,E12_PMA,h_12,d_12,month_12,y_12=Ciclomedio_m_y(E12)
E31_CMA,E31_PMA,h_31,d_31,month_31,y_31=Ciclomedio_m_y(E31)
E38_CMA,E38_PMA,h_38,d_38,month_38,y_38=Ciclomedio_m_y(E38)

#4.2 GRAFICOS
#4.2.1 CICLO MEDIO ANUALES
meses=np.array(["Ene","Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", 
                "Sep","Oct", "Nov", "Dic"])
#Promedio de los ciclos medios anuales
Me_E12_CMA=np.mean(E12_CMA)
Me_E31_CMA=np.mean(E31_CMA)
Me_E38_CMA=np.mean(E38_CMA)

print(E31_CMA)
print(np.max(E12_CMA))
print(np.min(E12_CMA))

print("#--------------#")
print("Ciclo medio anual")
print("El valor maximo de Ciclo medio anualE12 es="
      , np.max(E12_CMA), " en MARZO")
print("El valor minimo de Ciclo medio anual E12 es="
      , np.min(E12_CMA), " en JULIO")
print("El valor maximo de Ciclo medio anualE31 es="
      , np.max(E31_CMA), " en MARZO")
print("El valor minimo de Ciclo medio anual E31 es="
      , np.min(E31_CMA), " en NOVIEMBRE")
print("El valor maximo de Ciclo medio anual E38 es="
      , np.max(E38_CMA), " en el MARZO")
print("El valor minimo de lCiclo medio anual E38 es="
      , np.min(E38_CMA), " en JULIO")
print("promedio de E12_PMA=",Me_E12_CMA)
print("promedio de E31_PMA=",Me_E31_CMA)
print("promedio de E38_PMA=",Me_E38_CMA)
print("#--------------#")

#Anommalias, pendientes


#4.2.2 GRAFICOS 
plt.figure(figsize=(10,5))
plt.suptitle("Ciclo Medio Anual - PM 2.5  \n 2014-2021", fontsize=15)
#Estación 12
plt.subplot(1, 3, 1)
plt.plot(meses,E12_CMA, color="seagreen",label="Estación 12")
plt.axhline(y=Me_E12_CMA,color="k",linewidth=1.0,linestyle="--")
plt.text(10, 18, 'A', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.xticks(rotation=90)
plt.legend()
plt.minorticks_on()
plt.ylabel("Concentración [μg /m3 ]", fontsize=12)
plt.xlabel("Tiempo (meses)",fontsize=12)
plt.grid()
plt.ylim(15,45)
#Estación 31
plt.subplot(1, 3, 2)
plt.axhline(y=Me_E31_CMA,color="k",linewidth=1.0,linestyle="--")
plt.plot(meses,E31_CMA, color="crimson",label="Estación 31")
plt.text(10, 18, 'B', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.xticks(rotation=90)
plt.minorticks_on()
plt.xlabel("Tiempo (mes)",fontsize=12)
plt.legend()
plt.grid()
plt.ylim(15,45)
#Estación 38
plt.subplot(1, 3, 3)
plt.axhline(y=Me_E38_CMA,color="k",linewidth=1.0,linestyle="--")
plt.text(10, 18, 'C', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.plot(meses,E38_CMA, color="darkorange",label="Estación 38")
plt.xticks(rotation=90)
plt.minorticks_on()
plt.xlabel("Tiempo (mes)",fontsize=12)
plt.legend()
plt.grid()
plt.ylim(15,45)
plt.savefig( '/home/luisa/Documentos/Semestre_Actual/2. Analisis de datos/T4/graficos'
            + "/CMA_E12_E31_E38_2014-2021"+'.png',dpi = 400)
plt.show()


#4.2.3 PROMEDIOS ANUALES
plt.figure(figsize=(10,5))
Me_E12_PMA=np.mean(E12_PMA)
Me_E31_PMA=np.mean(E31_PMA)
Me_E38_PMA=np.mean(E38_PMA)
DE_E12_PMA=np.std(E12_PMA)
DE_E31_PMA=np.std(E31_PMA)
DE_E38_PMA=np.std(E38_PMA)

print(E12_PMA)

print("#--------------#")
print("Promedios anuales")
print("El valor maximo de los promedios anuales E12 es="
      , np.max(E12_PMA), " en el año 2015")
print("El valor minimo de los promedios anuales E12 es="
      , np.min(E12_PMA), " en el año 2020")
print("El valor maximo de los promedios anuales E31 es="
      , np.max(E31_PMA), " en el año 2016")
print("El valor minimo de los promedios anuales E31 es="
      , np.min(E31_PMA), " en el año 2021")
print("El valor maximo de los promedios anuales E38 es="
      , np.max(E38_PMA), " en el año 2016")
print("El valor minimo de los promedios anuales E38 es="
      , np.min(E38_PMA), " en el año 2021")
print("promedio de E12_PMA=",Me_E12_PMA)
print("promedio de E31_PMA=",Me_E31_PMA)
print("promedio de E38_PMA=",Me_E38_PMA)

print("Desviación estandar de E12_PMA=",DE_E12_PMA )
print("Desviación estandar de E31_PMA=",DE_E31_PMA )
print("Desviación estandar de E38_PMA=",DE_E38_PMA )

print("#--------------#")



#4.2.4 GRAFICOS
#Estación 12
plt.figure(figsize=(10,5))
plt.subplot(1, 3, 1)
plt.suptitle("Promedios Anuales - PM 2.5 \n 2014-2021", fontsize=15)
plt.axhline(y=Me_E12_PMA,color="k",linewidth=1.0,linestyle="--")
plt.plot(y_12,E12_PMA, color="seagreen",label="Estación 12")
plt.text(2015, 18, 'A', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.xticks(rotation=90)
plt.legend()
plt.minorticks_on()
plt.xlabel("Tiempo (años)",fontsize=12)
plt.ylabel("Concentración [μg /m3 ]", fontsize=12)
plt.grid()
plt.ylim(15,42)
#Estación 31
plt.subplot(1, 3, 2)
plt.plot(y_31,E31_PMA, color="crimson",label="Estación 31")
plt.axhline(y=Me_E31_PMA,color="k",linewidth=1.0,linestyle="--")
plt.text(2015, 18, 'B', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.xticks(rotation=90)
plt.minorticks_on()
plt.legend()
plt.grid()
plt.xlabel("Tiempo (años)",fontsize=12)
plt.ylim(15,42)
#Estación 38
plt.subplot(1, 3, 3)
plt.plot(y_38,E38_PMA, color="darkorange",label="Estación 38")
plt.text(2015, 18, 'C', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.axhline(y=Me_E38_PMA,color="k",linewidth=1.0,linestyle="--")
plt.xticks(rotation=90)
plt.minorticks_on()
plt.xlabel("Tiempo (años)",fontsize=12)
plt.legend()
plt.grid()
plt.ylim(15,42)
plt.savefig( '/home/luisa/Documentos/Semestre_Actual/2. Analisis de datos/T4/graficos'
            + "/PMA_E12_E31_E38_2014-2021"+'.png',dpi = 400)
plt.show() 
# SE ENCUENTRA QUE EL AÑO 2019 TIENE VALORES ATIPICOS MUY BAJOS, A CONTINUACIÓN
# PROCEDEMOS A ANALIZAR EL AÑO 2019

#4.3 PROMEDIOS MENSUALES MULTIANUAL

#4.3.1 CALCULO DE PROMEDIOS MENSUALES
E12_PMM=PromediosM_Multianuales(direccion_E12)
E31_PMM=PromediosM_Multianuales(direccion_E31)
E38_PMM=PromediosM_Multianuales(direccion_E38)

#4.3.2 CALCULO DE MEDIAS DE PROMEDIOS MENSUALES
Me_E12_PMM=np.mean(E12_PMM["pm25"])
Me_E31_PMM=np.mean(E31_PMM["pm25"])
Me_E38_PMM=np.mean(E38_PMM["pm25"])

print("promedio E12 PMM=", Me_E12_PMM)
print("promedio E31 PMM=", Me_E31_PMM)
print("promedio E38 PMM=", Me_E38_PMM)

#4.2.1.1 ANOMALIAS

E12_A=anomaliaJ(E12_PMM["pm25"],E12_CMA)
E31_A=anomaliaJ(E31_PMM["pm25"],E31_CMA)
E38_A=anomaliaJ(E38_PMM["pm25"],E38_CMA)

DE_E12_A=np.std(E12_A)
DE_E31_A=np.std(E31_A)
DE_E38_A=np.std(E38_A)

print("desviación estandar E12", DE_E12_A)
print("desviación estandar E31", DE_E31_A)
print("desviación estandar E38", DE_E38_A)

df_E12_A=pd.DataFrame(E12_A)
df_E12_A.columns=["A"]
inicio='1/1/2014'
final="31/12/2021"  

df_E12_A["fechas"]=pd.date_range(start=inicio, end=final, freq='M')
E12_A_max=df_E12_A[df_E12_A.A==19.02297307904867]
E12_A_min=df_E12_A[df_E12_A.A==-17.53708236258572]
print(E12_A_max)
print(E12_A_min)
print("el valor maximo para las anoamlias en E12=",np.max(E12_A), 
      "en", E12_A_max)
print("el valor minimo para las anoamlias en E12=",np.min(E12_A),
      "en",E12_A_min )

df_E31_A=pd.DataFrame(E31_A)
df_E31_A.columns=["A"]
inicio='1/1/2014'
final="31/12/2021"  
df_E31_A["fechas"]=pd.date_range(start=inicio, end=final, freq='M')

E31_A_max=df_E31_A[df_E31_A.A==17.124894664851034]
E31_A_min=df_E31_A[df_E31_A.A==-15.48827920596004]

print("el valor maximo para las anoamlias en E31=",np.max(E31_A), 
      "en", E31_A_max)
print("el valor minimo para las anoamlias en E31=",np.min(E31_A),
      "en",E31_A_min )

df_E38_A=pd.DataFrame(E38_A)
df_E38_A.columns=["A"]
inicio='1/1/2014'
final="31/12/2021"  
df_E38_A["fechas"]=pd.date_range(start=inicio, end=final, freq='M')

E38_A_max=df_E38_A[df_E38_A.A==13.506359518473342]
E38_A_min=df_E38_A[df_E38_A.A==-14.130732210687373]

print("el valor maximo para las anoamlias en E38=",np.max(E38_A), 
      "en", E38_A_max)
print("el valor minimo para las anoamlias en E38=",np.min(E38_A),
      "en",E38_A_min )

df_E38_A.head()

#4.2.1.2 PENDIENTE PARAMETRICA
E12_PP,e12_PP=pendienteParametrica(E12_PMM,2014,E12_A)
E31_PP,e31_PP=pendienteParametrica(E31_PMM,2014,E31_A)
E38_PP,e38_PP=pendienteParametrica(E38_PMM,2014,E38_A)
print("la pendiente de E12=", E12_PP)
print("la pendiente de E31=", E31_PP)
print("la pendiente de E38=", E38_PP)

#4.3.3 GRAFICOS DE PROMEDIOS MENSUALES
plt.figure(figsize=(10,5))
plt.subplot(1, 3, 1)
plt.suptitle("Anomalías promedios mensuales - PM 2.5 \n 2014-2021", fontsize=12)
#Estación 12
plt.plot(E12_PMM["fecha"],E12_A, color="seagreen",label="Estación 12")
plt.plot(E12_PMM["fecha"],e12_PP, color="k",linestyle="--")
plt.xticks((np.arange(11,96 ,12)),rotation=90)
plt.yticks((np.arange(-20,20,5)))
plt.text(20, -15, 'A', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.legend()
plt.minorticks_on()
plt.ylabel("Concentración [μg /m3 ]", fontsize=12)
plt.grid()
plt.ylim(-20,20)
#Estación 31
plt.subplot(1, 3, 2)
plt.plot(E31_PMM["fecha"],E31_A, color="crimson",label="Estación 31")
plt.plot(E31_PMM["fecha"],e31_PP, color="k",linestyle="--")
plt.xticks((np.arange(11,96 ,12)),rotation=90)
plt.yticks((np.arange(-20,20,5)))
plt.text(20, -15, 'B', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.minorticks_on()
plt.legend()
plt.grid()
plt.ylim(-20,20)
#Estación 38
plt.subplot(1, 3, 3)
plt.plot(E38_PMM["fecha"],E38_A, color="darkorange",label="Estación 38")
plt.plot(E38_PMM["fecha"],e38_PP, color="k",linestyle="--")
plt.xticks((np.arange(11,96 ,12)),rotation=90)
plt.yticks((np.arange(-20,20,5)))
plt.text(20, -15, 'C', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.minorticks_on()
plt.legend()
plt.grid()
plt.ylim(-20,20)
plt.xlabel('Tiempo(meses)', x=-0.70, y=0, fontsize=12)
plt.savefig( '/home/luisa/Documentos/Semestre_Actual/2. Analisis de datos/T4/graficos'
            + "/PMM_Anomalias_E12_E31_E38_2014-2021"+'.png',dpi = 400)
plt.show() 

#4.4 CALCULO PROMEDIOS HORARIOS (7 AÑOS)

#4.4.1 CALCULO DE LOS PROMEDIOS HORARIOS
E12_PMD=Promediosdiarios(direccion_E12)
E31_PMD=Promediosdiarios(direccion_E31)
E38_PMD=Promediosdiarios(direccion_E38)

#4.4.2 CALCULO DE MEDIAS DE LOS PROMEDIOS HORARIOS
Me_E12_PMD=np.mean(E12_PMD["pm25"])
Me_E31_PMD=np.mean(E31_PMD["pm25"])
Me_E38_PMD=np.mean(E38_PMD["pm25"])

print("el promedio para las medias de los promedios horarios E12=",Me_E12_PMD)
print("el promedio para las medias de los promedios horarios E31=",Me_E31_PMD)
print("el promedio para las medias de los promedios horarios E38=",Me_E38_PMD)

plt.figure(figsize=(10,5))
plt.suptitle("Ciclo diurno multianual - PM 2.5 \n 2014-2021", fontsize=15)
#Estación 12
plt.subplot(1, 3, 1)
plt.axhline(y=Me_E12_PMD,color="k",linewidth=1.0,linestyle="--")
plt.plot(h_12,E12_PMD["pm25"] ,color="seagreen",label="Estación 12")
plt.text(4, 45, 'A', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.xticks(rotation=90)
plt.legend()
plt.minorticks_on()
plt.ylabel("Concentración [μg /m3 ]", fontsize=12)
plt.xticks((np.arange(0,26 ,4)),rotation=90)
plt.yticks((np.arange(0,50 ,2)))
plt.grid()
plt.ylim(15,50)

#Estación 31
plt.subplot(1, 3, 2)
plt.plot(h_31,E31_PMD["pm25"], color="crimson",label="Estación 31")
plt.axhline(y=Me_E31_PMD,color="k",linewidth=1.0,linestyle="--")
plt.text(4, 45, 'B', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.minorticks_on()
plt.legend()
plt.grid()
plt.xlabel("Tiempo (horas)",fontsize=12)
plt.xticks((np.arange(0,26 ,4)),rotation=90)
plt.yticks((np.arange(0,50 ,2)))
plt.ylim(15,50)
#Estación 38
plt.subplot(1, 3, 3)
plt.plot(h_38,E38_PMD["pm25"], color="darkorange",label="Estación 38")
plt.axhline(y=Me_E38_PMD,color="k",linewidth=1.0,linestyle="--")
plt.text(4, 45, 'C', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.xticks((np.arange(0,26 ,4)),rotation=90)
plt.yticks((np.arange(0,50 ,2)))
plt.minorticks_on()
plt.legend()
plt.grid()
plt.ylim(15,50)
plt.savefig( '/home/luisa/Documentos/Semestre_Actual/2. Analisis de datos/T4/graficos'
            + "/PMD_E12_E31_E38_2014-2021"+'.png',dpi = 400)
plt.show() 

#----------------------------------------------------------------------------------         
#5  EXTRAER INFORMACIÓN PARTICULAR

#5.1 ORGANIZANDO LA INFORMACIÓN DE CADA UNA DE LAS MUESTRAS
#Estación 12
E12=pd.read_csv(direccion_E12,na_values="NaN")
E12.columns=["C","fecha","pm25","calidad"]
E12=dudosos(E12)
E12["fechas"]=pd.to_datetime(E12['fecha']).dt.strftime("%d/%m/%Y %X")
E12=E12.drop(["C","fecha","calidad"],axis=1)
#Creamos las 4 columnas con año, mes, día y hora
E12["year"]=pd.to_datetime(E12['fechas']).dt.year 
E12["month"]=pd.to_datetime(E12['fechas']).dt.month 
E12["day"]=pd.to_datetime(E12['fechas']).dt.day
E12["hour"]=pd.to_datetime(E12['fechas']).dt.hour

#Estación 31
E31=pd.read_csv(direccion_E31,na_values="NaN")
E31.columns=["C","fecha","pm25","calidad"]
E31=dudosos(E31)
E31["fechas"]=pd.to_datetime(E31['fecha']).dt.strftime("%d/%m/%Y %X")
E31=E31.drop(["C","fecha","calidad"],axis=1)
#Creamos las 4 columnas con año, mes, día y hora
E31["year"]=pd.to_datetime(E31['fechas']).dt.year 
E31["month"]=pd.to_datetime(E31['fechas']).dt.month 
E31["day"]=pd.to_datetime(E31['fechas']).dt.day
E31["hour"]=pd.to_datetime(E31['fechas']).dt.hour

#Estación 38
E38=pd.read_csv(direccion_E38,na_values="NaN")
E38.columns=["C","fecha","pm25","calidad"]
E38=dudosos(E38)
E38["fechas"]=pd.to_datetime(E38['fecha']).dt.strftime("%d/%m/%Y %X")
E38=E38.drop(["C","fecha","calidad"],axis=1)
#Creamos las 4 columnas con año, mes, día y hora
E38["year"]=pd.to_datetime(E38['fechas']).dt.year 
E38["month"]=pd.to_datetime(E38['fechas']).dt.month 
E38["day"]=pd.to_datetime(E38['fechas']).dt.day
E38["hour"]=pd.to_datetime(E38['fechas']).dt.hour

#----------//----------//----------//----------#

#5.2 EXTRAER INFORMACIÓN DE MARZO Y JUNIO
#recordar
#0 Enero  -  1 Febrero   -   2 Marzo  -  3 Abril  -  4 Mayo  -  5 Junio
#6 Julio  -  7 Agosto  -  8 Septiembre  -  9 Octubre  -  10 Noviembre
#11 Diciembre
     

#iniciamos las variables
def marzo_julio_horario(vector,v_horario):
    #MarzoJulio=[]
    vector_m=vector[vector.month==2]
    #print(vector_m.pm25.mean())
    vector_j=vector[vector.month==6]
    v=pd.concat([vector_m,vector_j],axis=0)
    MARZO=[]
    JULIO=[]
    marzo=0
    julio=0
    media_m=0
    media_j=0
    for i in tqdm(h_12):
        marzo=vector_m[vector_m.hour==i]
        julio=vector_j[vector_j.hour==i]
        media_m=marzo.pm25.mean()
        media_j=julio.pm25.mean()
        MARZO.append(media_m)
        JULIO.append(media_j)
    return(MARZO,JULIO,v)
    
E12_marzomultianual,E12_juliomultianual,marzojulio_E12=marzo_julio_horario(E12,h_12)
E31_marzomultianual,E31_juliomultianual,marzojulio_E31=marzo_julio_horario(E31,h_31)
E38_marzomultianual,E38_juliomultianual,marzojulio_E38=marzo_julio_horario(E38,h_38)

print(marzojulio_E12)

plt.figure(figsize=(10,8))
plt.suptitle("Ciclo diurno para marzo y julio - PM 2.5 \n 2014-2021", fontsize=15)
#Estación 12
plt.subplot(1, 3, 1)
plt.title("Estación 12")
plt.plot(h_12,E12_marzomultianual,color="seagreen",label="Marzo")
plt.plot(h_12,E12_juliomultianual,color="seagreen",linestyle="--",label="Julio")
plt.legend()
plt.text(4, 50, 'A', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.minorticks_on()
plt.ylabel("Concentración [μg /m3 ]", fontsize=12)
plt.xticks((np.arange(0,26 ,4)),rotation=90)
plt.yticks((np.arange(0,55 ,2)))
plt.grid(color="lightgray")
plt.ylim(13,52)
#Estación 31
plt.subplot(1, 3, 2)
plt.title("Estación 31")
plt.plot(h_31,E31_marzomultianual,color="crimson",label="Marzo")
plt.plot(h_31,E31_juliomultianual,color="crimson",linestyle="--",label="Julio")
plt.legend()
plt.text(4, 50, 'B', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.minorticks_on()
plt.xticks((np.arange(0,26 ,4)),rotation=90)
plt.yticks((np.arange(0,55 ,2)))
plt.grid(color="lightgray")
plt.ylim(13,52)
plt.xlabel("Tiempo (horas)",fontsize=12)
#Estación 38
plt.subplot(1, 3, 3)
plt.title("Estación 38")
plt.plot(h_38,E38_marzomultianual,color="darkorange",label="Marzo")
plt.plot(h_38,E38_juliomultianual,color="darkorange",linestyle="--",label="Julio")
plt.legend()
plt.text(4, 50, 'C', fontsize = 15,
         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.minorticks_on()
plt.xticks((np.arange(0,26 ,4)),rotation=90)
plt.yticks((np.arange(0,55 ,2)))
plt.grid(color="lightgray")
plt.ylim(13,52)
plt.savefig( '/home/luisa/Documentos/Semestre_Actual/2. Analisis de datos/T4/graficos'
            + "/CD_marzo_julio_E12_E31_E38_2014-2021"+'.png',dpi = 400)
plt.show() 

#----------//----------//----------//----------#
marzojulio_E12_df=pd.DataFrame(marzojulio_E12)
marzojulio_E31_df=pd.DataFrame(marzojulio_E31)
marzojulio_E38_df=pd.DataFrame(marzojulio_E38)


fig, axes = plt.subplots(nrows=1, ncols=3,figsize=(8, 5)) # create 2x2 array of subplots
marzojulio_E12.boxplot(column="pm25",by='month',figsize=(8, 5),ax=axes[0])
#plt.xticks([1,2],["Marzo","Junio"])
axes[0].set_ylabel('Concentración [μg /m3 ]', fontsize=12)
axes[0].set_title('Estación 12', fontsize=12)

#axes[0].set_xticks([1,2],["Marzo","Junio"])
marzojulio_E31.boxplot(column="pm25",by='month',figsize=(8, 5),ax=axes[1])
axes[1].set_title('Estación 31', fontsize=12)

marzojulio_E38.boxplot(column="pm25",by='month',figsize=(8, 5),ax=axes[2])
axes[2].set_title('Estación 38', fontsize=12)


marzojulio_E12.boxplot(column="pm25",by='month',figsize=(8, 5))
plt.title("pm25") 
plt.yticks((np.arange(0,140 ,10)))
plt.xticks([1,2],["Marzo","Junio"])
plt.ylabel("Concentración [μg /m3 ]", fontsize=12)
plt.xlabel("Tiempo (meses)",fontsize=12)

