#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 12:38:23 2022

@author: marcelae
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

eng = 'sqlite:////home/marcelae/Desktop/FACOM/2_db/presion.db'

q = '''
SELECT *
FROM presion 
WHERE FechaObservacion 
LIKE '01/15/2022%'
'''
df = pd.read_sql(q,con=eng)
df["FechaObservacion"]=pd.to_datetime(df['FechaObservacion'],format='%m/%d/%Y %I:%M:%S %p')
df = df.sort_values("FechaObservacion")

n = df.CodigoEstacion.unique()
len(n)
mx = []
lon = []
for i in range(len(n)):
    estacion = df[df.CodigoEstacion == df.CodigoEstacion[i]]
    #if len(estacion.ValorObservado) > 24:
    mx.append(estacion.FechaObservacion[estacion.ValorObservado == max(estacion.ValorObservado)])
    lon.append(estacion.Longitud[estacion.ValorObservado == max(estacion.ValorObservado)])
    
    cod = estacion.CodigoEstacion.unique()
    
    plt.figure(figsize=(10,5))
    plt.plot(estacion.FechaObservacion,estacion.ValorObservado,label=cod[0])
    plt.title("Presion vs tiempo para el dia 15 de enero del 2022",fontsize=20)
    plt.xlabel("Tiempo [Horas]",fontsize=15)
    plt.ylabel("Presión [hP]",fontsize=15)
    plt.grid()
    plt.legend()
    
    plt.savefig('/home/marcelae/Desktop/FACOM/1_Proyectos/5_volcan/png_completos/presion_15-01-2022_'+str(cod[0])+'.png') 
    
plt.figure(figsize=(9,5)) 
plt.plot(lon,mx,'o')
plt.title("Fecha del pico maximo de la anomalia por longitud geográfica",fontsize=20)     
plt.xlabel("Longitud Geográfica [°]",fontsize=14)
plt.ylabel("Fecha del pico maximo [min]",fontsize=14)
plt.grid()
plt.savefig('/home/marcelae/Desktop/FACOM/1_Proyectos/5_volcan/png_completos/longitudes'+'.png') 

