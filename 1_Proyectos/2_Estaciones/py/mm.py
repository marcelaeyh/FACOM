#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 16:11:03 2022

@author: marcelae
"""


import pandas as pd
import  numpy as np
from datetime import datetime
from tqdm import tqdm              # libreria para saber el tiempo de ejecución
from sqlalchemy import create_engine
import os
import math
import matplotlib.pyplot as plt #Para graficar
import re
from unicodedata import normalize

#Lucy
eng = 'sqlite:////home/marcelae/Desktop/FACOM/2_db/precipitacion_2.db'

#Marcela
#eng = 'sqlite:////Volumes/DiscoMarcela/facom/presion.db'

query='''
SELECT * FROM precipitacion
WHERE CodigoEstacion == 52017020
'''

df = pd.read_sql(query,eng)

df["FechaObservacion"]=pd.to_datetime(df['FechaObservacion'],format='%m/%d/%Y %I:%M:%S %p')
df = df.sort_values("FechaObservacion")
df = df.reset_index(drop='index')

plt.figure(figsize=(10,5))
plt.plot(df.FechaObservacion,df.ValorObservado)
plt.grid()