#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 09:42:41 2022

@author: mac
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
eng = 'sqlite:////home/marcelae/Desktop/FACOM/2_db/presion.db'

#Marcela
#eng = 'sqlite:////Volumes/DiscoMarcela/facom/presion.db'

query='''
SELECT DISTINCT CodigoEstacion FROM presion
'''

cod = pd.read_sql(query,con=eng)

for i in tqdm(cod.CodigoEstacion):
    q = '''
    SELECT FechaObservacion, ValorObservado
    FROM presion
    WHERE CodigoEstacion == {}
    '''.format(i)
    
    df = pd.read_sql(q,con=eng)
    
    df["FechaObservacion"]=pd.to_datetime(df['FechaObservacion'],format='%m/%d/%Y %I:%M:%S %p')
    df = df.sort_values("FechaObservacion")
    df = df.reset_index(drop='index')
    
    fechainicial=df["FechaObservacion"].min()
    fechafinal=df["FechaObservacion"].max()
    df["year"]=pd.to_datetime(df["FechaObservacion"]).dt.year 
    df["month"]=pd.to_datetime(df["FechaObservacion"]).dt.month 
    df["day"]=pd.to_datetime(df["FechaObservacion"]).dt.day
    df["hour"]=pd.to_datetime(df["FechaObservacion"]).dt.hour
    #creamos las lista con los dates
    h=list(df["hour"].unique())
    h.sort()
    d=list(df["day"].unique())
    d.sort()
    month=list(df["month"].unique())
    month.sort()
    y=list(df["year"].unique())
    y.sort()
    
    #Anomalia
    prom = df.ValorObservado.mean()
    desv = np.std(df.ValorObservado)
    
    datos = []
    
    for j in tqdm(df.ValorObservado):
        ae = (j-prom)/desv
        datos.append(ae)
    
    plt.figure(figsize=(10,5))
    plt.plot(df.FechaObservacion,datos,color="orange",label=str(i))
    plt.title("Anomalia Estandarizada - "+str(i),fontsize=15)
    plt.minorticks_on()
    plt.ylabel("Anomalía estandarizada", fontsize=12)
    plt.xlabel("TTiempo [años]",fontsize=12)
    plt.legend()
    plt.grid()
    
    plt.savefig(r"/home/marcelae/Desktop/FACOM/7_png/3_PresionCompleto/Anomalias/anomalia_estandarizada "+str(cod)+".png",dpi = 400)