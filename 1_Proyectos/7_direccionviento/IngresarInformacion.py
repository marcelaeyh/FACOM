#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 10:23:57 2022

@author: Luisa Fernanda Buriticá Ruíz
Descripción: Código para ingreso de datos de velocidad y dirección del 
viento, 
"""
#----------------------------------------------------------------#
#1. LIBRERIAS
import pandas as pd
import numpy as np
from tqdm import tqdm # libreria para saber el tiempo de ejecuci´on
from sqlalchemy import create_engine
import time
import math

#5.9.3 DIRECCIÓN VIENTO
#2.1 Base de datos
#2.1.1 postgresql
eng = "postgresql://facom:usuario@localhost:5432/alejandria" #Motor
engine = create_engine(eng) #Maquina
conn=engine.connect()

#2.3 Variables normalizadoras
vnC=['Codigo','Nombre','Categoria','Tecnologia','Estado','Departamento','Municipio', 
      'Ubicación','Altitud','Fecha_instalacion','Fecha_suspension','Area Operativa','Corriente',
      'Area Hidrografica','Zona Hidrografica','Subzona hidrografica','Entidad','Latitud','Longitud',
      'calidad','fecha_llaveforanea']

vnCSV=["CodigoEstacion","CodigoSensor","FechaObservacion","ValorObservado", "NombreEstacion",
        "Departamento","Municipio","ZonaHidrografica","Latitud","Longitud","DescripcionSensor",
        "UnidadMedida"]

vnBD=["nombre_categoria","nombre_tecnologia","nombre_estado", "nombre_departamento",
       "nombre_zonahidrografica","nombre_municipio","cod_departamento","cod_municipio",
       "cod_zonahidrografica","cod_categoria","cod_tecnologia","cod_estado","descripcion_variable",
       "unidad_medida","codigo_sensor","cod_estacion","nombre_estacion","latitud","longitud",
       "altitud","fecha_observacion","valor_observado","cod_estacion",
       "categoria_dato","cod_variable"]

tablas=["departamento","municipio","zonahidrografica","categoria","tecnologia","estado",
        "estacion","observacion","variable"]


direV=r"/home/marcelae/Desktop/FACOM/3_csv/Direcci_n_Viento.csv"
veloV=r"/home/marcelae/Desktop/FACOM/3_csv/Velocidad_Viento.csv"

#logitud del archivo de entrada
ldv =pd.read_csv(direV,usecols=[0])
n_dv=len(ldv)
del ldv

step=math.ceil(n_dv*0.05)  #el numero es el porcentaje que se va a tomar "dx"
cont=0 # el contador inicia desde 0, pero si es necesario se pue asignar uno diferente
dx=0
print("Longitud del archivo de entrada= ",n_dv)
print("Los pasos de tiempo son de= ",step)
print("Inicia desde= ",cont)
while tqdm(cont <= (n_dv-1)):
    start= time.time()
    #Las siguientes lineas de codigo toman una porcion de los datos y solo se ingresa
    #el porcentaje que se desea cargar, esto se asigno anteriormente en el paso. 
    df=pd.read_csv(direV,nrows=int(step),skiprows=range(1,int(cont)),usecols=[0,2,3])
    print("######################")
    print("#------#-------#")
    print("contador",cont,"paso=",dx)
    print("#------#-------#")
    df[vnCSV[2]]=pd.to_datetime(df[vnCSV[2]],format='%m/%d/%Y %I:%M:%S %p')
    df[vnCSV[2]] = df[vnCSV[2]].dt.floor('Min')
    df=df.sort_values(by=vnCSV[2]).reset_index(drop=True,inplace=False)
    df[vnC[19]]= np.zeros(len(df))
    df[vnC[20]]=np.zeros(len(df))
    n_df=len(df)
    print("Ingresa la categoria-",dx)
    print("#------#-------#")
    # Categoria del dato
    for index, row in tqdm(df.iterrows()):
        
        if row[vnCSV[3]] < 0 or row[vnCSV[3]] > 360:
            df[vnC[19]][index] = 1 
       

    print("Ingresa a ingresar informacion-",dx)
    print("#------#-------#")       
    #Ingreso de la informacion
    V=[]
    p=0
    for i in tqdm(range(p,n_df)):
        ab=df["CodigoEstacion"][i]
        if (ab==88112901 or ab==35237040 or ab==21202270 
            or ab==35217080 or ab==35227020 or ab==23157050 or ab==52017020):
            continue 
        
        if ab ==14015020:
            df[vnCSV[0]][i] = 14015080
        if ab==48015010:
            df[vnCSV[0]][i] = 48015050
            
        v =[df[vnCSV[3]][i],df[vnCSV[2]][i],df[vnCSV[0]][i],df[vnC[19]][i],4]
        V.append(v)

    V=pd.DataFrame(V)
    V.columns=[vnBD[21], vnBD[20],vnBD[22],vnBD[23],vnBD[24]]
    V.to_sql(tablas[7], con=engine, index=False, if_exists='append',chunksize=100000)
    cont=cont+step
    final= time.time()
    print("Termina-",dx)
    print("#------#-------#")

    dx=dx+1
    print("Tiempo de ejecucion",final-start)
    print("#------#-------#")
    print("######################")

#logitud del archivo de entrada
lvev =pd.read_csv(veloV,usecols=[0])
n_vev=len(lvev)
del lvev

step=math.ceil(n_vev*0.05)  #el numero es el porcentaje que se va a tomar "dx"
cont=0 # el contador inicia desde 0, pero si es necesario se pue asignar uno diferente
dx=0
print("Longitud del archivo de entrada= ",n_vev)
print("Los pasos de tiempo son de= ",step)
print("Inicia desde= ",cont)

while tqdm(cont <= (n_vev-1)):
    start= time.time()
    #Las siguientes lineas de codigo toman una porcion de los datos y solo se ingresa
    #el porcentaje que se desea cargar, esto se asigno anteriormente en el paso. 
    df=pd.read_csv(veloV,nrows=int(step),skiprows=range(1,int(cont)),usecols=[0,2,3])
    print("######################")
    print("#------#-------#")
    print("contador",cont,"paso=",dx)
    print("#------#-------#")
    df[vnCSV[2]]=pd.to_datetime(df[vnCSV[2]],format='%m/%d/%Y %I:%M:%S %p')
    df[vnCSV[2]] = df[vnCSV[2]].dt.floor('Min')
    df=df.sort_values(by=vnCSV[2]).reset_index(drop=True,inplace=False)
    df[vnC[19]]= np.zeros(len(df))
    df[vnC[20]]=np.zeros(len(df))
    n_df=len(df)
    print("Ingresa la categoria-",dx)
    print("#------#-------#")
    # Categoria del dato
    for index, row in tqdm(df.iterrows()):
        
        if row[vnCSV[3]] < 0 or row[vnCSV[3]] > 50:
            df[vnC[19]][index] = 1 
       

    print("Ingresa a ingresar informacion-",dx)
    print("#------#-------#")       
    #Ingreso de la informacion
    V=[]
    p=0
    for i in tqdm(range(p,n_df)):
        ab=df["CodigoEstacion"][i]
        if (ab==88112901 or ab==35237040 or ab==21202270 
            or ab==35217080 or ab==35227020 or ab==23157050 or ab==52017020):
            continue 
        
        if ab ==14015020:
            df[vnCSV[0]][i] = 14015080
        if ab==48015010:
            df[vnCSV[0]][i] = 48015050
            
        v =[df[vnCSV[3]][i],df[vnCSV[2]][i],df[vnCSV[0]][i],df[vnC[19]][i],5]
        V.append(v)

    V=pd.DataFrame(V)
    V.columns=[vnBD[21], vnBD[20],vnBD[22],vnBD[23],vnBD[24]]
    V.to_sql(tablas[7], con=engine, index=False, if_exists='append',chunksize=100000)
    cont=cont+step
    final= time.time()
    print("Termina-",dx)
    print("#------#-------#")
    dx=dx+1
    print("Tiempo de ejecucion",final-start)
    print("#------#-------#")
    print("######################")