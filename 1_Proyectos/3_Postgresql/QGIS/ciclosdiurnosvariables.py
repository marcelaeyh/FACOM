#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 23:33:17 2022

@author: luisa
"""
################################################################################
#1. LIBRERIAS
import pandas as pd
import  numpy as np
from datetime import datetime
from tqdm import tqdm              # libreria para saber el tiempo de ejecucion
from sqlalchemy import create_engine
import os
import math
import re
import matplotlib.pyplot as plt #Para graficar
import time 
################################################################################
#2 . INFORMACIÓN DE ENTRADA
#base de datos
eng = "postgresql://luisa:000000@localhost:5432/alejandria" #Motor Luisa
engine = create_engine(eng) #Maquina
conn=engine.connect()
#direcciones
presion=r"/media/luisa/Datos/FACOM/gits/FACOM/1_Proyectos/3_Postgresql/QGIS/csv_excel/presiata201712-202205.csv"
temperatura=r"/media/luisa/Datos/FACOM/gits/FACOM/1_Proyectos/3_Postgresql/QGIS/csv_excel/tempsiata201712-202205.csv"
precipitacion=r"/media/luisa/Datos/FACOM/gits/FACOM/1_Proyectos/3_Postgresql/QGIS/psiata201306-202205.csv"
presionIDEAM=r"/media/luisa/Datos/FACOM/gits/FACOM/3_csv/Presi_n_Atmosf_rica.csv"

#dataframe cvs
pre=pd.read_csv(presion, na_values=-999.0, usecols=[1,2,3])
tem=pd.read_csv(temperatura, na_values=-999.0,usecols=[1,2,3])
p=pd.read_csv(precipitacion, na_values=-999.0,usecols=[1,2,3,4])
PRESION=pd.read_csv(presionIDEAM)
pres=PRESION[PRESION.CodigoEstacion==27015310]
#dataframe postgres
busqueda1='''
select valor_observado,observacion.cod_estacion, fecha_observacion
from observacion where cod_variable=1 and cod_estacion =27015310
'''
busqueda2='''
select valor_observado,observacion.cod_estacion, fecha_observacion
from observacion where cod_variable=2 and cod_estacion =27015330
'''
P=pd.read_sql(busqueda2,con=eng)
T=pd.read_sql(busqueda1,con=eng)

# Funciones
# Es un grafico donde se suman todos los minutos contenidos en una hora particular
# de un mes, dia y año en particular, que luego va a ser promediado con el resto de sumas
# de esa hora en diferentes años del conjunto de datos.
# los datos de fecha se deben ingresar como DATATIME y se deben crear
# cuatro columnas una para los años, otra para los meses, dias y horas
def sumapordias(dia,mes,y,variable,nombrecolumnavariable,nombrecolumnafecha):
    # Sumar cada hora en cada año del día que se quiere analizar
    v = [] # vector donde se acumulan los resultados del ciclo for
    for i in tqdm(y):
        for j in h:
            acumulado = variable[variable.month == mes][variable.day == dia][variable.year == i][variable.hour == j] # acumula un vector con ese día.
            if len(acumulado) == 0.0: # vector para evitar un error en el código más adelante
                continue
            acumulado.reset_index(drop = True,inplace = True) #se resetea el indice del nuevo vector de salida
            # Segun la variable se añade la variable que se va a sumar y se almacena la fecha
            suma = acumulado[nombrecolumnavariable].sum()
            fecha = acumulado[nombrecolumnafecha].min()
            v.append([fecha,suma])
    v = pd.DataFrame(v,columns=["fecha","valor"]) # Se convierte el resultado en un dataframe
    v["fecha"] = pd.to_datetime(v["fecha"]) # convertir fecha en Datatime
    v=v.set_index(["fecha"]) # se pone la fecha como indice
    v1=v["valor"].groupby(v.index.hour).mean()
    return(v,v1)

# Es un grafico donde se promedian todos los minutos contenidos en una hora particular
# de un mes, dia y año en particular, que luego va a ser promediado con el resto de promedios
# de esa hora en diferentes años del conjunto de datos.
# los datos de fecha se deben ingresar como DATATIME y se deben crear
# cuatro columnas una para los años, otra para los meses, dias y horas
def promediopordias(dia,mes,y,variable,nombrecolumnavariable,nombrecolumnafecha):
    # Sumar cada hora en cada año del día que se quiere analizar
    v = [] # vector donde se acumulan los resultados del ciclo for
    for i in tqdm(y):
        for j in h:
            acumulado = variable[variable.month == mes][variable.day == dia][variable.year == i][variable.hour == j] # acumula un vector con ese día.
            if len(acumulado) == 0.0: # vector para evitar un error en el código más adelante
                continue
            acumulado.reset_index(drop = True,inplace = True) #se resetea el indice del nuevo vector de salida
            # Segun la variable se añade la variable que se va a sumar y se almacena la fecha
            suma = acumulado[nombrecolumnavariable].mean()
            fecha = acumulado[nombrecolumnafecha].min()
            v.append([fecha,suma])
    v = pd.DataFrame(v,columns=["fecha","valor"]) # Se convierte el resultado en un dataframe
    v["fecha"] = pd.to_datetime(v["fecha"]) # convertir fecha en Datatime
    v=v.set_index(["fecha"]) # se pone la fecha como indice
    v1=v["valor"].groupby(v.index.hour).mean()
    return(v,v1)

#DESCRIPCIÓN DEL GRÁFICO
# Es un grafico donde se suman todos los minutos contenidos en una hora particular
# de un mes, dia y año en particular, que luego va a ser promediado con el resto de sumas
# de esa hora en diferentes años del conjunto de datos.

def sumapordias_mes(y,variable,mes,nombrecolumnavariable,nombrecolumnafecha):
    v = [] # vector donde se acumulan los resultados del ciclo for
    for i in tqdm(y):
        for k in d :
            for j in h:
                acumulado = variable[variable.month == mes][variable.day == k][variable.year == i][variable.hour == j] # acumula un vector con ese día.
                if len(acumulado) == 0.0: # vector para evitar un error en el código más adelante
                    continue
                acumulado.reset_index(drop = True,inplace = True) #se resetea el indice del nuevo vector de salida
                # Segun la variable se añade la variable que se va a sumar y se almacena la fecha
                suma = acumulado[nombrecolumnavariable].sum()
                fecha = acumulado[nombrecolumnafecha].min()
                v.append([fecha,suma])

    v = pd.DataFrame(v,columns=["fecha","valor"]) # Se convierte el resultado en un dataframe
    v["fecha"] = pd.to_datetime(v["fecha"]) # convertir fecha en Datatime
    v=v.set_index(["fecha"]) # se pone la fecha como indice
    v1=v["valor"].groupby(v.index.hour).mean()
    return(v1)

#DESCRIPCIÓN DEL GRÁFICO
# Es un grafico donde se promedian todos los minutos contenidos en una hora particular
# de un mes, dia y año en particular, que luego va a ser promediado con el resto de promedios
# de esa hora en diferentes años del conjunto de datos.
def promediopordias_mes(y,variable,mes,nombrecolumnavariable,nombrecolumnafecha):
    v = [] # vector donde se acumulan los resultados del ciclo for
    for i in tqdm(y):
        for k in d :
            for j in h:
                acumulado = variable[variable.month == mes][variable.day == k][variable.year == i][variable.hour == j] # acumula un vector con ese día.
                if len(acumulado) == 0.0: # vector para evitar un error en el código más adelante
                    continue
                acumulado.reset_index(drop = True,inplace = True) #se resetea el indice del nuevo vector de salida
                # Segun la variable se añade la variable que se va a sumar y se almacena la fecha
                suma = acumulado[nombrecolumnavariable].mean()
                fecha = acumulado[nombrecolumnafecha].min()
                v.append([fecha,suma])

    v = pd.DataFrame(v,columns=["fecha","valor"]) # Se convierte el resultado en un dataframe
    v["fecha"] = pd.to_datetime(v["fecha"]) # convertir fecha en Datatime
    v=v.set_index(["fecha"]) # se pone la fecha como indice
    v1=v["valor"].groupby(v.index.hour).mean()
    return(v1)

#Descripción: En este ciclo se va a promediar la variable por cada día para un mes y año
# particular, luego se tomaran todas las promedios para cada día en los diferentes años y se
# promediará.

def promediosdiarioparaunmes(y,mes,variable,nombrevariablecolumna,nombrefechacolumna):
    v=[]
    for i in tqdm(y):
        for j in d:
            acumulado=variable[variable.year==i][variable.month==mes][variable.day==j]
            if len(acumulado) == 0.0: # vector para evitar un error en el código más adelante
                continue
            acumulado.reset_index(drop = True,inplace = True) #se resetea el indice del nuevo vector de salida
            dia=acumulado[nombrevariablecolumna].mean()
            fecha = acumulado[nombrefechacolumna].min()
            v.append([fecha,dia])
    v = pd.DataFrame(v,columns=["fecha","valor"]) # Se convierte el resultado en un dataframe
    v["fecha"] = pd.to_datetime(v["fecha"]) # convertir fecha en Datatime
    v=v.set_index(["fecha"]) # se pone la fecha como indice
    v1=v["valor"].groupby(v.index.day).mean()    
    return(v1)
#Descripción: En este ciclo se va a sumar la variable por cada día para un mes y año
# particular, luego se tomaran todas las sumas para cada día en los diferentes años y se
# promediará.

def sumasdiariosparaunmes(y,mes,variable,nombrevariablecolumna,nombrefechacolumna):
    v=[]
    for i in tqdm(y):
        for j in d:
            acumulado=variable[variable.year==i][variable.month==mes][variable.day==j]
            if len(acumulado) == 0.0: # vector para evitar un error en el código más adelante
                continue
            acumulado.reset_index(drop = True,inplace = True) #se resetea el indice del nuevo vector de salida
            dia=acumulado[nombrevariablecolumna].sum()
            fecha = acumulado[nombrefechacolumna].min()
            v.append([fecha,dia])
    v = pd.DataFrame(v,columns=["fecha","valor"]) # Se convierte el resultado en un dataframe
    v["fecha"] = pd.to_datetime(v["fecha"]) # convertir fecha en Datatime
    v=v.set_index(["fecha"]) # se pone la fecha como indice
    v1=v["valor"].groupby(v.index.day).mean()    
    return(v1)
################################################################################
#3. CORRECCIONES DE LOS DATOS Y DATATIME
# corrección de datos de calidad
for index, row in tqdm(pre.iterrows()):
    if row["Calidad"]>2.6:
        pre["Presion"][index]=None
for index, row in tqdm(tem.iterrows()):
    if row["Calidad"]>2.6:
        tem["Temperatura"][index]=None
for index, row in tqdm(p.iterrows()):
    if row["Calidad"]>2.6:
        p["P1"][index]=None
        p["P2"][index]=None

#3.1 Convertir a datatime
pre["fecha_hora"]=pd.to_datetime(pre["fecha_hora"]) #presion SIATA
tem["fecha_hora"]=pd.to_datetime(tem["fecha_hora"]) #temperatura SIATA
p["fecha_hora"]=pd.to_datetime(p["fecha_hora"]) #precipitacion SIATA

pres["FechaObservacion"]=pd.to_datetime(pres["FechaObservacion"]) #Presión IDEAM
T["fecha_observacion"]=pd.to_datetime(T["fecha_observacion"]) #Temperatura IDEAM
P["fecha_observacion"]=pd.to_datetime(P["fecha_observacion"]) #Precipitacion IDEAM

#3.2 Columnas con año, mes, dia y hora
 
#3.2.1 Presión SIATA
pre["year"]=pd.to_datetime(pre['fecha_hora']).dt.year  # crea una columna con los años
pre["month"]=pd.to_datetime(pre['fecha_hora']).dt.month # crea una columna con los meses
pre["day"]=pd.to_datetime(pre['fecha_hora']).dt.day  # crea una columna con los dias
pre["hour"]=pd.to_datetime(pre['fecha_hora']).dt.hour # crea una columna con los hora
ypre=list(pre["year"].unique())
ypre.sort()
#3.2.2 Temperatura SIATA
tem["year"]=pd.to_datetime(tem['fecha_hora']).dt.year  # crea una columna con los años
tem["month"]=pd.to_datetime(tem['fecha_hora']).dt.month # crea una columna con los meses
tem["day"]=pd.to_datetime(tem['fecha_hora']).dt.day  # crea una columna con los dias
tem["hour"]=pd.to_datetime(tem['fecha_hora']).dt.hour # crea una columna con los hora
ytem=list(tem["year"].unique())
ytem.sort()
#3.2.3 Precipitación SIATA
p["year"]=pd.to_datetime(p['fecha_hora']).dt.year  # crea una columna con los años
p["month"]=pd.to_datetime(p['fecha_hora']).dt.month # crea una columna con los meses
p["day"]=pd.to_datetime(p['fecha_hora']).dt.day  # crea una columna con los dias
p["hour"]=pd.to_datetime(p['fecha_hora']).dt.hour # crea una columna con los hora
yp=list(p["year"].unique())
yp.sort()

#3.2.4 Presion IDEAM
pres["year"]=pd.to_datetime(pres['FechaObservacion']).dt.year  # crea una columna con los años
pres["month"]=pd.to_datetime(pres['FechaObservacion']).dt.month # crea una columna con los meses
pres["day"]=pd.to_datetime(pres['FechaObservacion']).dt.day  # crea una columna con los dias
pres["hour"]=pd.to_datetime(pres['FechaObservacion']).dt.hour # crea una columna con los hora
ypres=list(pres["year"].unique())
ypres.sort()
#3.2.5 Temperatura IDEAM
T["year"]=pd.to_datetime(T['fecha_observacion']).dt.year  # crea una columna con los años
T["month"]=pd.to_datetime(T['fecha_observacion']).dt.month # crea una columna con los meses
T["day"]=pd.to_datetime(T['fecha_observacion']).dt.day  # crea una columna con los dias
T["hour"]=pd.to_datetime(T['fecha_observacion']).dt.hour # crea una columna con los hora
yT=list(T["year"].unique())
yT.sort()
#3.2.5 Precipitación IDEAM
P["year"]=pd.to_datetime(P['fecha_observacion']).dt.year # crea una columna con los años
P["month"]=pd.to_datetime(P['fecha_observacion']).dt.month # crea una columna con los meses 
P["day"]=pd.to_datetime(P['fecha_observacion']).dt.day# crea una columna con los años dias
P["hour"]=pd.to_datetime(P['fecha_observacion']).dt.hour # crea una columna con los horas
yP=list(P["year"].unique())
yP.sort()

#vectores individuales de la cantidad de días, meses, y horas
h=list(pre["hour"].unique()) 
d=list(pre["day"].unique())
month=list(pre["month"].unique())
h.sort()
d.sort()
month.sort()

################################################################################
# 4. GRAFICOS

#4.1 Grafico de cilos diurnos para un día en particular

preSIATA, preSgbyHOUR= promediopordias(20,10,ypre,pre,"Presion","fecha_hora") #presión SIATA
tSIATA, tSgbyHOUR= promediopordias(20,10,ytem,tem,"Temperatura","fecha_hora") #temperatura SIATA
p1SIATA, p1SgbyHOUR=  sumapordias(20,10,yp,p,"P1","fecha_hora") #precipitacion 1 SIATA
p2SIATA, p2SgbyHOUR=  sumapordias(20,10,yp,p,"P2","fecha_hora") #precipitación 2 SIATA
preIDEAM, preIgbyHOUR= promediopordias(20,10,ypres,pres,"ValorObservado","FechaObservacion") #presión IDEAM
tIDEAM, tIgbyHOUR= promediopordias(20,10,yT,T,"valor_observado","fecha_observacion") #Temperatura IDEAM
pIDEAM, pIgbyHOUR= sumapordias(20,10,yP,P,"valor_observado","fecha_observacion")   # precipitación IDEAM    


#grafico
fechatitulo="20 de octubre"
#precipitación promedio del 15 de enero 
plt.figure(figsize=(10,5))  
plt.plot(p1SgbyHOUR,color="blue",label="P1 81 SIATA")
plt.plot(p2SgbyHOUR,color="blueviolet",label="P2 81 SIATA")
plt.plot(pIgbyHOUR,color="turquoise",label="27015330")
plt.title(" Ciclo Medio Diurno de Precipitacion \n IDEAM vs SIATA \n "+ str(fechatitulo),fontsize=15)
plt.minorticks_on()
plt.ylabel("Precipitación [mm]", fontsize=12)
plt.xlabel("Tiempo (horas)",fontsize=12)
plt.xticks(np.arange(0, 24, step=1))
plt.legend()
plt.grid()
#temperatura promedio del 15 de enero
plt.figure(figsize=(10,5))   
plt.plot(tSgbyHOUR,color="palevioletred",label="271 SIATA")
plt.plot(tIgbyHOUR,color="crimson",label="27015310 IDEAM")
plt.title(" Ciclo Medio Diurno de Temperatura \n IDEAM vs SIATA \n "+ str(fechatitulo),fontsize=15)
plt.minorticks_on()
plt.ylabel("Temperatura [°C]", fontsize=12)
plt.xlabel("Tiempo (horas)",fontsize=12)
plt.xticks(np.arange(0, 24, step=1))
plt.legend()
plt.grid()
#presión promedio del 15 de enero
plt.figure(figsize=(10,5))   
plt.plot(preSgbyHOUR,color="lime",label="271 SIATA")
plt.plot(preIgbyHOUR,color="green",label="27015310 IDEAM")
plt.title(" Ciclo Medio Diurno de Presión \n IDEAM vs SIATA \n "+ str(fechatitulo),fontsize=15)
plt.minorticks_on()
plt.ylabel("Presion [hpa]", fontsize=12)
plt.xlabel("Tiempo (horas)",fontsize=12)
plt.xticks(np.arange(0, 24, step=1))
plt.legend()
plt.grid()

#4.2 Grafico de cilos diurnos para un mes en particular
# en este grafico se suman las horas en cada año,mes,día en particular y luego
#esas sumas son agrupadas por horas y posteriormente promediadas.


preSgbyHOUR_mes=promediopordias_mes(ypre,pre,3,"Presion","fecha_hora") #presión SIATA
tSgbyHOUR_mes=promediopordias_mes(ytem,tem,3,"Temperatura","fecha_hora") #Temperatura SIATA
p1SgbyHOUR_mes=sumapordias_mes(yp,p,3,"P1","fecha_hora") #Precipitacion SIATA
p2SgbyHOUR_mes=sumapordias_mes(yp,p,3,"P2","fecha_hora") #Precipitacion SIATA
preIgbyHOUR_mes=promediopordias_mes(ypres,pres,3,"ValorObservado","FechaObservacion") #Presión IDEAM
tIgbyHOUR_mes=promediopordias_mes(yT,T,3,"valor_observado","fecha_observacion") #Temperatura IDEAM
pIgbyHOUR_mes=sumapordias_mes(yP,P,3,"valor_observado","fecha_observacion") #Precipitacion IDEAM

#grafico
fechatitulo="Marzo"
#precipitación promedio del 15 de enero 
plt.figure(figsize=(10,5))  
plt.plot(p1SgbyHOUR_mes,color="blue",label="P1 81 SIATA")
plt.plot(p2SgbyHOUR_mes,color="blueviolet",label="P2 81 SIATA")
plt.plot(pIgbyHOUR_mes,color="turquoise",label="27015330")
plt.title(" Ciclo Medio Diurno de Precipitacion \n IDEAM vs SIATA \n "+ str(fechatitulo),fontsize=15)
plt.minorticks_on()
plt.ylabel("Precipitación [mm]", fontsize=12)
plt.xlabel("Tiempo (horas)",fontsize=12)
plt.xticks(np.arange(0, 24, step=1))
plt.legend()
plt.grid()
#temperatura promedio del 15 de enero
plt.figure(figsize=(10,5))   
plt.plot(tSgbyHOUR_mes,color="palevioletred",label="271 SIATA")
plt.plot(tIgbyHOUR_mes,color="crimson",label="27015310 IDEAM")
plt.title(" Ciclo Medio Diurno de Temperatura \n IDEAM vs SIATA \n "+ str(fechatitulo),fontsize=15)
plt.minorticks_on()
plt.ylabel("Temperatura [°C]", fontsize=12)
plt.xlabel("Tiempo (horas)",fontsize=12)
plt.xticks(np.arange(0, 24, step=1))
plt.legend()
plt.grid()
#presión promedio del 15 de enero
plt.figure(figsize=(10,5))   
plt.plot(preSgbyHOUR_mes,color="lime",label="271 SIATA")
plt.plot(preIgbyHOUR_mes,color="green",label="27015310 IDEAM")
plt.title(" Ciclo Medio Diurno de Presión \n IDEAM vs SIATA \n "+ str(fechatitulo),fontsize=15)
plt.minorticks_on()
plt.ylabel("Presion [hpa]", fontsize=12)
plt.xlabel("Tiempo (horas)",fontsize=12)
plt.xticks(np.arange(0, 24, step=1))
plt.legend()
plt.grid()

#4.3 Grafico del ciclo medio para un mes particular
#Descripción: En este ciclo se va a sumar la precipitación por cada día para un mes y año
# particular, luego se tomaran todas las sumas para cada día en los diferentes años y se
# promediará.


preSgbyDAY_mes=promediosdiarioparaunmes(ypre,3,pre,"Presion","fecha_hora")
tSgbyDAY_mes=promediosdiarioparaunmes(ytem,3,tem,"Temperatura","fecha_hora")
p1SgbyDAY_mes=sumasdiariosparaunmes(yp,3,p,"P1","fecha_hora")
p2SgbyDAY_mes=sumasdiariosparaunmes(yp,3,p,"P2","fecha_hora")
preIgbyDAY_mes=promediosdiarioparaunmes(ypres,3,pres,"ValorObservado","FechaObservacion")
tIgbyDAY_mes=promediosdiarioparaunmes(yT,3,T,"valor_observado","fecha_observacion")
pIgbyDAY_mes=sumasdiariosparaunmes(yP,3,P,"valor_observado","fecha_observacion")

#grafico
fechatitulo="Marzo"
#precipitación promedio del 15 de enero 
plt.figure(figsize=(10,5))  
plt.plot(p1SgbyDAY_mes,color="blue",label="P1 81 SIATA")
plt.plot(p2SgbyDAY_mes,color="blueviolet",label="P2 81 SIATA")
plt.plot(pIgbyDAY_mes,color="turquoise",label="27015330")
plt.title(" Ciclo Medio Diurno de Precipitacion \n IDEAM vs SIATA \n "+ str(fechatitulo),fontsize=15)
plt.minorticks_on()
plt.ylabel("Precipitación [mm]", fontsize=12)
plt.xlabel("Tiempo (horas)",fontsize=12)
plt.xticks(np.arange(0, 32, step=1))
plt.legend()
plt.grid()
#temperatura promedio del 15 de enero
plt.figure(figsize=(10,5))   
plt.plot(tSgbyDAY_mes,color="palevioletred",label="271 SIATA")
plt.plot(tIgbyDAY_mes,color="crimson",label="27015310 IDEAM")
plt.title(" Ciclo Medio Diurno de Temperatura \n IDEAM vs SIATA \n "+ str(fechatitulo),fontsize=15)
plt.minorticks_on()
plt.ylabel("Temperatura [°C]", fontsize=12)
plt.xlabel("Tiempo (horas)",fontsize=12)
plt.xticks(np.arange(0, 32, step=1))
plt.legend()
plt.grid()
#presión promedio del 15 de enero
plt.figure(figsize=(10,5))   
plt.plot(preSgbyDAY_mes,color="lime",label="271 SIATA")
plt.plot(preIgbyDAY_mes,color="green",label="27015310 IDEAM")
plt.title(" Ciclo Medio Diurno de Presión \n IDEAM vs SIATA \n "+ str(fechatitulo),fontsize=15)
plt.minorticks_on()
plt.ylabel("Presion [hpa]", fontsize=12)
plt.xlabel("Tiempo (horas)",fontsize=12)
plt.xticks(np.arange(0, 32, step=1))
plt.legend()
plt.grid()

#4.4 graculado de un mes
acumulado=p[p.year==2021][p.month==3]
acumulado.reset_index(drop = True,inplace = True) #se resetea el indice del nuevo vector de salida
m=np.cumsum(acumulado.P1)


plt.figure(figsize=(10,5))   
plt.plot(acumulado.fecha_hora,m,color="palevioletred",label="271 SIATA")
plt.title("Grafico acumulado de precipitacion \n Marzo",fontsize=15)
plt.ylabel("Precipitacion [mm]", fontsize=12)
plt.xlabel("Tiempo ",fontsize=12)
plt.xticks(rotation=90)
plt.legend()
plt.grid()
plt.minorticks_on()
