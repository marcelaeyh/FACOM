# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 21:23:37 2022

@author: USER
"""

#librerias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#funciones
def siata(csv,guardar):
    m01=pd.read_csv(csv)
    m01.columns = ['Index','fecha_hora', 'pm25', 'Calidad']
    m01['fecha']= pd.to_datetime(m01['fecha_hora']).dt.normalize()
    
    #m01['fecha_hora']= pd.to_datetime(m01['fecha_hora']).date()
    #m01['day'] = m01['fecha_hora'].dt.day
    #m01['month'] = m01['fecha_hora'].dt.month 
    #m01['year'] = m01['fecha_hora'].dt.year 
    
    
    count=0 #se guarda la cantidad de dias
    countval=0
    desc=0 #se guardan cuantos son menores a 2.6
    sumval1=0
    sumval2=0
    tdate=""
    res=[]
    
    dsres = pd.DataFrame()
    
    fecha=m01["fecha"].unique()
    #dias=m01['day'].unique()
    #month=m01['month'].unique()
    #year=m01['year'].unique()

    
    for i in range(len(fecha)):
        f=fecha[i]
        for index, row in m01.iterrows(): # row guarda la fila donde esta, y recorre todas las filas.
            if(row['fecha']==f):
                count+=1
                if(row['Calidad'] < 2.6):
                    countval+=1
                    sumval1=sumval1+row['pm25'] # agregar el numero de variables que se quieren promediar
                
        if((count-countval) < count*0.25):
            auxres={'pm25':sumval1/count,'fecha':f}
            dsres=dsres.append(auxres, ignore_index = True)
        else:
            auxres={'pm25':-999,'fecha':f}
            dsres=dsres.append(auxres, ignore_index = True)

        count=0
        countval=0
        desc=0
        sumval1=0
        sumval2=0
        sumval3=0
        sumval4=0
    
    dsres.to_csv('D:/Ubuntu/AD/Tfinal/'+guardar+".csv")
    return(dsres)

direccion="D:/Ubuntu/AD/Tfinal/datos completos/originales/12_CA_2014-2021.csv"


df_nuevo=siata(direccion,"12AC_Promediosdiarios_2014-2018")