#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fecha: 18 de abril de 2022
lugar: Medellín-Antioquía
Autores: Marcela y Luisa Fernanda Buriticá Ruíz

El proposito de este codigo es analizar dos bases de datos de precipitación
y temperatura del IDEAM. 
"""

#------------------------#----------------------------#-----------------------#
#  1. importar las librerías

import pandas as pd
import  numpy as np
from datetime import datetime
from tqdm import tqdm              # libreria para saber el tiempo de ejecución
from sqlalchemy import create_engine
import os
import math
#------------------------#----------------------------#-----------------------#
#  2. leer las bases de datos
#Si la base de datos ya esta creada por favor agregar # para comentar las 
#lineas ya que no se usaran.

p="/home/luisab/Documents/FACOM/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv" 
t="/home/luisab/Documents/FACOM/Precipitaci_n.csv"

#2.1 información de las columnas 
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

#CodigoEstacion,FechaObservacion,ValorObservado,NombreEstacion,
#Departamento,Municipio,ZonaHidrografica,Latitud,Longitud

# 2.2 Crear la base de datos

#cambiar por "p" o por "t" según la información que se desee cargar
k=pd.read_csv(p,usecols=[0])    #Se crea una variable que contenga la longitud del archivo original
n=len(k)                        #longitud de la columna de prueba
k.head()
del k

data_base_name = "DATA.db"    # se asigna un nombre al db
engine = create_engine('sqlite:///'+data_base_name)     # se crea el motor 
sqlite_connection = engine.connect()                    # se enciende la conexión
step=math.ceil(n*0.01)             # el número es el porcentaje que se va a tomar "dx"
cont=0                  #contador

#Se crea el while que recorra el DataFrame y lo vaya ingresando cada dx
while tqdm(cont <= (n-1)):  
    #La siguiente fila de codigo lo que carga es el dx, se toma una porción y solo se carga
    #el porcentaje que se desea cargar que inicialmente se asigno en cada paso. 
    v=pd.read_csv(p,nrows=int(step),skiprows=range(1,int(cont)))
    print("ingresando paso",cont)
    v.to_sql(name='temperatura',con=sqlite_connection,index=False,if_exists='append') 
    cont=cont+step
    del v
    #print(cont,"_",step)
    
sqlite_connection.close()   


#  2.3 información de la base de datos
eng = 'sqlite:///DATA.db'

#------------------------#----------------------------#-----------------------#
#3. funciones

#3.1 Extracción de datos de un database
# Load de data
def SQL_PD(table_or_sql,eng):
       engine = create_engine(eng)
       conn = engine.connect()
       generator_object = pd.read_sql(table_or_sql,con=conn)
       return generator_object 

#------------------------#----------------------------#-----------------------#
#  4. se genera el archivo con la informaición por estación
my_query1='''
SELECT CodigoEstacion FROM temperatura
WHERE 
'''
codigo = SQL_PD(my_query1,eng)

print(" se empieza a leer por columna")
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
    print("5", df.head())
        
    del df_est




#------------------------#----------------------------#-----------------------#
#------------------------#----------------------------#-----------------------#
#------------------------#----------------------------#-----------------------#
#------------------------#----------------------------#-----------------------#
#------------------------#----------------------------#-----------------------#