#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 12:05:21 2022

@author: marcela
"""

import pandas as pd
import  numpy as np
from datetime import datetime
from tqdm import tqdm              # libreria para saber el tiempo de ejecución
from sqlalchemy import create_engine
import os
import math
import re
import matplotlib.pyplot as plt #Para graficar

#Funciones extra
# Load de data
def SQL_PD(table_or_sql,eng):
       engine = create_engine(eng)
       conn = engine.connect()
       generator_object = pd.read_sql(table_or_sql,con=conn)
       return generator_object 

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

# Se crea la conexión a la base de datos
engine = create_engine("postgresql://lucy2:usuario@localhost:5432/prueba")

eng = "postgresql://lucy2:usuario@localhost:5432/prueba"

# Se lee el catalogo con la información para añadir
catalogo = pd.read_csv(r"/home/marcela/Desktop/FACOM/otros_documentos/Cat_logo_Nacional_de_Estaciones_del_IDEAM.csv")
print("Se leyó correctamente el catalogo de estaciones")

# Se saca la latitud y longitud de cada una de las estaciones de los datos del IDEAM

print("inició la carga del archivo precipitacion")
p = pd.read_csv(r"/home/marcela/Documents/organizar/Precipitaci_n.csv",usecols=(0,8,9))
print("terminó la carga del archivo precipitacion")


print("inició la carga del archivo temperatura")
t = pd.read_csv(r"/home/marcela/Documents/organizar/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv",
                usecols=(0,8,9))
print("terminó la carga del archivo temperatura")

p = p.drop_duplicates(subset = "CodigoEstacion")
p = p.sort_values("CodigoEstacion")
p = p.reset_index(drop="index")

t = t.drop_duplicates(subset = "CodigoEstacion")
t = t.sort_values("CodigoEstacion")
t = t.reset_index(drop="index")

a = pd.read_csv(r"/home/marcela/Desktop/FACOM/Estaciones/existencia_estaciones_catalogo.csv",sep=";")

est = []
lat = []
lon = []

for i in range(len(a)):
    if (a.t[i] == 1.0) or (a.p[i] == 1.0):
        est.append(a.Codigo[i])
        try:
            indexp = p.index[p.CodigoEstacion == a.Codigo[i]][0]
            lat.append(p.Latitud[indexp])
            lon.append(p.Longitud[indexp])
        except:
            indext = t.index[t.CodigoEstacion == a.Codigo[i]][0]
            lat.append(t.Latitud[indext])
            lon.append(t.Longitud[indext])
        
coordenadas = pd.DataFrame(columns = ["Codigo","Latitud","Longitud"])
coordenadas.Codigo = est
coordenadas.Latitud = lat
coordenadas.Longitud = lon


# Funciones para añadir informacion por tabla

def departamento(catalogo):
    dep = pd.DataFrame(catalogo.Departamento.unique(),columns = ["nombre_departamento"])
    dep = dep.sort_values("nombre_departamento")
    dep.to_sql("departamento", engine, if_exists= "append",index=False)

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

def zonahidrografica(catalogo):
    zh = pd.DataFrame(catalogo["Zona Hidrografica"].unique(),columns = ["nombre_zonahidrografica"])
    zh = zh.sort_values("nombre_zonahidrografica")
    zh.to_sql("zonahidrografica", engine, if_exists= "append",index=False)

def categoria(catalogo):
    ca = pd.DataFrame(catalogo.Categoria.unique(),columns = ["nombre_categoria"])
    ca = ca.sort_values("nombre_categoria")
    ca.to_sql("categoria", engine, if_exists= "append",index=False)
    
def tecnologia(catalogo):
    tec = pd.DataFrame(catalogo.Tecnologia.unique(),columns = ["nombre_tecnologia"])
    tec = tec.sort_values("nombre_tecnologia")
    tec.to_sql("tecnologia", engine, if_exists= "append",index=False)
        
def estado(catalogo):
    es = pd.DataFrame(catalogo.Estado.unique(),columns = ["nombre_estado"])
    es = es.sort_values("nombre_estado")
    es.to_sql("estado", engine, if_exists= "append",index=False)

def estaciones(catalogo,coordenadas,eng):
    
    print("Inició la corrección de columnas para estaciones")
    
    #Separa latitud y longitud del catalogo
    m=catalogo['Ubicación'].str.replace('(','').str.replace(')','').str.split(',',expand=True)
    la =m[0]
    lo =m[1]

    # Reemplaza las coordenadas de las estaciones que están en los csv del IDEAM
    for i in tqdm(range(len(catalogo))):
        for j in range(len(coordenadas)):
            if catalogo.Codigo[i] == coordenadas.Codigo[j]:
                la[i] = float(coordenadas.Latitud[j])
                lo[i] = float(coordenadas.Longitud[j])
    
    print("Se corrigieron las coordenadas correctamente")
    
    # Corregir errores de altitud 
    altitud = catalogo.Altitud
    for i in range(len(catalogo)):
        altitud[i] = re.sub(",","",altitud[i])
        altitud[i] = float(altitud[i])
        
    print("Se corrigió la altitud correctamente")
    # Busqueda de codigos
    
    # Municipio:       
    mun = '''
    SELECT * FROM municipio;
    '''
    mun = SQL_PD(mun,eng)
    mun.set_index("cod_municipio",inplace = True)
    cod_mun = []
    
    for i in catalogo.Municipio:
        for j in mun.nombre_municipio:
            if i == j:
                cod_mun.append(mun.index[mun["nombre_municipio"] == j][0])
                break
   
    # Zona Hidrografica:       
    zh = '''
    SELECT * FROM zonahidrografica;
    '''
    zh = SQL_PD(zh,eng)
    zh.set_index("cod_zonahidrografica",inplace = True)
    cod_zh = []
    
    for i in catalogo["Zona Hidrografica"]:
        for j in zh.nombre_zonahidrografica:
            if i == j:
                cod_zh.append(zh.index[zh["nombre_zonahidrografica"] == j][0])
                break
        
    # Categoria
    cat = '''
    SELECT * FROM categoria
    '''
    cat = SQL_PD(cat,eng)
    cat.set_index("cod_categoria",inplace = True)

    cod_cat = []
    
    for i in catalogo.Categoria:
        for j in cat.nombre_categoria:
            if i == j:
                cod_cat.append(cat.index[cat["nombre_categoria"] == j][0])
                break
                
    # Tecnologia
    tec = '''
    SELECT * FROM tecnologia
    '''
    tec = SQL_PD(tec,eng)
    tec.set_index("cod_tecnologia",inplace = True)

    cod_tec = []
    
    for i in catalogo.Tecnologia:
        for j in tec.nombre_tecnologia:
            if i == j:
                cod_tec.append(tec.index[tec["nombre_tecnologia"] == j][0])
                break

    # Estado
    es = '''
    SELECT * FROM estado
    '''
    es = SQL_PD(es,eng)
    es.set_index("cod_estado",inplace = True)

    cod_es = []
    
    for i in catalogo.Estado:
        for j in es.nombre_estado:
            if i == j:
                cod_es.append(es.index[es["nombre_estado"] == j][0])
                break
                
    # df con toda la informacion anterior        
    estacion = pd.DataFrame(columns = ["codigo_estacion","nombre_estacion","latitud","longitud",
                                  "cod_municipio","cod_zonahidrografica","cod_categoria",
                                  "cod_tecnologia","cod_estado","altitud"])
    
    estacion.codigo_estacion = catalogo.Codigo
    estacion.nombre_estacion = nombres_catalogo(catalogo.Nombre)
    print("Se corrigieron los nombres de las estaciones correctamente")
    estacion.latitud = la
    estacion.longitud = lo
    estacion.cod_municipio = cod_mun
    estacion.cod_zonahidrografica = cod_zh
    estacion.cod_categoria = cod_cat
    estacion.cod_tecnologia = cod_tec
    estacion.cod_estado = cod_es
    estacion.altitud = altitud
    # Se añade el df a la tabla estacion
    estacion.to_sql("estacion", engine, if_exists= "append",index=False)
    
def momento_observacion():
    start = pd.to_datetime("01-01-2000 00:00:00", format="%d-%m-%Y %H:%M:%S")
    end = pd.to_datetime("31-12-2030 23:59:59", format="%d-%m-%Y %H:%M:%S")
    mo = pd.date_range(start, end,freq="1min").to_frame()
    mo.columns=["fecha_observacion"]
    
    # Se añade el df a la tabla momento_observacion
    mo.to_sql('momento_observacion', con=engine, index=False, if_exists='append', 
                  chunksize=5000)
def variable():
    temp = pd.read_csv(r"/home/marcela/Documents/organizar/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv",
                       nrows=1)
    precip = pd.read_csv(r"/home/marcela/Documents/organizar/Precipitaci_n.csv",
                         nrows=1)

    variable = pd.DataFrame(columns = ["descripcion_variable","unidad_medida","codigo_sensor"])
    variable.descripcion_variable = [temp.DescripcionSensor[0],precip.DescripcionSensor[0],"Presión Atmosferica (1h)"]
    variable.unidad_medida = [temp.UnidadMedida[0],precip.UnidadMedida[0],"HPa"]
    variable.codigo_sensor = [temp.CodigoSensor[0],precip.CodigoSensor[0],255]
    
    # Se añade el df a la tabla variable
    variable.to_sql("variable", engine, if_exists= "append",index=False)
    
def añadirdb(catalogo):
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
    estaciones(catalogo,coordenadas,eng)
    print("Se añadieron los datos a la tabla estacion")
    momento_observacion()
    print("Se añadieron los datos a la tabla momento_observacion")
    variable()
    print("Se añadieron los datos a la tabla variable")

añadirdb(catalogo)





