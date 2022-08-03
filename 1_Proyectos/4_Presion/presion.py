#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 14:41:45 2022

@author: luisa
"""
#1. LIBRERIAS
import pandas as pd
import  numpy as np
from tqdm import tqdm              # librería para saber el tiempo de ejecución.
from sqlalchemy import create_engine
import matplotlib.pyplot as plt    #Para graficar.

direccion1= r"/media/luisa/Datos/FACOM/gits/FACOM/3_csv/Presi_n_Atmosf_rica.csv"

nombrecolumnafecha="FechaObservacion"
nombrecolumnavariable="ValorObservado"
estacion=36015020
variable="Presión"
unidades="Hpa"
datos= pd.read_csv(direccion1, usecols=[0,2,3])
df1= datos[datos.CodigoEstacion==36015020]

del datos


df1[nombrecolumnafecha]=pd.to_datetime(df1[nombrecolumnafecha]) #conversión a datatime.
df1["year"]=pd.to_datetime(df1[nombrecolumnafecha]).dt.year  # crea una columna con los años.
df1["month"]=pd.to_datetime(df1[nombrecolumnafecha]).dt.month # crea una columna con los meses.
df1["day"]=pd.to_datetime(df1[nombrecolumnafecha]).dt.day  # crea una columna con los días.
df1["hour"]=pd.to_datetime(df1[nombrecolumnafecha]).dt.hour # crea una columna con los hora.
df1["minute"]=pd.to_datetime(df1[nombrecolumnafecha]).dt.minute # crea una columna con los hora.
y=list(df1["year"].unique()) # se obtiene una lista de los años.
month=list(df1["month"].unique()) # se obtiene una lista de los meses.
d=list(df1["day"].unique()) # se obtiene una lista de los días.
h=list(df1["hour"].unique()) # se obtiene una lista de las horas.
minute=list(df1["minute"].unique())
h.sort()
d.sort()
month.sort()
y.sort()
minute.sort()
def STdiarios(variable,tipo,nombrecolumnafecha,nombrecolumnavariable):
    v=[]
    for i in tqdm(y):
        for j in month:
            for k in d:
                acumulado=variable[variable.year==i][variable.month==j][variable.day==k]
                if len(acumulado) == 0.0: # vector para evitar un error en el código más adelante
                    continue
                acumulado.reset_index(drop = True,inplace = True) #se resetea el indice del nuevo vector de salida
                if tipo ==1:
                    dia = acumulado[nombrecolumnavariable].sum()
                elif tipo ==2:
                    dia = acumulado[nombrecolumnavariable].mean()
                fecha = acumulado[nombrecolumnafecha].min()
                fecha= fecha.strftime('%Y-%m-%d')
                v.append([fecha,dia])
    v = pd.DataFrame(v,columns=["fecha","valor"]) # Se convierte el resultado en un dataframe
    v["fecha"] = pd.to_datetime(v["fecha"]) # convertir fecha en Datatime
    v["year"]=pd.to_datetime(v.fecha).dt.year
    v["month"]=pd.to_datetime(v.fecha).dt.month
    v["day"]=pd.to_datetime(v.fecha).dt.day
    v=v.set_index(["fecha"]) # se pone la fecha como indice
    return v
def STmensual(datos,tipoPD,nombrecolumnafecha,nombrecolumnavariable):
    df1=STdiarios(datos,tipoPD,nombrecolumnafecha,nombrecolumnavariable) #promedios diarios 
    df2=df1.valor.resample('M').mean() #serie de tiempo mensual
    df2=df2.reset_index()
    df2["year"]=pd.to_datetime(df2["fecha"]).dt.year  # crea una columna con los años
    df2["month"]=pd.to_datetime(df2["fecha"]).dt.month # crea una columna con los meses
    df2["day"]=pd.to_datetime(df2["fecha"]).dt.day  # crea una columna con los dias
    df2["hour"]=pd.to_datetime(df2["fecha"]).dt.hour # crea una columna con los hora
    return df2
def CMA_mes(datos,tipoPD,nombrecolumnafecha,nombrecolumnavariable):
    df1=STdiarios(datos,tipoPD,nombrecolumnafecha,nombrecolumnavariable) #promedios diarios
    df2=df1["valor"].groupby(df1.index.month).mean() #cma_mensual
    df2=df2.reset_index()
    df2.columns=["month","valor"]
    return df2
def anomalias_mes(datos,tipo,nombrecolumnafecha,nombrecolumnavariable):
    #serie de tiempo de promedios mensuales de acumulados/promedios diarios
    df1=STmensual(datos,tipo,nombrecolumnafecha,nombrecolumnavariable) 
    #cma mensual de acumulados/promedios diarios
    df2=CMA_mes(datos,tipo,nombrecolumnafecha,nombrecolumnavariable)

    v=[] #Vector para ingresar los resultados 
    for i in tqdm(y): # año # Ejecuta las restas para encontrar las anomalías
        for j in month: # mes
            acumulado1=df1[df1.year==i][df1.month==j] #valor dia particular.
            acumulado2=df2[df2.month==j]# valor del dia promedio. 
            if len(acumulado1) == 0.0: # vector para evitar un error en el código más adelante
                continue
            # reseteo del indice en ambos vectores
            acumulado1.reset_index(drop = False,inplace = True)
            acumulado2.reset_index(drop = False,inplace = True)
            resta=acumulado1.valor[0]-acumulado2.valor[0] # se ejecuta la resta
            
            fecha=acumulado1.fecha[0] #fecha analizada
            v.append([resta,fecha]) # se agrega al vector resultante
    v=pd.DataFrame(v,columns=["valor","fecha"])
    return(v)
    
    
g18=anomalias_mes(df1,2,nombrecolumnafecha,nombrecolumnavariable) #anomalias mensuales
g5=STmensual(df1,2,nombrecolumnafecha,nombrecolumnavariable)


def cmaminutos(datos,tipo,nombrecolumnafecha,nombrecolumnavariable):
    v=[]   
    for i in tqdm(month):
        for j in d:
            for k in h:
                for w in minute:
                    acumulado=datos[datos.month==i][datos.day==j][datos.hour==k][datos.minute==w]
                    acumulado=acumulado.reset_index()
                    if len(acumulado) == 0.0: # vector para evitar un error en el código más adelante
                        continue
                    if tipo ==1:
                        m = acumulado[nombrecolumnavariable].sum()
                    elif tipo ==2:
                        m = acumulado[nombrecolumnavariable].mean()
                    fecha=acumulado[nombrecolumnafecha][0] #fecha analizada
                    v.append([m,fecha]) # se agrega al vector resultante
    v = pd.DataFrame(v,columns=["valor","fecha"]) # Se convierte el resultado en un dataframe
    v["fecha"] = pd.to_datetime(v["fecha"]) # convertir fecha en Datatime
    v["month"]=pd.to_datetime(v.fecha).dt.month
    v["day"]=pd.to_datetime(v.fecha).dt.day
    v["hour"]=pd.to_datetime(v.fecha).dt.hour
    v["minute"]=pd.to_datetime(v.fecha).dt.minute
    for i in range(len(v)):
        v["fecha"][i]=v["fecha"][i].strftime('%m-%d %I:%S:%M')
    return(v)
                    
m1=cmaminutos(df1,2,nombrecolumnafecha,nombrecolumnavariable)#cma por minuto           
                    

def anomaliasmin(datos,tipo,nombrecolumnafecha, nombrecolumnavariable):
    datos1=cmaminutos(datos,tipo,nombrecolumnafecha,nombrecolumnavariable)#cma por minuto 
    v=[]
    for i in tqdm(y):
        for j in month:
            for k in d:
                for w in h:
                    for x in minute:
                        acumulado1=datos[datos.year==i][datos.month==j][datos.day==k][datos.hour==w][datos.minute==x]
                        acumulado2=datos1[datos1.month==j][datos1.day==k][datos1.hour==w][datos1.minute==x]
                        acumulado1=acumulado1.reset_index()
                        acumulado2=acumulado2.reset_index()
                        if len(acumulado1) == 0.0 or len(acumulado2) == 0.0: # vector para evitar un error en el código más adelante
                            continue
                        resta=acumulado1[nombrecolumnavariable][0]-acumulado2["valor"][0]
                        fecha=acumulado1[nombrecolumnafecha][0] #fecha analizada
                        v.append([resta,fecha]) # se agrega al vector resultante
    v = pd.DataFrame(v,columns=["valor","fecha"]) # Se convierte el resultado en un dataframe
    return(v)
                        
m2=anomaliasmin(df1,2,nombrecolumnafecha, nombrecolumnavariable)


y1=[2007,2008]
tipo=2
m1=cmaminutos(df1,2,nombrecolumnafecha,nombrecolumnavariable)#cma por minuto  
for i in tqdm(y1):
    print(i)
    for j in month:
        for k in d:
            for w in h:
                for x in minute:
                    acumulado1=df1[df1.year==i][df1.month==j][df1.day==k][df1.hour==w][df1.minute==x]
                    acumulado2=m1[m1.month==j][m1.day==k][m1.hour==w][m1.minute==x]
                    if len(acumulado1)==0 or len(acumulado2) == 0.0: # vector para evitar un error en el código más adelante
                        #print(i,"-",j,"-",k,"-",w,"-",x,"-")
                        continue
                    acumulado1=acumulado1.reset_index()
                    acumulado2=acumulado2.reset_index()
                    resta=acumulado1[nombrecolumnavariable][0]-m1["valor"][0]
                    
                    print(resta)

acumulado1=df1[df1.year==2021][df1.month==3][df1.day==14][df1.hour==6][df1.minute==0]
acumulado2=m1[m1.month==3][m1.day==14][m1.hour==6][m1.minute==0]
acumulado1=acumulado1.reset_index()
acumulado2=acumulado2.reset_index()
resta=acumulado1[nombrecolumnavariable][0]-acumulado2["valor"][0]


df3=df1[df1.month==3][df1.day==14][df1.hour==5][df1.minute==0]
df4=df3[nombrecolumnavariable].mean()
fecha=df3.FechaObservacion

df1=df1.set_index([nombrecolumnafecha]) # se pone la fecha como indice
df1=df1.reset_index()
df2=df1["ValorObservado"].groupby(df1.index.minute).mean() #cma_mensual

print(len(g5))
g20=g18

g18=g20
from scipy import stats

p5=stats.scoreatpercentile(g18.valor, 1)
p95=stats.scoreatpercentile(g18.valor, 99)

count=0
for index, row in tqdm(g18.iterrows()):
    if g18["valor"][index] < p5 or g18["valor"][index] > p95:
        
        print(g18.fecha[index])
        print(g5.fecha[index])
        count=count+1
        print(count)
        g18["valor"][index] = None


num_bins = 30
plt.figure(figsize=(10,5))
plt.title("Presión",fontsize=15)
plt.hist(df1[nombrecolumnavariable], num_bins,facecolor = "slateblue",
         alpha=0.75,label="T",edgecolor = "gray")


#gráfico
plt.figure(figsize=(10,5))  
plt.plot(g18.fecha,g18.valor,color="darkslategray",label=(str(estacion)+"- g18"))
plt.title(" Anomalías ST mensual  \n  "+ str(variable),fontsize=15)
plt.axhline(y=0,color="k",linewidth=1.0,linestyle="--")
plt.ylabel( str(variable)+ " ["+str(unidades)+"]", fontsize=12)
plt.xlabel("Tiempo (meses)",fontsize=12)
plt.minorticks_on()
plt.legend()
plt.grid()