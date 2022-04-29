#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:11:05 2022

@author: luisa
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

#  2.3 información de la base de datos
eng = 'sqlite:////home/marcelae/Desktop/FACOM/DATA3.db'
#------------------------#----------------------------#-----------------------#
#3. funciones

#3.1 Extracción de datos de un database
# Load de data
def SQL_PD(table_or_sql,eng):
       engine = create_engine(eng)
       conn = engine.connect()
       generator_object = pd.read_sql(table_or_sql,con=conn)
       return generator_object 
   

# 3.2 CORREGIR TILDES, COMAS Y Ñ
def normalizar(df):
    
    # Diccionario con las correcciones
    dic = {'á':'a', 'é':'e','í':'i','ó':'o','ú':'u',",":"",'ñ':'n'}
    
    # Busca en el diccionario el caracter especial
    for key in dic:
        x = re.search(key,df)
        
        # Si lo encuentra, lo reemplaza 
        if x != None:
            df = df.replace(key,dic[key])

    return df,x

     

cod = 21201200

my_query2='''
SELECT CodigoEstacion,FechaObservacion,ValorObservado,NombreEstacion,Departamento,
Municipio,ZonaHidrografica,Latitud,Longitud,DescripcionSensor,UnidadMedida 
FROM temperatura
WHERE (codigoestacion = {})
'''.format(int(cod))

df_est = SQL_PD(my_query2,eng)


x=1
#Datos reemplazados
columnas=["CodigoEstacion","FechaObservacion","ValorObservado"]
T_null=[columnas]
P_null=[columnas]

if (x==1):
    df_est["Departamento"] = pd.DataFrame(df_est["Departamento"].str.lower())
    df_est["Municipio"] = pd.DataFrame(df_est["Municipio"].str.lower())
    df_est["ZonaHidrografica"] = pd.DataFrame(df_est["ZonaHidrografica"].str.lower())

    for index, row in tqdm(df_est.iterrows()):
          
        if (row["ValorObservado"]<0):
            df_est["ValorObservado"][index]="<nil>"
            t_vec=[row["CodigoEstacion"],row["ValorObservado"],row["fechaObservación"]]
            T_null.append(t_vec)
            print("Se encontro un valor menor a cero de= ",
                  row["ValorObservado"], ", en la fecha= ", row["FechaObservacion"])   
            
        # Corrección de nombres
        
        # Busqueda de casos especiales
        x_dep_bog = re.search('bog',row["Departamento"])
        x_dep_sa = re.search('san and',row["Departamento"])
        x_mun = re.search('bog',row["Municipio"])
        
        if x_dep_bog != None:
            row["Departamento"] = "bogota"
            df_est["Departamento"][index] = row["Departamento"]
        if x_mun != None:
            row["Municipio"] = "bogota"
            df_est["Municipio"][index] = row["Municipio"]
        if x_dep_sa != None:
            row["Departamento"] = "san andres"
            df_est["Departamento"][index] = row["Departamento"]
            
       # Corrección de tildes, ñ y comas 
        row["Departamento"],x = normalizar(row["Departamento"])
        
        if x != None:
            df_est["Departamento"][index] = row["Departamento"]
        
        row["Municipio"],x = normalizar(row["Municipio"])
        
        if x != None:
            df_est["Municipio"][index] = row["Municipio"]
        
        row["ZonaHidrografica"],x = normalizar(row["ZonaHidrografica"])
        
        if x != None:
            df_est["ZonaHidrografica"][index] = row["ZonaHidrografica"]
        
if (x==t):
    
    for index, row in df_est.iterrows():
        if (row["ValorObservado"]< -10.0):
            df_est["ValorObservado"][index]="<nil>"
            p_vec=[row["CodigoEstacion"],row["ValorObservado"],row["fechaObservación"]]
            P_null.append(p_vec)
            print("Se encontro un valor menor a cero de= ",
                  row["ValorObservado"], ", en la fecha= ", row["FechaObservacion"])
            
        if (row["ValorObservado"] > 60.0):
            df_est["ValorObservado"][index]="<nil>"
            p_vec=[row["CodigoEstacion"],row["ValorObservado"],row["fechaObservación"]]
            P_null.append(p_vec)
            print("Se encontro un valor menor a cero de= ",
                  row["ValorObservado"], ", en la fecha= ", row["FechaObservacion"])
            
        # Corrección de nombres
        
        # Busqueda de casos especiales
        x_dep_bog = re.search('bog',row["Departamento"])
        x_dep_sa = re.search('san and',row["Departamento"])
        x_mun = re.search('bog',row["Municipio"])
        
        if x_dep_bog != None:
            row["Departamento"] = "bogota"
            df_est["Departamento"][index] = row["Departamento"]
        if x_mun != None:
            row["Municipio"] = "bogota"
            df_est["Departamento"][index] = row["Departamento"]
        if x_dep_sa != None:
            row["Departamento"] = "san andres"
            df_est["Departamento"][index] = row["Departamento"]
            
       # Corrección de tildes, ñ y comas 
        row["Departamento"],x = normalizar(row["Departamento"])
        
        if x != None:
            df_est["Departamento"][index] = row["Departamento"]
        
        row["Municipio"],x = normalizar(row["Municipio"])
        
        if x != None:
            df_est["Municipio"][index] = row["Municipio"]
        
        row["ZonaHidrografica"],x = normalizar(row["ZonaHidrografica"])
        
        if x != None:
            df_est["ZonaHidrografica"][index] = row["ZonaHidrografica"]
    

