#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 20:41:23 2022

@author: marcelae
"""

import pandas as pd

cat = pd.read_csv('/home/marcelae/Desktop/FACOM/1_Proyectos/2_Estaciones/CSV/existencia_estaciones_catalogo.csv',sep=';')
cat
eng = 'sqlite:////home/marcelae/Desktop/FACOM/2_db/presion.db'

q ='''
SELECT DISTINCT CodigoEstacion FROM presion
'''
df = pd.read_sql(q,con=eng)
pa = []
g=False
for i in cat.Codigo:
    g=False
    for j in df.CodigoEstacion:
        if j == i:
            g=True
    
    if g==True:
        pa.append(1.0)
    else:
        pa.append(0.0)
        
cat = cat.assign(pa =pa)

contador = 0
for i in range(len(cat)):
    if cat.pa[i]==1.0 or cat.p[i]==1.0 or cat.pa[i] ==1.0:
        contador +=1
print(contador)
ne = []
for i in df.CodigoEstacion:
    g=False
    for j in cat.Codigo:
        if j == i:
            g = True
            
    if g==False:
        ne.append(i)
        
ne = pd.DataFrame(ne)

ne.to_csv(r'/home/marcelae/Desktop/FACOM/1_Proyectos/2_Estaciones/CSV/noexisten_presion.csv', index=None, sep=';')
cat.to_csv(r'/home/marcelae/Desktop/FACOM/1_Proyectos/2_Estaciones/CSV/existencia_estaciones_catalogo.csv', index=None, sep=';')     
        

cat.t[0]

