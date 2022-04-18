#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 14:45:03 2022

@author: luisa
"""
#------------------------------------------------------------------------------
#1. IMPORTAR LIBRERIAS
import pandas as pd
import  numpy as np
from datetime import datetime
from tqdm import tqdm # libreria para saber el tiempo de ejecución
from sqlalchemy import create_engine
import os
import math
#-----------------------------------------------------------------------------
#2. LECTURAS DE DATOS
# 0-CodigoEstacion
# 1-CodigoSensor
# 2-FechaObservacion
# 3-ValorObservado
# 4-NombreEstacion
# 5-Departamento
# 6-Municipio
# 7-ZonaHidrografica
# 8-Latitud
# 9-Longitud
# 10-DescripcionSensor
# 11-UnidadMedida

#CodigoEstacion,FechaObservacion,ValorObservado,NombreEstacion,Departamento,Municipio,ZonaHidrografica,Latitud,Longitud

 
#-----------------------------------------------------------------------------
#3. FUNCIONES

#3.1 EXTRACCIÓN DE DATOS DE DATABASE
# Load de data
def SQL_PD(table_or_sql,eng):
       engine = create_engine(eng)
       conn = engine.connect()
       generator_object = pd.read_sql(table_or_sql,con=conn)
       return generator_object


#-----------------------------------------------------------------------------

#4. ANALIZAR EL FUNCIONAMIENTO DEL SQL_PD

my_query='''
SELECT CodigoEstacion,FechaObservacion,ValorObservado,NombreEstacion,Departamento,
Municipio,ZonaHidrografica,Latitud,Longitud 
FROM precipitacion
WHERE (codigoestacion = '25025380')
'''
eng = 'sqlite:///DATA.db'

#Se carga el DF con las especificaciones anteriores
df_25025380 = SQL_PD(my_query,eng)
#Convertir a datatime
df_25025380["fecha"]=pd.to_datetime(df_25025380['FechaObservacion']).dt.strftime("%d/%m/%Y %X")
#organizar las filas de mayor a menor con respecto a la fecha
df_25025380 = df_25025380.sort_values(by='fecha')
#Se resetean los indices
df_25025380=df_25025380.reset_index(drop=True)
#longitud de filas
n=len(df_25025380)
#longitud de columnas
shape = df_25025380.shape
#Obtener el nombre de las columnas
columns_names = df_25025380.columns.values

print("Estación 25025380")
print("1. La fecha inicial =",df_25025380["fecha"][0] )
print("2. La fecha final =",df_25025380["fecha"][n-1] )
print("3. La cantidad de filas y columnas =",shape )
print("4. El nombre de las columnas es=",columns_names)

df_25025380.head()
df_25025380.tail()
df_25025380.index()

print("1. La fecha inicial para la estación 25025380 es",df_25025380["fecha"][0] )

df_25025380

m1=sorted(df_25025380["fecha"], reverse=False)
m1=pd.DataFrame(m1)

m1.tail()
#df_25025380["fecha"].sorted()


# Leer varias estaciones
#DataFrame con codigos de estacion

my_query1='''
SELECT CodigoEstacion
FROM precipitacion
WHERE (codigoestacion = '25025380')
'''

codigo = SQL_PD(my_query1,eng)

for i in tqdm(range(3)):
    
    cod = codigo["CodigoEstacion"][i]
    
    my_query2='''
    SELECT CodigoEstacion,FechaObservacion,ValorObservado,NombreEstacion,Departamento,
    Municipio,ZonaHidrografica,Latitud,Longitud 
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
    
    print("Estación",cod)
    print("1. La fecha inicial =",df_est["fecha"][0] )
    print("2. La fecha final =",df_est["fecha"][n-1] )
    print("3. La cantidad de filas y columnas =",shape )
    print("4. El nombre de las columnas es=",columns_names)
        
    del df_est









