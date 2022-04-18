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

bd = "/Volumes/DiscoMarcela/facom/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv"
d = "/Users/mac/Desktop/facom/Departamentos.csv"

# Lee los archivos
bd_dep = pd.read_csv(bd, usecols = [5])
dep = pd.read_csv(d,sep=";")
dep.columns = ["Departamento"]

# Pone todo en minuscula
bd_depl = bd_dep["Departamento"].str.lower()
depl = dep["Departamento"].str.lower()

# Función para corregir tildes, comas y ñ 
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
            
    print("Terminó corrección de tildes y caractéres especiales")
        
# Función para corregir casos especiales
def casos_especiales(df):
    # Corregir bogotá
    for i in range(len(df)):
        x = re.search('bog',df[i])
        if x != None:
            df[i] = 'bogota'
    # Corregir san andres
    for i in range(len(df)):
        x = re.search('san andres',df[i])
        if x != None:
            df[i] = 'san andres'
        
    print("Terminó corrección de casos especiales")

normalizar(bd_depl)
casos_especiales(bd_depl)

bd_depl.head()
