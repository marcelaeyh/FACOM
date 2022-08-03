#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 09:32:19 2022

@author: luisa
"""
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import datetime
import os
import windrose #https://github.com/python-windrose/windrose
from windrose import WindroseAxes
from tqdm import tqdm              # librería para saber el tiempo de ejecución.


#tutorial
# https://github.com/SaulMontoya/Tutorial-para-realizar-una-Rosa-de-Vientos-con-Python/blob/master/Rosa%20de%20Vientos.ipynb
# https://www.youtube.com/watch?v=_VeS0qdmbkc
###############################################################################
#direcciones
#d1=r"/media/luisa/Datos/FACOM/gits/FACOM/3_csv/Direcci_n_Viento.csv"
#d2=r"/media/luisa/Datos/FACOM/gits/FACOM/3_csv/Velocidad_Viento.csv"
#direccionV=pd.read_csv(d1,usecols=[0,2,3])
#velocidadV=pd.read_csv(d2,usecols=[0,2,3])
############################################
#cseleccionamos una estacion para empezar con el analisis
estacion=15065190
nombrecolumnacod="CodigoEstacion"
nombrecolumnafecha="FechaObservacion"

#dv_datos=direccionV[direccionV[nombrecolumnacod]==estacion]
#vv_datos=velocidadV[velocidadV[nombrecolumnacod]==estacion]
#dv_datos.to_csv(r"/media/luisa/Datos/FACOM/gits/FACOM/1_Proyectos/7_direccionviento/estacion15065190dv.csv")
#vv_datos.to_csv(r"/media/luisa/Datos/FACOM/gits/FACOM/1_Proyectos/7_direccionviento/estacion15065190vv.csv")
###############################################
#ingresando datos de la estación 15065190
d1=r"/media/luisa/Datos/FACOM/gits/FACOM/1_Proyectos/7_direccionviento/estacion15065190.csv"
d2=r"/media/luisa/Datos/FACOM/gits/FACOM/1_Proyectos/7_direccionviento/estacion15065190vv.csv"
df1=pd.read_csv(d1)
df2=pd.read_csv(d2)

#direccion
df1[nombrecolumnafecha]=pd.to_datetime(df1[nombrecolumnafecha]) #conversión a datatime.
df1["year"]=pd.to_datetime(df1[nombrecolumnafecha]).dt.year  # crea una columna con los años.
df1["month"]=pd.to_datetime(df1[nombrecolumnafecha]).dt.month # crea una columna con los meses.
df1["day"]=pd.to_datetime(df1[nombrecolumnafecha]).dt.day  # crea una columna con los días.
df1["hour"]=pd.to_datetime(df1[nombrecolumnafecha]).dt.hour # crea una columna con los hora.
df1["minute"]=pd.to_datetime(df1[nombrecolumnafecha]).dt.minute # crea una columna con los hora.
y1=list(df1["year"].unique()) # se obtiene una lista de los años.
month1=list(df1["month"].unique()) # se obtiene una lista de los meses.
d1=list(df1["day"].unique()) # se obtiene una lista de los días.
h1=list(df1["hour"].unique()) # se obtiene una lista de las horas.
minute1=list(df1["minute"].unique())
h1.sort()
d1.sort()
month1.sort()
y1.sort()
minute1.sort()
df1= df1.sort_values(by=nombrecolumnafecha) 

#velocidad
df2[nombrecolumnafecha]=pd.to_datetime(df2[nombrecolumnafecha]) #conversión a datatime.
df2["year"]=pd.to_datetime(df2[nombrecolumnafecha]).dt.year  # crea una columna con los años.
df2["month"]=pd.to_datetime(df2[nombrecolumnafecha]).dt.month # crea una columna con los meses.
df2["day"]=pd.to_datetime(df2[nombrecolumnafecha]).dt.day  # crea una columna con los días.
df2["hour"]=pd.to_datetime(df2[nombrecolumnafecha]).dt.hour # crea una columna con los hora.
df2["minute"]=pd.to_datetime(df2[nombrecolumnafecha]).dt.minute # crea una columna con los hora.

y2=list(df2["year"].unique()) # se obtiene una lista de los años.
month2=list(df2["month"].unique()) # se obtiene una lista de los meses.
d2=list(df2["day"].unique()) # se obtiene una lista de los días.
h2=list(df2["hour"].unique()) # se obtiene una lista de las horas.
minute2=list(df2["minute"].unique())

h2.sort()
d2.sort()
month2.sort()
y2.sort()
minute2.sort()
df2= df2.sort_values(by=nombrecolumnafecha) 
print(len(d1),len(d2))

v=[]                   
for k in tqdm(d1):
    for l in h1:
        for w in minute1:
            acumulado1=df1[df1.year==2016][df1.month==3][df1.day==k][df1.hour==l][df1.minute==w]
            acumulado2=df2[df2.year==2016][df2.month==3][df2.day==k][df2.hour==l][df2.minute==w]
            if len(acumulado1) == 0.0 or len(acumulado2) == 0.0: # vector para evitar un error en el código más adelante
                continue
            acumulado1=acumulado1.reset_index(drop=True)
            acumulado2=acumulado2.reset_index(drop=True)
            v.append([acumulado1.FechaObservacion[0],
                      acumulado1.ValorObservado[0],
                      acumulado2.ValorObservado[0]])
    
v = pd.DataFrame(v,columns=["fecha","dv","vv"]) # Se convierte el resultado en un dataframe

ax = WindroseAxes.from_ax()
ax.bar(v.dv, v.vv, normed=True, opening=0.8, edgecolor='white')
ax.set_legend()