#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 10:25:18 2022

@author: mac
"""

import numpy as np
import pandas as pd
import re
from tqdm import tqdm

bd = "/home/marcelae/Documents/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv"
#d = "/Users/mac/Desktop/facom/Departamentos.csv"

# Lee las columnas 4,5,6 y 7

#4. NombreEstacion
bd_ne = pd.read_csv(bd, usecols = [4])
#5. Departamentos
bd_dep = pd.read_csv(bd, usecols = [5])
#6. Municipios
bd_mun = pd.read_csv(bd, usecols = [6])
#7. ZonaHidrografica
bd_zh = pd.read_csv(bd, usecols = [7])

# FUNCIONES 

# CORREGIR TILDES, COMAS Y Ñ
def normalizar(df):
    
    # Diccionario con las correcciones
    dic = {'á':'a', 'é':'e','í':'i','ó':'o','ú':'u',",":"",'ñ':'n'}
    
    for i in tqdm(range(len(df))):
        # guarda el string viejo
        vs = df[i]
        
        # Busca en el diccionario el caracter especial
        for key in dic:
            x = re.search(key,df[i])
            
            # Si lo encuentra, lo reemplaza 
            if x != None:
                df[i] = df[i].replace(key,dic[key])
                
                # Reemplaza el string viejo por el nuevo en todo el df
                df = df.replace(vs,df[i])
    return df        
    
# CORRECCIÓN DEPARTAMENTOS
        
def corregir_departamentos(df):
    # Pone todo en minuscula
    df = df["Departamento"].str.lower()
    # Cambia tildes, comas y ñ
    df = normalizar(df)
    
    # Casos especiales departamentos
    def casos_especiales_dep(df):
        # Corregir bogotá
        for i in tqdm(range(len(df))):
            x = re.search('bog',df[i])
            if x != None:
                df[i] = 'bogota'
                
        # Corregir san andres
        for i in tqdm(range(len(df))):
            x = re.search('san and',df[i])
            if x != None:
                df[i] = 'san andres'
                
        return df   
    
    casos_especiales_dep(df)
    df = pd.DataFrame(df)
    return df

# CORRECCIÓN MUNICIPIOS
        
def corregir_municipios(df):
    # Pone todo en minuscula
    df = df["Municipio"].str.lower()
    # Cambia tildes, comas y ñ
    df = normalizar(df)
    
    # Casos especiales municipios
    def casos_especiales_mun(df):
        # Corregir bogotá
        for i in tqdm(range(len(df))):
            x = re.search('bog',df[i])
            if x != None:
                df[i] = 'bogota'
                
        return df       
    
    casos_especiales_mun(df)
    
    df = pd.DataFrame(df)
    return df

# CORRECCIÓN ZONA HIDROGRÁFICA
        
def corregir_zona_hidrografica(df):
    # Pone todo en minuscula
    df = df["ZonaHidrografica"].str.lower()
    # Cambia tildes, comas y ñ
    df = normalizar(df)
    
    df = pd.DataFrame(df)
    return df


# IMPLEMENTACIÓN DE LAS FUNCIONES 
        
bd_dep_c = corregir_departamentos(bd_dep)
bd_mun_c = corregir_municipios(bd_mun)
bd_zn_c = corregir_zona_hidrografica(bd_zh)