df_est["fecha"]=pd.to_datetime(df_est['FechaObservacion']).dt.strftime("%d/%m/%Y %X")
#organizar las filas de mayor a menor con respecto a la fecha
df_est = df_est.sort_values(by='fecha')
#Se resetean los indices
df_est=df_est.reset_index(drop=True)
#longitud de filas
n=len(df_est)
#longitud de columnas
shape = df_est.shape
#Obtener el nombre de las columnas
columns_names = df_est.columns.values
#latitud y longitud
lat=df_est.Latitud.unique()
lon=df_est.Longitud.unique()
#Municipio y departamento
mu=df_est.Municipio.unique()
dep=df_est.Departamento.unique()
#Zona hidrografica y nombre de la estación
zh=df_est.ZonaHidrografica.unique()
ne=df_est.NombreEstacion.unique()
#descrición del sensor y unidades
desS=df_est.DescripcionSensor.unique()
unidades=df_est.UnidadMedida.unique()


print("Estación",cod)
print("")
print("INFORMACIÓN INICIAL")
print("")
print("1. La fecha inicial =",df_est["fecha"][0] )
print("2. La fecha final =",df_est["fecha"][n-1] )
print("3. La cantidad de filas y columnas =",shape )
print("4. El nombre de las columnas es=",columns_names)
print("5. Las primeras filas son= ")
print(df_est.head())
print("6. Las últimas filas= ")
print(df_est.tail())
print("")
print("LATITUD Y LONGITUD")
print("")
print("7. latitud=", lat[0])
print("8. longitud=", lon[0])
print("")
print("MUNICIPIO, DEPARTAMENTO, ZONA HIDROGRAFICA Y NOMBRE DE LA ESTACIÓN")
print("")
print("9. Municipio= ", mu[0])
print("10. Departamento= ", dep[0])
print("11. Zona Hidrografica= ", zh[0])
print("12. Nombre de la estación= ", ne[0])
print("")
print("UNIDADES Y OTRAS DESCRIPCIONES")
print("")
print("13. Unidades de la variable de estudio= ", unidades[0])
print("14. Descripción del sensor= ", desS[0])
print("")
    
#CALCULOS
#max, min, promedio
#Valor máximo
maxi=df_est.ValorObservado.max()
mini=df_est.ValorObservado.min()
media=df_est.ValorObservado.mean()
desviacion=np.std(df_est.ValorObservado)
mediana=np.median(df_est.ValorObservado)


print("")
print("ESTADISTICOS")
print("")
print("15. Valor máximo= ", maxi)
print("16. Valor mínimo= ", mini)
print("17. Valor medio= ", media)
print("18. Desviación estandar", desviacion)
print("19. Mediana= ", mediana)



df_est["year"]=pd.to_datetime(df_est['fecha']).dt.year 
df_est["month"]=pd.to_datetime(df_est['fecha']).dt.month
df_est["day"]=pd.to_datetime(df_est['fecha']).dt.day  
df_est["hour"]=pd.to_datetime(df_est['fecha']).dt.hour
month=list(df_est["month"].unique())
month.sort() 
Ma_mes=[]
for i in tqdm(month):
    mes=df_est[df_est.month==i]
    mean_m=mes.ValorObservado.mean(skipna=True)
    Ma_mes.append(mean_m)
    print("Ingresa el promedio del mes",i)
meses=np.array(["Ene","Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", 
                "Sep","Oct", "Nov", "Dic"])
print("")
print("GRAFICOS")
print("")
plt.figure(figsize=(10,5))
plt.title("Ciclo medio anual \n Estación" )
plt.plot(meses,Ma_mes)
plt.xlabel("tiempo (meses)")
plt.ylabel("precipitación "+unidades)
plt.grid()


titulos=["Codigo Estacion","Nombre de estacion","Municipio","Departamento", "Zona Hidrográfica","Latitud"
         ,"Longitud","Fecha Inicial","Fecha Final","Numerofilas","Numero de columnas",
         "Máximo","Mínimo","Promedio","Desviación Estándar","Mediana"]
