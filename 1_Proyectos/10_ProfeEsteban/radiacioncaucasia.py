#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 16:34:52 2022

@author: luisa
"""
################################ 1. LIBRERIAS ################################

import pandas as pd                  # Análisis de los datos  
from tqdm import tqdm                # Tiempo de ejecución
from sqlalchemy import create_engine # Conexión con la base de datos
import matplotlib.pyplot as plt      # Gráficar
import numpy as np                   # Matemáticas
import datetime                      # Manipulación de datos "fecha"
import scipy     
from scipy import stats
from datetime import datetime
################################ 2. FUNCIONES ################################ 
datos= pd.read_csv(r"/home/luisa/Downloads/excel.csv.csv", usecols=[16,17])
datos["Fecha"]=pd.to_datetime(datos["Fecha"])
datos["year"]=pd.to_datetime(datos["Fecha"]).dt.year
datos["month"]=pd.to_datetime(datos["Fecha"]).dt.month
datos["day"]=pd.to_datetime(datos["Fecha"]).dt.day
datos["hour"]=pd.to_datetime(datos["Fecha"]).dt.hour 
y=list(datos["year"].unique())
month=list(datos["month"].unique())
d=list(datos["day"].unique())
h=list(datos["hour"].unique()) 
y.sort()
month.sort()
d.sort()
h.sort()

fi=datos["Fecha"].min()
ff=datos["Fecha"].max()
print(datos["Fecha"].min())
print(datos["Fecha"].max())
print(datos["Valor"].mode())
nombrecolumnavariable="Valor"

v=datos


v1=pd.DataFrame(pd.date_range(start=fi,end=ff,freq="H"),columns=["fecha"]) 
v1[nombrecolumnavariable]=np.nan  # Columna para la variable
for i in tqdm(y):
    for ii in month:
        for iii in d:
            for iv in h:
                acumulado=v[v.year==i][v.month==ii][v.day==iii][v.hour==iv]
                acumulado=acumulado.reset_index()
                if len(acumulado)==0.0:
                    continue
                # Indice de la fecha del C.teórico, donde la fecha del C.teórico 
                # sea igual a la del C.real.
                indice=v1.index[v1["fecha"]==str(acumulado["Fecha"][0])].tolist() 
                # Se reemplaza el Nan del C.teórico por el valor del C.real 
                v1[nombrecolumnavariable][indice[0]]=acumulado["Valor"][0]
v1["year"]=pd.to_datetime(v1["fecha"]).dt.year   # crea una columna con los años.
v1["month"]=pd.to_datetime(v1["fecha"]).dt.month # crea una columna con los meses.
v1["day"]=pd.to_datetime(v1["fecha"]).dt.day     # crea una columna con los dias.
v1["hour"]=pd.to_datetime(v1["fecha"]).dt.hour   # crea una columna con los hora.


plt.figure(figsize=(10,5)) 
plt.plot(v1.fecha,v1.Valor,color="#0504aa",label=("26255030"))
plt.title(" Serie de Tiempo \n Radiación - "+ str(fi)+" - "+str(ff),fontsize=15)
plt.minorticks_on()
plt.ylabel("Valor ", fontsize=12)
plt.xlabel("Tiempo (horas)",fontsize=12)
#plt.xticks(np.arange(0, 24, step=1))
plt.legend()
plt.grid()

num_bins=20
plt.figure(figsize=(10,5))
import seaborn as sb
sb.displot(datos.Valor, color='#F2AB6D', bins=20, kde=True) #creamos el gráfico en Seaborn
plt.title(" Histograma \n Radiación ",fontsize=15)
plt.ylabel("Frecuencia (Pr) ", fontsize=12)
plt.xlabel("Valor de radiacion",fontsize=12)
plt.legend()
plt.grid()





plt.minorticks_on()
plt.ylabel("Frecuen ", fontsize=12)
plt.xlabel("Tiempo (horas)",fontsize=12)
#plt.xticks(np.arange(0, 24, step=1))
plt.legend()
plt.grid()
v1.columns=("fecha","radiación","year","month","day","hour")



meses=["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"]
vector=[1,2,3,4,5,6,7,8,9,10,11,12]

m1= v1[v1.month==1]
m2= v1[v1.month==2]
m3= v1[v1.month==3]
m4= v1[v1.month==4]
m5= v1[v1.month==5]
m6= v1[v1.month==6]
m7= v1[v1.month==7]
m8= v1[v1.month==8]
m9= v1[v1.month==9]
m10= v1[v1.month==10]
m11= v1[v1.month==11]
m12= v1[v1.month==12]
m13=v1[v1.hour>=6][v1.hour<=18]


m13.boxplot(column="radiación",by="month",figsize=(8, 5))
plt.title("RH (6hr - 18hr) ",loc=("left"))
plt.minorticks_on()
plt.ylabel("Valor de radiación ", fontsize=12)
plt.xlabel("Tiempo(HL)",)
plt.xticks(vector,meses)
plt.legend()
plt.grid()

plt.figure(figsize=(15,10))
#enero
m1.boxplot(column="radiación",by="hour",figsize=(8, 5))
plt.title("a) Enero ",loc=("left"))
plt.minorticks_on()
plt.ylabel("Valor de radiación ", fontsize=12)
plt.xlabel("Tiempo(HL)")
#febrero
plt.figure(figsize=(15,10))
m2.boxplot(column="radiación",by="hour",figsize=(8, 5))
plt.title("b) Febero ",loc=("left"))
plt.minorticks_on()
plt.ylabel("Valor de radiación ", fontsize=12)
plt.xlabel("Tiempo(HL)")
#marzo
plt.figure(figsize=(15,10))
m3.boxplot(column="radiación",by="hour",figsize=(8, 5))
plt.title("c) Marzo ",loc=("left"))
plt.minorticks_on()
plt.ylabel("Valor de radiación ", fontsize=12)
plt.xlabel("Tiempo(HL)")
#Abril
plt.figure(figsize=(15,10))
m4.boxplot(column="radiación",by="hour",figsize=(8, 5))
plt.title("d) Abril ",loc=("left"))
plt.minorticks_on()
plt.ylabel("Valor de radiación ", fontsize=12)
plt.xlabel("Tiempo(HL)")
#Mayo
plt.figure(figsize=(15,10))
m5.boxplot(column="radiación",by="hour",figsize=(8, 5))
plt.title("e) Mayo ",loc=("left"))
plt.minorticks_on()
plt.ylabel("Valor de radiación ", fontsize=12)
plt.xlabel("Tiempo(HL)")
#Junio
plt.figure(figsize=(15,10))
m6.boxplot(column="radiación",by="hour",figsize=(8, 5))
plt.title("f) Junio ",loc=("left"))
plt.minorticks_on()
plt.ylabel("Valor de radiación ", fontsize=12)
plt.xlabel("Tiempo(HL)")
#Julio
plt.figure(figsize=(15,10))
m7.boxplot(column="radiación",by="hour",figsize=(8, 5))
plt.title("g) Julio ",loc=("left"))
plt.minorticks_on()
plt.ylabel("Valor de radiación ", fontsize=12)
plt.xlabel("Tiempo(HL)")
#Agosto
plt.figure(figsize=(15,10))
m8.boxplot(column="radiación",by="hour",figsize=(8, 5))
plt.title("h) Agosto ",loc=("left"))
plt.minorticks_on()
plt.ylabel("Valor de radiación ", fontsize=12)
plt.xlabel("Tiempo(HL)")
#Septiembre
plt.figure(figsize=(15,10))
m9.boxplot(column="radiación",by="hour",figsize=(8, 5))
plt.title("i) Septiembre ",loc=("left"))
plt.minorticks_on()
plt.ylabel("Valor de radiación ", fontsize=12)
plt.xlabel("Tiempo(HL)")
#Octubre
plt.figure(figsize=(15,10))
m10.boxplot(column="radiación",by="hour",figsize=(8, 5))
plt.title("j) Octubre ",loc=("left"))
plt.minorticks_on()
plt.ylabel("Valor de radiación ", fontsize=12)
plt.xlabel("Tiempo(HL)")
#Noviembre
plt.figure(figsize=(15,10))
m11.boxplot(column="radiación",by="hour",figsize=(8, 5))
plt.title("k) Noviembre ",loc=("left"))
plt.minorticks_on()
plt.ylabel("Valor de radiación ", fontsize=12)
plt.xlabel("Tiempo(HL)")
#Diciembre
plt.figure(figsize=(15,10))
m12.boxplot(column="radiación",by="hour",figsize=(8, 5))
plt.title("l) Diciembre ",loc=("left"))
plt.minorticks_on()
plt.ylabel("Valor de radiación ", fontsize=12)
plt.xlabel("Tiempo(HL)")




