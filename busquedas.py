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

co21 = []

for a in tqdm(cod.CodigoEstacion):
    qq = '''
    SELECT COUNT(ValorObservado)
    FROM presion
    WHERE FechaObservacion LIKE '01/15/2022%'
    AND CodigoEstacion == {}
    '''.format(a)
    
    co = pd.read_sql(qq,con=eng)
    
    if co['COUNT(ValorObservado)'][0] > 24:
        co21.append(a)
        
        
for a in tqdm(cod):

        q = '''
        SELECT FechaObservacion, ValorObservado
        FROM presion
        WHERE CodigoEstacion == {}
        AND FechaObservacion LIKE '01/%/2022%'
        '''.format(a)
        
        df = pd.read_sql(q,con=eng)
        
        df["FechaObservacion"]=pd.to_datetime(df['FechaObservacion'],format='%m/%d/%Y %I:%M:%S %p')
        df = df.sort_values("FechaObservacion")
        df = df.reset_index(drop='index')
        
        # anomalia otra **
        q2 = '''
        SELECT FechaObservacion, ValorObservado
        FROM presion
        WHERE CodigoEstacion == {}
        AND FechaObservacion LIKE '01/%'
        '''.format(a)
        
        
        eneros = pd.read_sql(q2,con=eng)
        
        eneros["FechaObservacion"]=pd.to_datetime(eneros['FechaObservacion'],format='%m/%d/%Y %I:%M:%S %p')
        eneros = eneros.sort_values("FechaObservacion")
        eneros = eneros.reset_index(drop='index')
        
        eneros["min"]=pd.to_datetime(eneros["FechaObservacion"]).dt.minute
        eneros["hour"]=pd.to_datetime(eneros["FechaObservacion"]).dt.hour
        eneros["day"]=pd.to_datetime(eneros["FechaObservacion"]).dt.day
        eneros["year"] = pd.to_datetime(eneros["FechaObservacion"]).dt.year
        
        df["min"]=pd.to_datetime(df["FechaObservacion"]).dt.minute
        df["hour"]=pd.to_datetime(df["FechaObservacion"]).dt.hour
        df["day"]=pd.to_datetime(df["FechaObservacion"]).dt.day
        
        #creamos las lista con los dates
        h=list(eneros["hour"].unique())
        h.sort()
        m=list(eneros["min"].unique())
        m.sort()
        d=list(eneros["day"].unique())
        d.sort()
        """
        # Analisis por minutos
        eneros_min = eneros[eneros.day==15]
        df_min = df[df.day==15]
        
        AN=[]
        ANE =[]
        mean = []
        
        for i in tqdm(h):
            for j in tqdm(m):
                minute = eneros_min[eneros_min.hour==i]
                minute=minute[minute["min"]==j]
                mean_h=minute["ValorObservado"].mean(skipna=True)
                desv = np.std(minute["ValorObservado"])
                
                años = len(eneros_min.year.unique())
                
                minute = df_min[df_min.hour==i]
                minute=minute[minute["min"]==j]
                vo = minute["ValorObservado"]
                
                if len(vo)!=0:
                    vo = vo[vo.index[0]]
                    AN.append(vo-mean_h)
                    ANE.append((vo-mean_h)/desv)
                    mean.append(mean_h)
                    
                    
        plt.figure(figsize=(15,18))
        
        plt.subplot(3,1,1)
        plt.plot(df_min.FechaObservacion,df_min.ValorObservado,color="darkorange",label="15 de enero de 2022")
        plt.plot(df_min.FechaObservacion,mean,'-',color="wheat",label="promedio todos los eneros de "+str(años)+" años")
        plt.title("Serie de tiempo - "+str(a),fontsize=15)
        plt.minorticks_on()
        plt.ylabel("Presión [hPa]", fontsize=12)
        plt.xlabel("Tiempo [horas]",fontsize=12)
        plt.legend()
        plt.grid()
        
        plt.subplot(3,1,2)
        plt.plot(df_min.FechaObservacion,ANE,color="darkorange")
        plt.title("Anomalia estandarizada - "+str(a),fontsize=15)
        plt.minorticks_on()
        plt.ylabel("Anomalía estandarizada", fontsize=12)
        plt.xlabel("Tiempo [horas]",fontsize=12)
        plt.grid()
        
        plt.subplot(3,1,3)
        plt.plot(df_min.FechaObservacion,AN,color="darkorange")
        plt.title("Anomalia - "+str(a),fontsize=15)
        plt.minorticks_on()
        plt.ylabel("Anomalía", fontsize=12)
        plt.xlabel("Tiempo [horas]",fontsize=12)
        plt.grid()
        
        plt.savefig(r"/home/marcelae/Desktop/graficos_prueba/minutos/63/"+str(a)+".png",dpi = 400)
        """
        # Analisis por horas
        eneros_h = eneros[eneros.day==15]
        df_h = df[df.day==15]
        
        AN=[]
        ANE =[]
        mean_t = []
        mean = []
        
        for i in tqdm(h):
        
            ho = eneros_h[eneros_h.hour==i]
            mean_h=ho["ValorObservado"].mean(skipna=True)
            desv = np.std(ho["ValorObservado"])
            años = len(eneros_h.year.unique())
            
            ho = df_h[df_h.hour==i]
            vo_m = ho["ValorObservado"].mean(skipna=True)
            
            if len(ho["ValorObservado"])!=0:
                AN.append(vo_m-mean_h)
                ANE.append((vo_m-mean_h)/desv)
                mean_t.append(mean_h)
                mean.append(vo_m)
            else:
                AN.append(np.nan)
                ANE.append(np.nan)
                mean_t.append(np.nan)
                mean.append(np.nan)
        
        
        plt.figure(figsize=(15,18))
        
        plt.subplot(3,1,1)
        plt.plot(h,mean,color="darkorange",label="15 de enero de 2022")
        plt.plot(h,mean_t,'-',color="wheat",label="promedio todos los eneros de "+str(años)+" años")
        plt.title("Promedio horario - "+str(a),fontsize=15)
        plt.ylabel("Presión [hPa]", fontsize=12)
        plt.xlabel("Tiempo [horas]",fontsize=12)
        plt.legend()
        plt.grid()
        
        
        plt.subplot(3,1,2)
        plt.plot(h,ANE,color="darkorange")
        plt.title("Anomalia estandarizada - "+str(a),fontsize=15)
        plt.minorticks_on()
        plt.ylabel("Anomalía estandarizada", fontsize=12)
        plt.xlabel("Tiempo [horas]",fontsize=12)
        plt.grid()
        
        plt.subplot(3,1,3)
        plt.plot(h,AN,color="darkorange")
        plt.title("Anomalia - "+str(a),fontsize=15)
        plt.minorticks_on()
        plt.ylabel("Anomalía", fontsize=12)
        plt.xlabel("Tiempo [horas]",fontsize=12)
        plt.grid()
        
        plt.savefig(r"/home/marcelae/Desktop/graficos_prueba/horas/63/"+str(a)+".png",dpi = 400)
        
        # Analisis por dias
        
        AN=[]
        ANE =[]
        mean_t = []
        mean = []
        
        for i in tqdm(d):
        
            dias = eneros[eneros.day==i]
            mean_h=dias["ValorObservado"].mean(skipna=True)
            desv = np.std(dias["ValorObservado"])
            años = len(eneros.year.unique())
            
            ho = df[df.day==i]
            vo_m = ho["ValorObservado"].mean(skipna=True)

            if len(dias["ValorObservado"])!=0:
                AN.append(vo_m-mean_h)
                ANE.append((vo_m-mean_h)/desv)
                mean_t.append(mean_h)
                mean.append(vo_m)
            else:
                AN.append(np.nan)
                ANE.append(np.nan)
                mean_t.append(np.nan)
                mean.append(np.nan)
        
        plt.figure(figsize=(15,18))
        
        plt.subplot(3,1,1)
        plt.plot(d,mean,color="darkorange",label="15 de enero de 2022")
        plt.plot(d,mean_t,'-',color="wheat",label="promedio todos los eneros de "+str(años)+" años")
        plt.title("promedio diario - "+str(a),fontsize=15)
        plt.ylabel("Presión [hPa]", fontsize=12)
        plt.xlabel("Tiempo [dias]",fontsize=12)
        plt.legend()
        plt.grid()
        
        plt.subplot(3,1,2)
        plt.plot(d,ANE,color="darkorange")
        plt.title("Anomalia estandarizada - "+str(a),fontsize=15)
        plt.minorticks_on()
        plt.ylabel("Anomalía estandarizada", fontsize=12)
        plt.xlabel("Tiempo [dias]",fontsize=12)
        plt.grid()
        
        plt.subplot(3,1,3)
        plt.plot(d,AN,color="darkorange")
        plt.title("Anomalia - "+str(a),fontsize=15)
        plt.minorticks_on()
        plt.ylabel("Anomalía", fontsize=12)
        plt.xlabel("Tiempo [dias]",fontsize=12)
        plt.grid()
        
        plt.savefig(r"/home/marcelae/Desktop/graficos_prueba/dias/63/"+str(a)+".png",dpi = 400)
        