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
WHERE FechaObservacion LIKE '01/15/2022%'
'''

cod = pd.read_sql(query,con=eng)

for i in tqdm(cod.CodigoEstacion):
    qq = '''
    SELECT COUNT(ValorObservado)
    FROM presion
    WHERE FechaObservacion LIKE '01/15/2022%'
    AND CodigoEstacion == {}
    '''.format(i)
    
    co = pd.read_sql(qq,con=eng)
    
    if co['COUNT(ValorObservado)'][0] > 24:
        q = '''
        SELECT FechaObservacion, ValorObservado
        FROM presion
        WHERE CodigoEstacion == {}
        AND FechaObservacion LIKE '01/15/2022%'
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
            if desv ==0:
                continue
            ae = (j-prom)/desv
            datos.append(ae)
        
        plt.figure(figsize=(10,5))
        plt.plot(df.FechaObservacion,datos,color="orange",label=str(i))
        plt.title("Anomalia Estandarizada - "+str(i),fontsize=15)
        plt.minorticks_on()
        plt.ylabel("Anomalía estandarizada", fontsize=12)
        plt.xlabel("Tiempo [horas]",fontsize=12)
        plt.legend()
        plt.grid()
        
        plt.savefig(r"/home/marcelae/Desktop/graficos_prueba/ "+str(i)+".png",dpi = 400)