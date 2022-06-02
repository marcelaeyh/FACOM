#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 18:47:36 2022

@author: luisa
"""
import pandas as pd
import  numpy as np
from datetime import datetime
from tqdm import tqdm              # libreria para saber el tiempo de ejecución
from sqlalchemy import create_engine
import os
import math
import matplotlib.pyplot as plt #Para graficar
import re
from unicodedata import normalize
import statistics as stat


#Información inicial
v=["FechaObservacion","ValorObservado","CodigoEstacion"]

datos=pd.read_csv(r"/media/luisa/Datos/FACOM/gits/FACOM/csv/Presi_n_Atmosf_rica.csv")
ESTACIONES= len(datos.CodigoEstacion.unique())
n=len(datos)
datos[v[0]]=pd.to_datetime(datos[v[0]],format='%m/%d/%Y %I:%M:%S %p')
Finicial=datos[v[0]].min()
Ffinal=datos[v[0]].max()
datos = datos.sort_values(by=v[0]).reset_index(drop=True)
#####ESTADISTICAS####
maxi=datos.ValorObservado.max()
mini=datos.ValorObservado.min()
media=datos.ValorObservado.mean()
desviacion=np.std(datos.ValorObservado)
mediana=np.median(datos.ValorObservado)

k=datos.ValorObservado
moda=stat.mode(k)
p01_t=np.percentile(k,1)
p02_t=np.percentile(k,2)
p98_t=np.percentile(k,98)
p99_t=np.percentile(k,99)

print("")
print("ESTADISTICOS")
print("")
print("moda=",moda)
print("15. Valor máximo= ", maxi)
print("16. Valor mínimo= ", mini)
print("17. Valor medio= ", media)
print("18. Desviación estandar", desviacion)
print("19. Mediana= ", mediana)
print("El percentil 1= ",round(p01_t,3))
print("El percentil 2= ",round(p02_t,3))
print("El percentil 98= ",round(p98_t,3))
print("El percentil 99= ",round(p99_t,3))

#histograma
num_bins = 30
plt.figure(figsize=(10,5))
plt.title("IDEAM-Presion (Hpa)",fontsize=15)
plt.hist(datos["ValorObservado"], num_bins,facecolor = "slateblue",
         alpha=0.75,label="T",edgecolor = "gray")

plt.axvline(x=media,color="black",linewidth=1.0,linestyle='-',label=('Media=',round(media,3)))
plt.axvline(x=mediana,color="black",linewidth=1.0,linestyle='--',
            label=('Mediana=',round(mediana,3)))
plt.ylabel("Frecuencia (pr)", fontsize=10)
plt.xlabel("Presion [Hpa]", fontsize=10)
#plt.title("Muestra 1")
plt.grid(color='lightgrey',linewidth=1.0)
#plt.text(1, 65, 'A', fontsize = 15,
#         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.minorticks_on()
plt.legend()

#caja de bigotes
datos.boxplot(column="ValorObservado",figsize=(8, 5))
plt.title("IDEAM") 
plt.xticks([1],["Presion"])
plt.ylabel("Presion [Hpa]", fontsize=12)
plt.xlabel("Presion",fontsize=12)

# Valores observador por debajo del percentil 02
vp02=datos[datos[v[1]]<=p02_t]
vp02=pd.DataFrame(vp02)
vp02_uniques=vp02[v[2]].unique()

#graficos
for i in range(len(vp02_uniques)):
    cod=vp02_uniques[i]
    print(cod)
    k=vp02[vp02[v[2]]==cod]
    plt.figure(figsize=(10,5))
    plt.title("Serie de tiempo -Presión \n Código Estación"+str(cod))
    plt.ylabel("Presión [Hpa]")
    plt.xlabel("Tiempo")
    plt.grid()
    plt.minorticks_on()
    plt.plot(k.FechaObservacion,k.ValorObservado,color="mediumvioletred")
    plt.legend()
    plt.savefig(r"/media/luisa/Datos/FACOM/gits/FACOM/Proyectos/Presion/png/presion-"+str(cod)+".png")

    

cod=vp02_uniques[2]
print(cod)
k=vp02[vp02[v[2]]==cod].reset_index(drop=True)

fi=k["FechaObservacion"].min()
ff=k["FechaObservacion"].max()
k1=pd.DataFrame(pd.date_range(start=fi, end=ff, freq='min'),columns=["fecha"])
k1["valor"]=np.nan
k1
p=0
for i in tqdm(range(len(k))):
    fk=k["FechaObservacion"][i]
    for j in range(p,len(k1)):
        fk1=k1["fecha"][j]
        if fk1==fk :
            k1.valor[j]=k.ValorObservado[i]
            p=j
            print(i)
            break
            
            
plt.plot(k1.fecha,k1.valor,linestyle="dashdot")



k1
k["FechaObservacion"]
k=pd.DataFrame(k)
k2=k.set_index(pd.DatetimeIndex(k["FechaObservacion"])).drop("FechaObservacion",axis=1)
k['season'] = k['FechaObservacion'].dt.month

k.ValorObservado
k3=k2.resample("M").mean().reset_index()
plt.plot(k.FechaObservacion,k.ValorObservado)

k2.ValorObservado

#guardar e información
vp02_uniques[0]
n=len(vp02_uniques)
m=datos[datos[v[2]]==57015010]

cat=pd.read_csv(r"/media/luisa/Datos/FACOM/gits/FACOM/otros_documentos/Cat_logo_Nacional_de_Estaciones_del_IDEAM.csv")
cat

V=[]
alt=0
for i in tqdm(range(n)):
    cod=vp02_uniques[i]
    m=datos[datos[v[2]]==cod]
    print(m.Departamento.unique())
    lat=m.Latitud.unique()
    lot=m.Longitud.unique()
    dep=m.Departamento.unique()
    mun=m.Municipio.unique()
    for j in range(len(cat)):
        if cat.Codigo[j]==cod:
            alt=cat.Altitud[j]
            break
            
    vector=[cod,lat[0],lot[0],dep[0],mun[0],alt[0]]
    print(vector)
    V.append(vector)
    
V=pd.DataFrame(V)
V.columns=["cod","lat","lon","dep","mun","alt"]
V.to_csv(r"/media/luisa/Datos/FACOM/gits/FACOM/Proyectos/Presion/valores_p02.csv",sep=";")
vp02

p02_t
vp02_uniques
