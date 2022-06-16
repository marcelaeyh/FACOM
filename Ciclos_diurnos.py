#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 23:44:38 2022

@author: mac
"""

import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sqlalchemy import create_engine
import numpy as np

eng_t = 'sqlite:////Users/mac/Desktop/local_facom/Volcan/db Meteoro/meteoro-turbo.db'
eng_o = 'sqlite:////Users/mac/Desktop/local_facom/Volcan/db Meteoro/meteoro-oriente.db'

eng = 'sqlite:////home/marcelae/Desktop/FACOM/2_db/presion.db'
#------------------------#----------------------------#-----------------------#

q = '''
SELECT DISTINCT CodigoEstacion
FROM presion 
'''
codigos = pd.read_sql(q,con=eng)

for i in codigos:

    query = '''
    SELECT FechaObservacion,ValorObservado
    WHERE CodigoEstacion = {}
    '''.format(i)

    df = pd.read_sql(query,con=eng)

    n=len(df)
    
    if n==0:
        continue
    
    fechainicial=df['FechaObservacion'].min()
    fechafinal=df['FechaObservacion'].max()
    
    print("Gráficos -",i)
    df = df.set_index(['FechaObservacion'])
    print("1. ciclo medio diurno-",i)
    
    diurno= df.ValorObservado.groupby(df.index.hour).mean()
    plt.figure(figsize=(10,5))    
    plt.plot(diurno,color="orange",label=str(i))
    plt.title(" Ciclo Medio Diurno de Presión \n "+str(fechainicial)+" - "+str(fechafinal),fontsize=15)
    plt.minorticks_on()
    plt.ylabel("Presion [hPa]", fontsize=12)
    plt.xlabel("Tiempo (horas)",fontsize=12)
    plt.xticks(np.arange(0, 24, step=1))
    plt.legend()
    plt.grid()