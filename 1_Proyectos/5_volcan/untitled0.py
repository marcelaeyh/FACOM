#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 22:38:57 2022

@author: mac
"""

import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sqlalchemy import create_engine
import numpy as np
from tqdm import tqdm  

#------------------------#----------------------------#-----------------------#
# Estaciones IDEAM
eng = 'sqlite:////home/marcelae/Desktop/FACOM/2_db/presion.db'

qu = '''
SELECT DISTINCT CodigoEstacion FROM presion
WHERE FechaObservacion LIKE '01/1%/2022%'
'''
cod = pd.read_sql(qu,con=eng)


for a in range(0,18,6):
    plt.figure(figsize=(25,20))
    m=1
    for j in range(a+1,a+7):
        i = cod.CodigoEstacion[j]
        
        q = '''
        SELECT *
        FROM presion 
        WHERE FechaObservacion LIKE '01/1%/2022%'
        AND CodigoEstacion == {}
        '''.format(int(i))
        
        df = pd.read_sql(q,con=eng)
    
        df["FechaObservacion"]=pd.to_datetime(df['FechaObservacion'],format='%m/%d/%Y %I:%M:%S %p')
        df = df.sort_values("FechaObservacion")
        df = df.reset_index(drop='index')
        
        # Pasar a UTC
        df.FechaObservacion = df.FechaObservacion + datetime.timedelta(hours=5)
        
        oi = df[df.FechaObservacion >= '2022-01-15 00:00:00']
        of = df[df.FechaObservacion <= '2022-01-15 23:59:59']
        
        df = df[oi.index[0]:of.index[-1]]
        df = df.reset_index(drop='index')
        
        #plt.figure(figsize=(15,15))
        
        plt.subplot(3,2,m)
        plt.plot(df.FechaObservacion,df.ValorObservado,label='Code = '+str(int(i)))
        plt.title("Pressure [hPa] vs Time [hours] in "+df.Municipio.unique()[0]+" on January 15th 2022 (UTC) " ,fontsize="16")
        plt.xlabel("Time [Hours]",fontsize="16")
        plt.ylabel("Pressure [hPa]",fontsize="16")
        plt.grid()
        plt.legend()
        m+=1  
    plt.savefig('/home/marcelae/Desktop/FACOM/1_Proyectos/5_volcan/ga/fig'+str(a)+'.png')