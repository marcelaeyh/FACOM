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

#Lucy
#eng = 'sqlite:////home/marcelae/Desktop/FACOM/2_db/presion.db'

#Marcela
eng = 'sqlite:////Volumes/DiscoMarcela/facom/presion.db'

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

mx = []
codigos = []
lon = []
volcan = pd.DataFrame(columns =['CodigoEstacion', 'NombreEstacion', 'Departamento', 'Municipio',
       'ZonaHidrografica', 'Latitud', 'Longitud'])

cont=0
for i in range(len(n)):
    estacion = df[df.CodigoEstacion == n[i]]
    estacion = estacion.reset_index(drop='index')
    if len(estacion.ValorObservado) > 24:
        
        condicion = estacion.ValorObservado == max(estacion.ValorObservado)
        maximo = estacion.ValorObservado[condicion]
        fecha = estacion.FechaObservacion[condicion]

        mx.append(fecha[fecha.index[0]])
        lon.append(estacion.Longitud[0])

        cod = estacion.CodigoEstacion.unique()
        codigos.append(cod[0])
    
        '''
        plt.figure(figsize=(10,5))
        plt.plot(estacion.FechaObservacion,estacion.ValorObservado,label=n[i])
        plt.title("Presion vs tiempo para el dia 15 de enero del 2022 "+str(cont),fontsize=20)
        plt.xlabel("Tiempo [Horas]",fontsize=15)
        plt.ylabel("Presión [hP]",fontsize=15)
        plt.grid()
        plt.legend()
        cont+=1
        
        #plt.savefig(r'/Users/mac/Desktop/FACOM/1_Proyectos/5_volcan/png/presion_15-01-2022'+str(n[i])+'.png') 
        plt.show()
        '''
        
        estacion = estacion.drop(columns = ["FechaObservacion","ValorObservado","DescripcionSensor","CodigoSensor","UnidadMedida"])
        estacion = estacion.drop_duplicates()
        volcan = volcan.append(estacion)
        
        
plt.figure(figsize=(9,5)) 
plt.plot(lon,mx,'o')
plt.title("Maximo pico de presion por longitud geográfica",fontsize=20)     
plt.xlabel("Longitud Geográfica [km]",fontsize=14)
plt.ylabel("Magnitud del pico maximo [hP]",fontsize=14)
plt.grid()
plt.savefig('/home/marcelae/Desktop/FACOM/1_Proyectos/5_volcan/png/max_km'+'.png') 


volcan.to_csv('/Users/mac/Desktop/FACOM/1_Proyectos/5_volcan/estaciones_10min.csv')
