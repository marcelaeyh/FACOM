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
#----------------------------------------------------------------#
#2. CREACION DE VARIABLES DE NORMALIZACION, MOTOR DE POSGREST, DIRECCIONES, CONJUNTO DE DATOS

eng = "postgresql://lucy:usuario@localhost:5432/FACOM_IDEAM" #Motor
engine = create_engine(eng) #Maquina

#variables normalizadoras
vnC=["ValorObservado","FechaObservacion","CodigoEstacion","Calidad",
    "Departamento","Municipio","Zona Hidrografica","Tecnologia","Categoria",
    "Estado"]

vnBD=["nombre_categoria","nombre_tecnologia","nombre_estado",
      "nombre_departamento","nombre_zonahidrografica","nombre_municipio"]

#direcciones
d1=r"/home/marcelae/Desktop/FACOM/otros_documentos/Cat_logo_Nacional_de_Estaciones_del_IDEAM.csv"

#conjunto de datos
datos = pd.read_csv(d1)

#----------------------------------------------------------------#
# 3. FUNCIONES
def lower(df):
    df_s=df.str.lower().str.replace('á','a').str.replace('é','e').str.replace('í','i').str.replace('ó','o').str.replace('ú','u').str.replace('ñ','n')
    
    return(df_s)

#----------------------------------------------------------------#
# 4. FILTROS
#
#----------------------------------------------------------------#
# 5. CORRECIONES
#5.1 MAYUSCULAS, MINUSCULAS Y TILDES

datos[ac] = lower(cat_unicos[ac]) #remover mayúsculas, vocales y ñ
tec_unicos[at] = lower(tec_unicos[at]) #remover mayúsculas, vocales y ñ
est_unicos[ae] = lower(est_unicos[ae]) #remover mayúsculas, vocales y ñ
dep_unicos[ad] = lower(dep_unicos[ad]) #remover mayúsculas, vocales y ñ
zoh_unicos[azh] = lower(zoh_unicos[azh]) #remover mayúsculas, vocales y ñ


#5.2 COLUMNA NOMBRE ESTACION
import time
s = time.time()
nombre_estacion=datos.Nombre.str.split('-',expand=True).drop([1,2], axis=1)
nombre_estacion=pd.DataFrame(nombre_estacion[0].str.split('[',expand=True).drop([1], axis=1))
f = time.time()
print(f-s,nombre_estacion)
print(nombre_estacion[0].str.strip())

def nombres_catalogo(df):
    for i in range(len(df)):
        a = re.search("AUT",df[i])
        b = re.search("\[",df[i])
        if a:
 
            n = re.search("-",df[i])
            if n:
                n = n.start()-1
                if df[i][n-1] != " ":
                   df[i] = df[i][:n]
                else:
                    df[i] = df[i][:n-1]
        elif b:
            n = b.start()-1
            if df[i][n-1] != " ":
               df[i] = df[i][:n]
            else:
                df[i] = df[i][:n-1]
                  
    return df
s=time.time()
nombres_catalogo(datos.Nombre)
f = time.time()

print(f-s)

#5.3 UBICACION

ubicacion=pd.DataFrame(datos['Ubicación'].str.replace('(','').str.replace(')','').str.split(',',expand=True))
ubicacion.columns=["latitud","longitud"]
datos.Altitud=pd.DataFrame(datos.Altitud.str.replace(',','.'))
#5.4 ALTITUD
#----------------------------------------------------------------#
# 6.PROCESOS POR TABLA

#6.1 TABLA CATEGORIA
def categoria(catalogo):
    ca = pd.DataFrame(catalogo.Categoria.unique(),columns = ["nombre_categoria"])
    ca = ca.sort_values("nombre_categoria")
    ca.to_sql("categoria", engine, if_exists= "append",index=False)
    
