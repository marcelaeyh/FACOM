#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 10:59:33 2022

@author: marcelae
"""

#----------------------------------------------------------------#
#1. LIBRERIAS

import pandas as pd
import  numpy as np
from datetime import datetime
from tqdm import tqdm              # libreria para saber el tiempo de ejecucion
from sqlalchemy import create_engine
import os
import math
import re
import matplotlib.pyplot as plt #Para graficar
import time 
#----------------------------------------------------------------#
#2. CREACION DE VARIABLES DE NORMALIZACION, MOTOR DE POSGREST, DIRECCIONES, CONJUNTO DE DATOS

#2.1 Bases de datos

#2.1.1 postgresql
eng = "postgresql://facom:usuario@localhost:5432/alejandria" #Motorlucy marcela
#eng="postgresql://luisa:000000@localhost:5432/alejandria" #Motor Luisa
engine = create_engine(eng) #Maquina
conn=engine.connect()

#2.1.2 sqlite
T_sqlite= 'sqlite:////home/marcelae/Desktop/FACOM/2_db/temperatura_2.db' #lucy
P_sqlite= 'sqlite:////home/marcelae/Desktop/FACOM/2_db/precipitacion_2.db' #lucy
#T_sqlite= 'sqlite:////media/luisa/Datos/FACOM/gits/FACOM/2_db/temperatura_2.db' #lucy
#P_sqlite= 'sqlite:////media/luisa/Datos/FACOM/gits/FACOM/2_db/precipitacion_2.db' #luisa

#2.2 Creación de la conexión con la base de datos
Tengine_sql = create_engine(T_sqlite)  #Temperatura 
Pengine_sql = create_engine(P_sqlite)  #Precipitación
Tconn = Tengine_sql.connect()  #Temperatura
Pconn = Pengine_sql.connect()  #Precipitación

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

#2.4 Direcciones

#2.4.1 lucy
d1=r"/home/marcelae/Desktop/FACOM/5_Documentos/Cat_logo_Nacional_de_Estaciones_del_IDEAM.csv"
temp = r"/home/marcelae/Desktop/FACOM/3_csv/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv"
pre = r"/home/marcelae/Desktop/FACOM/3_csv/Precipitaci_n.csv"
pres= r"/home/marcelae/Desktop/FACOM/3_csv/Presi_n_Atmosf_rica.csv"
coor= r"/home/marcelae/Desktop/FACOM/1_Proyectos/2_Estaciones/CSV/coordenadas_estaciones.csv"

#2.4.2 Luisa
#d1=r"/media/luisa/Datos/FACOM/gits/FACOM/5_Documentos/Cat_logo_Nacional_de_Estaciones_del_IDEAM.csv"
#temp = r"/media/luisa/Datos/FACOM/gits/FACOM/3_csv/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv"
#pre=r"/media/luisa/Datos/FACOM/gits/FACOM/3_csv/Precipitaci_n.csv"
#pres= r"/media/luisa/Datos/FACOM/gits/FACOM/3_csv/Presi_n_Atmosf_rica.csv"
#coor= r"/media/luisa/Datos/FACOM/gits//FACOM/1_Proyectos/2_Estaciones/CSV/coordenadas_estaciones.csv"

#conjunto de datos
datos = pd.read_csv(d1)
#----------------------------------------------------------------#
# 3. FUNCIONES
def lower(df):
    df_s=df.str.lower().str.replace('á','a').str.replace('é','e').str.replace('í','i').str.replace('ó','o').str.replace('ú','u').str.replace('ñ','n')
    
    return(df_s)

def llave(eng,tabla_FK,cod_FK,data,data_FK,nombredb_FK):
    q = '''
    SELECT * FROM {};
    '''.format(tabla_FK)
    b = pd.read_sql(q,con=eng)
    #b = SQL_PD(q,eng)
    b.set_index(cod_FK,inplace = True)
    
    cod = []
    
    for i in data[data_FK]:
        for j in b[nombredb_FK]:
            if i == j:
                cod.append(b.index[b[nombredb_FK] == j][0])
                break 
    return cod
#----------------------------------------------------------------#
# 4. FILTROS
#
#----------------------------------------------------------------#
# 5. CORRECIONES
#5.1 MAYUSCULAS, MINUSCULAS Y TILDES

datos[vnC[1]] = lower(datos[vnC[1]] ) #remover mayúsculas, vocales y ñ
datos[vnC[2]] = lower(datos[vnC[2]] ) #remover mayúsculas, vocales y ñ
datos[vnC[3]] = lower(datos[vnC[3]] ) #remover mayúsculas, vocales y ñ
datos[vnC[4]] = lower(datos[vnC[4]] ) #remover mayúsculas, vocales y ñ
datos[vnC[5]] = lower(datos[vnC[5]] ) #remover mayúsculas, vocales y ñ
datos[vnC[6]] = lower(datos[vnC[6]] ) #remover mayúsculas, vocales y ñ
datos[vnC[14]] = lower(datos[vnC[14]]) #remover mayúsculas, vocales y ñ

#5.2 COLUMNA NOMBRE ESTACION
def nombres_cat(df):
    df=df.str.split('-',expand=True).drop([1,2], axis=1)
    df=pd.DataFrame(df[0].str.split('[',expand=True).drop([1], axis=1))
    return df

datos[vnC[1]] = nombres_cat(datos[vnC[1]])

#5.3 UBICACION
def ubicacion(datos):
    ubicacion = datos[vnC[7]].str.replace('(','').str.replace(')','').str.split(',',expand=True)
    c = pd.read_csv(coor,sep=";")
    # Reemplaza las coordenadas de las estaciones que están en los csv del IDEAM
    for i in tqdm(range(len(datos))):
        for j in range(len(c)):
            if datos[vnC[0]][i] == c.Codigo[j]:
                ubicacion[0][i] = c.Latitud[j]
                ubicacion[1][i] = c.Longitud[j]
    return ubicacion[0].astype(float),ubicacion[1].astype(float)

lat, lon = ubicacion(datos)
datos.insert(17,"Latitud",lat)
datos.insert(18,"Longitud",lon)
datos =  datos.drop(columns=["Ubicación"])

#5.4 ALTITUD                
def Altitud(datos):                
    datos[vnC[8]]=pd.DataFrame(datos[vnC[8]].str.replace(',','')).astype(float)

Altitud(datos)

#----------------------------------------------------------------#
# 6.PROCESOS POR TABLA

#6.1 TABLA CATEGORIA
def categoria(datos):
    ca = pd.DataFrame(datos[vnC[2]].unique(),columns = [vnBD[0]])
    ca = ca.sort_values(vnBD[0])
    ca.to_sql(tablas[3], engine, if_exists= "append",index=False)
    
#6.2 TABLA DEPARTAMENTO
def departamento(datos):
    dep = pd.DataFrame(datos[vnC[5]].unique(),columns = [vnBD[3]])
    dep = dep.sort_values(vnBD[3])
    dep.to_sql(tablas[0], engine, if_exists= "append",index=False)
    
#6.3 TABLA ESTADO

def estado(datos):
    es = pd.DataFrame(datos[vnC[4]].unique(),columns = [vnBD[2]])
    es = es.sort_values(vnBD[2])
    es.to_sql(tablas[5], engine, if_exists= "append",index=False)
    
#6.4 TABLA FLAGS

#6.5 TABLA MOMENTO OBSERVACION
def momento_observacion():
    mo=pd.DataFrame(pd.date_range(start="2000-01-01 00:00:00", end="2031-01-01 00:00:00", freq='min'),columns=["fecha_observacion"])
    mo.to_sql(tablas[6], con=engine, index=False, if_exists='append', chunksize=10000)

#6.6 TABLA TECNOLOGIA
def tecnologia(datos):
    tec = pd.DataFrame(datos[vnC[3]].unique(),columns = [vnBD[1]])
    tec = tec.sort_values(vnBD[1])
    tec.to_sql(tablas[4], engine, if_exists= "append",index=False)
    
#6.7 TABLA VARIABLE
def variable():
    temperatura = pd.read_csv(temp,nrows=1)
    precipitacion = pd.read_csv(pre,nrows=1)

    variable = pd.DataFrame(columns = [vnBD[12],vnBD[13],vnBD[14]])
    variable.descripcion_variable = [temperatura.DescripcionSensor[0],precipitacion.DescripcionSensor[0],"Presión Atmosferica (1h)"]
    variable.unidad_medida = [temperatura.UnidadMedida[0],precipitacion.UnidadMedida[0],"HPa"]
    variable.codigo_sensor = [temperatura.CodigoSensor[0],precipitacion.CodigoSensor[0],255]
    
    # Se añade el df a la tabla variable
    variable.to_sql(tablas[9], engine, if_exists= "append",index=False)
    
#6.8 TABLA ZONA HIDROGRAFICA
def zonahidrografica(datos):
    zh = pd.DataFrame(datos[vnC[14]].unique(),columns = [vnBD[4]])
    zh = zh.sort_values(vnBD[4])
    zh.to_sql(tablas[2], engine, if_exists= "append",index=False)
    
#6.9 TABLA MUNICIPIO
def municipio(datos,eng):
    
    mun_cat = datos[[vnC[5],vnC[6]]]
    mun_cat = mun_cat.drop_duplicates(subset = vnC[6])
    mun_cat = mun_cat.sort_values(vnC[6])
    
    cod_mun = llave(eng,tablas[0],vnBD[6],mun_cat,vnC[5],vnBD[3])
    
    mun = pd.DataFrame(columns = [vnBD[6],vnBD[5]])
    mun.nombre_municipio = mun_cat[vnC[6]]
    mun.cod_departamento = cod_mun
    
    mun.to_sql(tablas[1], engine, if_exists= "append",index=False)
    
#6.10 TABLA ESTACION
def estacion(datos,eng):
    # Busqueda de Codigos
    
    cod_mun = llave(eng,tablas[1],vnBD[7],datos,vnC[6],vnBD[5])
    cod_zh = llave(eng,tablas[2],vnBD[8],datos,vnC[14],vnBD[4])
    cod_tec = llave(eng,tablas[4],vnBD[10],datos,vnC[3],vnBD[1])
    cod_est = llave(eng,tablas[5],vnBD[11],datos,vnC[4],vnBD[2])
    cod_cat = llave(eng,tablas[3],vnBD[9],datos,vnC[2],vnBD[0])
    
    estacion = pd.DataFrame(columns = [vnBD[15],vnBD[16],vnBD[17],vnBD[18],vnBD[7],
                                       vnBD[8],vnBD[9],vnBD[10],vnBD[11],vnBD[19]])
    
    estacion.cod_estacion = datos[vnC[0]]
    estacion.nombre_estacion = datos[vnC[1]]
    estacion.latitud = datos[vnC[17]]
    estacion.longitud = datos[vnC[18]]
    estacion.cod_municipio = cod_mun
    estacion.cod_zonahidrografica = cod_zh
    estacion.cod_categoria = cod_cat
    estacion.cod_tecnologia = cod_tec
    estacion.cod_estado = cod_est
    estacion.altitud = datos[vnC[8]]
    # Se añade el df a la tabla estacion
    estacion.to_sql(tablas[7], engine, if_exists= "append",index=False)

#########################################################
# EJECUCION DE LAS FUNCIONES PARA AGREGAR TABLAS
def añadirdb(catalogo,eng):
    departamento(catalogo)
    print("Se añadieron los datos a la tabla departamento")
    municipio(catalogo,eng)
    print("Se añadieron los datos a la tabla municipio")
    zonahidrografica(catalogo)
    print("Se añadieron los datos a la tabla zonahidrografica")
    categoria(catalogo)
    print("Se añadieron los datos a la tabla categoria")
    tecnologia(catalogo)
    print("Se añadieron los datos a la tabla tecnologia")
    estado(catalogo)
    print("Se añadieron los datos a la tabla estado")
    estacion(catalogo,eng)
    print("Se añadieron los datos a la tabla estacion")
    #momento_observacion()
    #print("Se añadieron los datos a la tabla momento_observacion")
    variable()
    print("Se añadieron los datos a la tabla variable")


añadirdb(datos,eng)

#6.11 TABLA OBSERVACION


#tabla momento observacion
#mo='''
#SELECT *
#FROM momento_observacion
#''' 
#mo = pd.read_sql(mo,con=conn) # se obtiene la tabla momento observacion
#n_mo=len(mo)


#6.11.1 PRECIPITACION
#logitud del archivo de entrada
lp=pd.read_csv(pre,usecols=[0])
n_p=len(lp)
del lp

step=math.ceil(n_p*0.05)  #el número es el porcentaje que se va a tomar "dx"
cont=0 # el contador inicia desde 0, pero si es necesario se pue asignar uno diferente
dx=0
print("Longitud del archivo de entrada= ",n_p)
print("Los pasos de tiempo son de= ",step)
print("Inicia desde= ",cont)

while tqdm(cont <= (n_p-1)):
    start= time.time()
    #La siguiente fila de codigo lo que carga es el dx, se toma una porción y solo se carga
    #el porcentaje que se desea cargar que inicialmente se asigno en cada paso. 
    df=pd.read_csv(pre,nrows=int(step),skiprows=range(1,int(cont)),usecols=[0,2,3])
    print("#------#-------#")
    print("contador ",cont,"paso=",dx)
    print("#------#-------#")
    dx=dx+1
    
    df[vnCSV[2]]=pd.to_datetime(df[vnCSV[2]],format='%m/%d/%Y %I:%M:%S %p')
    df[vnCSV[2]] = df[vnCSV[2]].dt.floor('Min')
    df=df.sort_values(by=vnCSV[2]).reset_index(drop=True,inplace=False)
    df[vnC[19]]= np.zeros(len(df))
    df[vnC[20]]=np.zeros(len(df))
    n_df=len(df)
    
    #categoria del dato
    for index, row in tqdm(df.iterrows()):
        
        if row[vnCSV[3]] < 0.0 or row[vnCSV[3]] >0.8:
            df[vnC[19]][index] = 1.0
       
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
            
        v =[df[vnCSV[3]][i],df[vnCSV[2]][i],df[vnCSV[0]][i],df[vnC[19]][i],2]
        V.append(v)

    V=pd.DataFrame(V)
    vnBD[25]
    V.columns=[vnBD[22], "fecha_observacion",vnBD[23],"categoria_dato",vnBD[25]]
    V.to_sql(tablas[8], con=engine, index=False, if_exists='append',chunksize=100000)
    cont=cont+step
    final= time.time()
    print("Tiempo de ejecución",final-start)
    
#6.11.2 TEMPERATURA
#logitud del archivo de entrada
lt =pd.read_csv(temp,usecols=[0])
n_t=len(lt)
del lt

step=math.ceil(n_t*0.05)  #el número es el porcentaje que se va a tomar "dx"
cont=0 # el contador inicia desde 0, pero si es necesario se pue asignar uno diferente
dx=0
print("Longitud del archivo de entrada= ",n_t)
print("Los pasos de tiempo son de= ",step)
print("Inicia desde= ",cont)
while tqdm(cont <= (n_t-1)):
    start= time.time()
    #La siguiente fila de codigo lo que carga es el dx, se toma una porción y solo se carga
    #el porcentaje que se desea cargar que inicialmente se asigno en cada paso. 
    df=pd.read_csv(temp,nrows=int(step),skiprows=range(1,int(cont)),usecols=[0,2,3])
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
    print("Ingresa a calidad-",dx)
    print("#------#-------#")
    #Calidad del dato
    for index, row in tqdm(df.iterrows()):
        
        if row[vnCSV[3]] < 1.3 or row[vnCSV[3]] > 32.90:
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
            
        v =[df[vnCSV[3]][i],df[vnCSV[2]][i],df[vnCSV[0]][i],df[vnC[19]][i],1]
        V.append(v)

    V=pd.DataFrame(V)
    vnBD[25]
    V.columns=[vnBD[22], "fecha_observacion",vnBD[23],"categoria_dato",vnBD[25]]
    V.to_sql(tablas[8], con=engine, index=False, if_exists='append',chunksize=100000)
    cont=cont+step
    final= time.time()
    print("Termina-",dx)
    print("#------#-------#")

    dx=dx+1
    print("Tiempo de ejecución",final-start)
    print("#------#-------#")
    print("######################")


    

#6.12 TABLA FLAGS X ESTACION
#6.13 TABLA FLAGS X OBSERVACION