c1=[cod,ne,mu,dep,zh,lat,lon,df_est["fecha"][0],df_est["fecha"][n-1],n,shape,maxi,mini,media,desviacion,mediana]
#------------------------#----------------------------#-----------------------#

print(c)

m=[m,c]
m=[titulos]

m.append(c1)
m1=pd.DataFrame(m)
m1.head()
print( titulos) 

my_query2='''
SELECT COUNT(CodigoEstacion) FROM temperatura
'''

df_est = SQL_PD(my_query2,eng)
df_est

m = "HOLá"
normalizar(m)
#------------------------#----------------------------#-----------------------#
#luisa
#t="/media/luisa/Datos/documentos/FACOM/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv"
#p="/media/luisa/Datos/documentos/FACOM/P.csv"
# Histogramas con todos los valores

k=pd.read_csv(t,usecols=[3]) 
k2=pd.read_csv(p,usecols=[3]) 
#k.head()


#Temperatura
#Estadisticos
media_t=k["ValorObservado"].mean(skipna=True)
mediana_t=np.median(k)
de_t=np.std(k)
p01_t=np.percentile(k,1)
p02_t=np.percentile(k,2)
p98_t=np.percentile(k,98)
p99_t=np.percentile(k,99)
max_t=np.max(k)
min_t=np.min(k)

print("La media es=",media_t)
print("La mediana es=",mediana_t )
print("La desviación estándar es=", de_t)
print("El Valor máximo= ", max_t)
print("El Valor mínimo= ", min_t)
print("El percentil 1= ",round(p01_t,3))
print("El percentil 2= ",round(p02_t,3))
print("El percentil 98= ",round(p98_t,3))
print("El percentil 99= ",round(p99_t,3))


#histograma
num_bins = 30
plt.figure(figsize=(10,5))
plt.title("Temperatura",fontsize=15)
plt.hist(k["ValorObservado"], num_bins,facecolor = "slateblue",
         alpha=0.75,label="T",edgecolor = "gray")

plt.axvline(x=media_t,color="black",linewidth=1.0,linestyle='-',label=('Media=',round(media_t,3)))
plt.axvline(x=mediana_t,color="black",linewidth=1.0,linestyle='--',
            label=('Mediana=',round(mediana_t,3)))
plt.ylabel("Frecuencia (pr)", fontsize=10)
plt.xlabel("Temperatura [°C]", fontsize=10)
#plt.title("Muestra 1")
plt.grid(color='lightgrey',linewidth=1.0)
#plt.text(1, 65, 'A', fontsize = 15,
#         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.minorticks_on()
plt.legend()

#caja de bigotes
k.boxplot(column="ValorObservado",figsize=(8, 5))
plt.title("Temperatura") 
plt.xticks([1],["Temperatura"])
plt.ylabel("T [°C]", fontsize=12)
plt.xlabel("T",fontsize=12)


#Precipitación
#Estadisticos
media_p=k2["ValorObservado"].mean(skipna=True)
mediana_p=np.median(k2)
de_p=np.std(k2)
p01_p=np.percentile(k2,1)
p02_p=np.percentile(k2,2)
p98_p=np.percentile(k2,98)
p99_p=np.percentile(k2,99)
max_p=np.max(k2)
min_p=np.min(k2)

print("La media es=",media_p)
print("La mediana es=",mediana_p )
print("La desviación estándar es=", de_p)
print("El Valor máximo= ", max_p)
print("El Valor mínimo= ", min_p)
print("El percentil 1= ",round(p01_p,3))
print("El percentil 2= ",round(p02_p,3))
print("El percentil 98= ",round(p98_p,3))
print("El percentil 99= ",round(p99_p,3))


#histograma
num_bins = 30
plt.figure(figsize=(10,5))
plt.title("Precipitación",fontsize=15)
plt.hist(k2["ValorObservado"], num_bins,facecolor = "darkcyan",
         alpha=0.75,label="P",edgecolor = "gray")

plt.axvline(x=media_p,color="black",linewidth=1.0,linestyle='-',label=('Media=',round(media_p,3)))
plt.axvline(x=mediana_p,color="black",linewidth=1.0,linestyle='--',
            label=('Mediana=',round(mediana_p,3)))
plt.ylabel("Frecuencia (pr)", fontsize=10)
plt.xlabel("Precipitación [mm]", fontsize=10)
#plt.title("Muestra 1")
plt.grid(color='lightgrey',linewidth=1.0)
#plt.text(1, 65, 'A', fontsize = 15,
#         bbox=dict(boxstyle="square,pad=0.3", fc="plum", ec="black", lw=2))
plt.minorticks_on()
plt.legend()

#caja de bigotes
k2.boxplot(column="ValorObservado",figsize=(8, 5))
plt.title("Precipitación") 
plt.xticks([1],["Precipitación"])
plt.ylabel("P [mm]", fontsize=12)
plt.xlabel("P",fontsize=12)

