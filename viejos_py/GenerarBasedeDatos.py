#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 15:24:54 2022

Generación de base da datos
"""
#------------------------------------------------------------------------------
#1. IMPORTAR LIBRERIAS
import pandas as pd
import  numpy as np
from datetime import datetime
from tqdm import tqdm # libreria para saber el tiempo de ejecución
from sqlalchemy import create_engine
import os
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


#2.1 DIRECIONES DE LOS ARCHIVOS
mt="Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv" 
mp="P.csv"

#2.2 LECTURA Y CARGA DE LOS ARCHIVOS
k=pd.read_csv(mt,usecols=[0])    #Se crea una variable que contenga la longitud del archivo original
n=len(k)                        #longitud de la columna de prueba
#n_2=665055 # los datos para restar de precipitación
#n=n_1-n_2
k.head()
del k

data_base_name = "DATA.db"    # se asigna un nombre al db
engine = create_engine('sqlite:///'+data_base_name)     # se crea el motor 
sqlite_connection = engine.connect()                    # se enciende la conexión
step=n*0.01             # el número es el porcentaje que se va a tomar "dx"
cont=0                  #contador
#Se crea el while que recorra el DataFrame y lo vaya ingresando cada dx
while tqdm(cont <= (n-1)):  
    #La siguiente fila de codigo lo que carga es el dx, se toma una porción y solo se carga
    #el porcentaje que se desea cargar que inicialmente se asigno en cada paso. 
    v=pd.read_csv(mt,nrows=int(step),skiprows=range(1,int(cont)))
    print("ingresando paso",cont)
    v.to_sql(name='temperatura',con=sqlite_connection,index=False,if_exists='append') 
    cont=cont+step
    del v
    #print(cont,"_",step)
    
sqlite_connection.close()   