#6.2 TABLA DEPARTAMENTO
def departamento(catalogo):
    dep = pd.DataFrame(catalogo.Departamento.unique(),columns = ["nombre_departamento"])
    dep = dep.sort_values("nombre_departamento")
    dep.to_sql("departamento", engine, if_exists= "append",index=False)
    
#6.3 TABLA ESTADO
def estado(catalogo):
    es = pd.DataFrame(catalogo.Estado.unique(),columns = ["nombre_estado"])
    es = es.sort_values("nombre_estado")
    es.to_sql("estado", engine, if_exists= "append",index=False)
    
#6.4 TABLA FLAGS

#6.5 TABLA MOMENTO OBSERVACION
def momento_observacion():
    mo=pd.DataFrame(pd.date_range(start="2000-01-01 00:00:00", end="2031-01-01 00:00:00", freq='min'),columns=["fecha_observacion"])
    mo.to_sql('momento_observacion', con=engine, index=False, if_exists='append', chunksize=10000)

#6.6 TABLA TECNOLOGIA
def tecnologia(catalogo):
    tec = pd.DataFrame(catalogo.Tecnologia.unique(),columns = ["nombre_tecnologia"])
    tec = tec.sort_values("nombre_tecnologia")
    tec.to_sql("tecnologia", engine, if_exists= "append",index=False)
    
#6.7 TABLA VARIABLE

#6.8 TABLA ZONA HIDROGRAFICA
def zonahidrografica(catalogo):
    zh = pd.DataFrame(catalogo["Zona Hidrografica"].unique(),columns = ["nombre_zonahidrografica"])
    zh = zh.sort_values("nombre_zonahidrografica")
    zh.to_sql("zonahidrografica", engine, if_exists= "append",index=False)
    
#6.9 TABLA MUNICIPIO
def llaveforanea(df,colum_cod_KF,tabla_KF,colum_name_KF,colum_name_dfKF,conn,
                 column_name_dfPK,colum_name_PF):
    #paso1: encontrar el valor con el que se relaciona
    #en la tabla de la llave foranea
    V=[]
    for i in tqdm(range(len(df))):
        my_query='''
        SELECT {} FROM {} WHERE {} = '{}'
        '''.format(colum_cod_KF,tabla_KF,colum_name_KF,df[colum_name_dfKF][i])
        
        #d_f=SQL_PD(my_query,conn)
        d_f=pd.read_sql(my_query,con=conn)
        
        v=[df[column_name_dfPK][i] ,int(d_f[colum_cod_KF][0])]
        V.append(v)
    V=pd.DataFrame(V)
    V.columns=[colum_name_PF,colum_cod_KF]
    return(V)

def municipio(catalogo,eng):
    
    mun_cat = catalogo[["Departamento","Municipio"]]
    mun_cat = mun_cat.drop_duplicates(subset = "Municipio")
    mun_cat = mun_cat.sort_values("Municipio")
    
    q = '''
    SELECT * FROM departamento;
    '''
    dep = SQL_PD(q,eng)
    dep.set_index("cod_departamento",inplace = True)
    
    cod = []
    
    for i in dep.nombre_departamento:
        for j in mun_cat.Departamento:
            if i == j:
                cod.append(dep.index[dep["nombre_departamento"] == i][0])
    
    mun = pd.DataFrame(columns = ["cod_departamento","nombre_municipio"])
    mun.nombre_municipio = mun_cat.Municipio
    mun.cod_departamento = cod
    
    mun.to_sql("municipio", engine, if_exists= "append",index=False)
    
#6.10 TABLA ESTACION
#6.11 TABLA OBSERVACION
#6.12 TABLA FLAGS X ESTACION
#6.13 TABLA FLAGS X OBSERVACION
 
 






datos = pd.read_csv()

nombre_estacion=datos.Nombre.str.split('-',expand=True).drop([1,2], axis=1)
nombre_estacion=pd.DataFrame(nombre_estacion[0].str.split('[',expand=True).drop([1], axis=1))
