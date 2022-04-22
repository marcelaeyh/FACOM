#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:11:05 2022

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

#  2.3 información de la base de datos
eng = 'sqlite:////home/luisab/Documents/FACOM/DATA.db'

#------------------------#----------------------------#-----------------------#
#3. funciones

#3.1 Extracción de datos de un database
# Load de data
def SQL_PD(table_or_sql,eng):
       engine = create_engine(eng)
       conn = engine.connect()
       generator_object = pd.read_sql(table_or_sql,con=conn)
       return generator_object 
   
    
cod = 25025380

my_query2='''
SELECT CodigoEstacion,FechaObservacion,ValorObservado,NombreEstacion,Departamento,
Municipio,ZonaHidrografica,Latitud,Longitud,DescripcionSensor,UnidadMedida 
FROM precipitacion
WHERE (codigoestacion = {})
'''.format(int(cod))

df_est = SQL_PD(my_query2,eng)

df_est["fecha"]=pd.to_datetime(df_est['FechaObservacion']).dt.strftime("%d/%m/%Y %X")
#organizar las filas de mayor a menor con respecto a la fecha
df_est = df_est.sort_values(by='fecha')
#Se resetean los indices
df_est=df_est.reset_index(drop=True)
#longitud de filas
n=len(df_est)
#longitud de columnas
shape = df_est.shape
#Obtener el nombre de las columnas
columns_names = df_est.columns.values
#latitud y longitud
lat=df_est.Latitud.unique()
lon=df_est.Longitud.unique()
#Municipio y departamento
mu=df_est.Municipio.unique()
dep=df_est.Departamento.unique()
#Zona hidrografica y nombre de la estación
zh=df_est.ZonaHidrografica.unique()
ne=df_est.NombreEstacion.unique()
#descrición del sensor y unidades
desS=df_est.DescripcionSensor.unique()
unidades=df_est.UnidadMedida.unique()


print("Estación",cod)
print("")
print("INFORMACIÓN INICIAL")
print("")
print("1. La fecha inicial =",df_est["fecha"][0] )
print("2. La fecha final =",df_est["fecha"][n-1] )
print("3. La cantidad de filas y columnas =",shape )
print("4. El nombre de las columnas es=",columns_names)
print("5. Las primeras filas son= ")
print(df_est.head())
print("6. Las últimas filas= ")
print(df_est.tail())
print("")
print("LATITUD Y LONGITUD")
print("")
print("7. latitud=", lat[0])
print("8. longitud=", lon[0])
print("")
print("MUNICIPIO, DEPARTAMENTO, ZONA HIDROGRAFICA Y NOMBRE DE LA ESTACIÓN")
print("")
print("9. Municipio= ", mu[0])
print("10. Departamento= ", dep[0])
print("11. Zona Hidrografica= ", zh[0])
print("12. Nombre de la estación= ", ne[0])
print("")
print("UNIDADES Y OTRAS DESCRIPCIONES")
print("")
print("13. Unidades de la variable de estudio= ", unidades[0])
print("14. Descripción del sensor= ", desS[0])
print("")
    
#CALCULOS
#max, min, promedio
#Valor máximo
maxi=df_est.ValorObservado.max()
mini=df_est.ValorObservado.min()
media=df_est.ValorObservado.mean()
desviacion=np.std(df_est.ValorObservado)
mediana=np.median(df_est.ValorObservado)


print("")
print("ESTADISTICOS")
print("")
print("15. Valor máximo= ", maxi)
print("16. Valor mínimo= ", mini)
print("17. Valor medio= ", media)
print("18. Desviación estandar", desviacion)
print("19. Mediana= ", mediana)



df_est.head(20)

df_est["year"]=pd.to_datetime(df_est['fecha']).dt.year 
df_est["month"]=pd.to_datetime(df_est['fecha']).dt.month
df_est["day"]=pd.to_datetime(df_est['fecha']).dt.day  
df_est["hour"]=pd.to_datetime(df_est['fecha']).dt.hour
month=list(df_est["month"].unique())
month.sort() 
Ma_mes=[]
for i in tqdm(month):
    mes=df_est[df_est.month==i]
    mean_m=mes.ValorObservado.mean(skipna=True)
    Ma_mes.append(mean_m)
    print("Ingresa el promedio del mes",i)
meses=np.array(["Ene","Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", 
                "Sep","Oct", "Nov", "Dic"])
print("")
print("GRAFICOS")
print("")
plt.figure(figsize=(10,5))
plt.title("Ciclo medio anual \n Estación" )
plt.plot(meses,Ma_mes)
plt.xlabel("tiempo (meses)")
plt.ylabel("precipitación "+unidades)
plt.grid()


titulos=["Codigo Estacion","Nombre de estacion","Municipio","Departamento", "Zona Hidrográfica","Latitud"
         ,"Longitud","Fecha Inicial","Fecha Final","Numerofilas","Numero de columnas",
         "Máximo","Mínimo","Promedio","Desviación Estándar","Mediana"]
c=[cod,ne,mu,dep,zh,lat,lon,df_est["fecha"][0],df_est["fecha"][n-1],n,shape,maxi,mini,media,desviacion,mediana]




