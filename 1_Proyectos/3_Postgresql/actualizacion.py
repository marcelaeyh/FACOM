#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################  1. LIBRERIAS ################################ 
import pandas as pd
import  numpy as np
from datetime import datetime
from tqdm import tqdm              # libreria para saber el tiempo de ejecucion
from sqlalchemy import create_engine
import math
import time 
import streamlit as st
import folium
from streamlit_folium import folium_static
from sodapy import Socrata
from datetime import date, timedelta, datetime
################################  2. FUNCIONES ################################ 
################################  3. INFORMACIÓN DE ENTRADA ################################ 
#2.1 Información para la conexión con Socrata.
cliente= Socrata("www.datos.gov.co", "iiNW2MaM6IEhc9ryL8yT2Ouz8",
                  username="luisaburitica.ruiz@gmail.com",password="Paquito_Cabrito15")
#2.2 Base de datos de Postgresql
#eng="postgresql://facom:usuario@localhost:5432/alejandria"  #Motor Lucy-marcela
eng="postgresql://luisa:000000@localhost:5432/alejandria" #Luisa
engine = create_engine(eng) #Maquina
conn=engine.connect()

#2.3 Variables normalizadoras
vnC=['Codigo', 'Nombre', 'Categoria', 'Tecnologia', 'Estado', 'Departamento',
       'Municipio', 'Ubicación', 'Altitud', 'Fecha_instalacion',
       'Fecha_suspension', 'Area Operativa', 'Corriente', 'Area Hidrografica',
       'Zona Hidrografica', 'Subzona hidrografica', 'Entidad','Latitud','Longitud',
       'calidad','fecha_llaveforanea']

vnCSV=["CodigoEstacion","CodigoSensor","FechaObservacion","ValorObservado",
       "NombreEstacion","Departamento","Municipio","ZonaHidrografica","Latitud",
       "Longitud","DescripcionSensor","UnidadMedida"]

vnBD=["nombre_categoria","nombre_tecnologia","nombre_estado",
      "nombre_departamento","nombre_zonahidrografica","nombre_municipio",
      "cod_departamento","cod_municipio","cod_zonahidrografica","cod_categoria",
      "cod_tecnologia","cod_estado","descripcion_variable","unidad_medida","codigo_sensor",
      "cod_estacion","nombre_estacion","latitud","longitud","altitud","fecha_observacion",
      "cod_momento_observacion","valor_observado","cod_estacion","calidad_dato",
      "cod_variable"]

tablas=["departamento","municipio","zonahidrografica","categoria","tecnologia",
        "estado","momento_observacion","estacion","observacion","variable","flags",
        "flags_X_observacion","flags_x_estacion"]

################################  4. PROCESOS ################################

def fechaMaxVariable(variable):

    query='''
    select max(fecha_observacion) from observacion
    WHERE  cod_variable ={}
    '''.format(variable)
    datos=pd.read_sql(query,con=eng)
    return (datos)

#codvar= código de la variable de búsqueda
def ActualizacionIngreso(codvar,codDatosAbiertos,limSUP,limINF):
    #PASO 1 BÚSQUEDA DE ÚLTIMA FECHA
    fmax=fechaMaxVariable(codvar) #Búsqueda de fecha máxima para la variable
    f=fmax["max"][0] #Fecha máxima
    f= datetime.strftime(f,'%Y-%m-%dT%H:%M:%S') # Cambio de formato de fecha
    fbusqueda="fechaobservacion > " +"'" +str(f)+"'"
    
    #PASO 2 DESCARGA DE DATOS DE LA VARIABLE 
    df1 = pd.DataFrame( cliente.get(str(codDatosAbiertos), where=fbusqueda,limit=1000000))
    df1['codigoestacion'] = df1['codigoestacion'].astype(float)
    df1['valorobservado'] = df1['valorobservado'].astype(float)
    
    #PASO 3 FORMATO PARAEL ARCHIVO QUE INGRESA A LOS FILTROS
    df=pd.concat([df1.codigoestacion,df1.fechaobservacion,df1.valorobservado],axis=1)
    df.columns=["CodigoEstacion","FechaObservacion","ValorObservado"]
    del df1
    df[vnCSV[2]]=pd.to_datetime(df[vnCSV[2]],format='%Y-%m-%dT%H:%M:%S.%f')
    df[vnCSV[2]] = df[vnCSV[2]].dt.floor('Min')
    df=df.sort_values(by=vnCSV[2]).reset_index(drop=True,inplace=False)
    df[vnC[19]]= np.zeros(len(df))
    df[vnC[20]]=np.zeros(len(df))
    n_df=len(df)
    
    #PASO 4 FILTROS
    #categoria del dato
    for index, row in tqdm(df.iterrows()):
        if row[vnCSV[3]] < int(limSUP) or row[vnCSV[3]] > int(limINF):
            df[vnC[19]][index] = 1 
            
    #PASO 5 INGRESO DE INFORMACIÓN A LA BASE DE DATOS
    V=[] # Vector de almacenamiento 
    p=0  # Paso inicial para el for.
    for i in tqdm(range(p,n_df)):
        ab=df["CodigoEstacion"][i]
        if (ab==88112901 or ab==35237040 or ab==21202270 
            or ab==35217080 or ab==35227020 or ab==23157050 or ab==52017020):
            continue 
        if ab ==14015020:
            df[vnCSV[0]][i] = 14015080
        if ab==48015010:
            df[vnCSV[0]][i] = 48015050        
        v =[df[vnCSV[3]][i],df[vnCSV[2]][i],df[vnCSV[0]][i],df[vnC[19]][i],codvar] #Temperatura
        V.append(v)
    V=pd.DataFrame(V)
    V.columns=[vnBD[22], "fecha_observacion",vnBD[23],"categoria_dato",vnBD[25]]
    V.to_sql(tablas[8], con=engine, index=False, if_exists='append',chunksize=100000)
    print("Ingreso la información a la base de datos")
 
#Temperatura "sbwg-7ju4" 
#Precipitación 's54a-sgyg'
#presión '62tk-nxj5'
#dirección del viento "kiw7-v9ta"
#Velocida del viento 'sgfv-3yp8'

ActualizacionIngreso(1,"sbwg-7ju4",1.3,32.90) #Temperatura
ActualizacionIngreso(2,"s54a-sgyg",0.0,0.8) #precipitación
ActualizacionIngreso(3,"62tk-nxj5",1.3,32.90) #presión
ActualizacionIngreso(4,"kiw7-v9ta",0,360) #Dirección del viento
ActualizacionIngreso(5,'sgfv-3yp8',0,50) #velocidad del viento

