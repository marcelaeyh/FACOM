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
v=["FechaObservacion"]

datos=pd.read_csv(r"/media/luisa/Datos/FACOM/Presi_n_Atmosf_rica.csv")
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

# Valores observador por debajo del percentil 98
p99_t
