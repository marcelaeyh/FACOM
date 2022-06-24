#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 22:22:15 2022

@author: luisa
"""
import numpy as np

import matplotlib.pyplot as plt
import pandas as pd


#direcciones
d1="/media/luisa/Datos/FACOM//SIATA/SIATAprecipitacion81/"
d2="p81201306.csv"
d4="/media/luisa/Datos/FACOM/gits/FACOM/1_Proyectos/3_Postgresql/QGIS/csv_excel"
vector=pd.read_csv(d1+d2)

d3="p812018"
for i in range(0,12):
    if i<9:
        cont=("0"+str(i+1))
        print(d3+cont)
        m=pd.read_csv(d1+d3+cont+".csv")
        vector=pd.concat([vector,m])
    else:
        cont=(str(i+1))
        print(d3+cont)
        m=pd.read_csv(d1+d3+cont+".csv")
        vector=pd.concat([vector,m])

        
datos=pd.read_csv(r"/home/luisa/Descargas/precipitacion_012019-052022.csv")
vector=pd.concat([vector,datos])
vector.to_csv(d4+"psiata201306-202205.csv")



        
