#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fecha: 18 de abril de 2022
lugar: Medellín-Antioquía
Autores: Marcela y Luisa Fernanda Buriticá Ruíz

El proposito de este codigo es analizar dos bases de datos de precipitación
y temperatura del IDEAM. 
"""

#------------------------#----------------------------#-----------------------#
#  1. importar las librerías

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

# 1.1. funciones
# 1.1.1 CORREGIR TILDES, COMAS Y Ñ
def normalizar(df):
    
    # caracteres especiales sin tildes
    s = re.sub(r"[^\w\-]","",df)
    
    # tildes
    s = re.sub(
        	r"([^\u0300-\u036f])[\u0300-\u036f]+", r"\1", 
        	normalize( "NFD", s), 0, re.I
        )
     
    s = normalize( 'NFC', s)

    return s

#1.1.2 Extracción de datos de un database
# Load de data
def SQL_PD(table_or_sql,eng):
       engine = create_engine(eng)
       conn = engine.connect()
       generator_object = pd.read_sql(table_or_sql,con=conn)
       return generator_object 
#------------------------#----------------------------#-----------------------#
#  2. leer las bases de datos
#Si la base de datos ya esta creada por favor agregar # para comentar las 
#lineas ya que no se usaran.

#marcela
#t="/Volumes/DiscoMarcela/facom/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv" 
#p="/Volumes/DiscoMarcela/facom/Precipitaci_n.csv"
#lucy
#t="/home/marcelae/Documents/organizar/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv"
#p="/home/marcelae/Documents/organizar/Precipitaci_n.csv"
#luisa
#t="/media/luisa/Datos/documentos/FACOM/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv"
#p="/media/luisa/Datos/documentos/FACOM/P.csv"
#lucy2
t="/home/marcela/Documents/organizar/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv"
p="/home/marcela/Documents/organizar/Precipitaci_n.csv"


#2.1 información de las columnas 
# 0-CodigoEstacion
# 1-CodigoSensor
# 2-FechaObservacion
# 3-ValorObservado
# 4-NombreEstacion
# 5-Departamento
# 6-Municipio
# 7-ZonaHidrografica
# 8-Latitud
# 9-Longitud
# 10-DescripcionSensor
# 11-UnidadMedida

#CodigoEstacion,FechaObservacion,ValorObservado,NombreEstacion,
#Departamento,Municipio,ZonaHidrografica,Latitud,Longitud

# 2.2 Crear la base de datos

#se cambia x1 por p o por t
x1=p

k=pd.read_csv(x1,usecols=[0])    #Se crea una variable que contenga la longitud del archivo original
n=len(k)                        #longitud de la columna de prueba
k.head()
print(n)
del k

#marcela
#data_base_name = "/Volumes/DiscoMarcela/facom/prueba1.db"    # se asigna un nombre al db
#lucy
#data_base_name = "/home/marcelae/Desktop/FACOM/precipitacion.db"     # se asigna un nombre al db
#lucy2
data_base_name = "/home/marcela/Desktop/FACOM/Bases_de_datos/precipitacion.db"     # se asigna un nombre al db

engine = create_engine('sqlite:///'+data_base_name)     # se crea el motor 
sqlite_connection = engine.connect()                    # se enciende la conexión
step=math.ceil(n*0.001)             # el número es el porcentaje que se va a tomar "dx"
cont=0                  #contador

#Se crear el archivo donde se almacena la información de los datos cambiados en Valor Observado
columnas=["CodigoEstacion","FechaObservacion","ValorObservado"]
T_null=[columnas]
P_null=[columnas]

#Se crea el while que recorra el DataFrame y lo vaya ingresando cada dx
while tqdm(cont <= (n-1)):  
    #La siguiente fila de codigo lo que carga es el dx, se toma una porción y solo se carga
    #el porcentaje que se desea cargar que inicialmente se asigno en cada paso. 
    v=pd.read_csv(x1,nrows=int(step),skiprows=range(1,int(cont)))
    
    if (x1==p):
        v["Departamento"] = pd.DataFrame(v["Departamento"].str.lower())
        v["Municipio"] = pd.DataFrame(v["Municipio"].str.lower())
        v["ZonaHidrografica"] = pd.DataFrame(v["ZonaHidrografica"].str.lower())

        for index, row in tqdm(v.iterrows()):
              
            if (row["ValorObservado"]<0):
                v["ValorObservado"][index]="<nil>"
                t_vec=[row["CodigoEstacion"],row["ValorObservado"],row["FechaObservación"]]
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
                v["Departamento"][index] = row["Departamento"]
            if x_mun != None:
                row["Municipio"] = "bogota"
                v["Municipio"][index] = row["Municipio"]
            if x_dep_sa != None:
                row["Departamento"] = "san andres"
                v["Departamento"][index] = row["Departamento"]
                
           # Corrección de tildes, ñ y comas 
            row["Departamento"] = normalizar(row["Departamento"])
            v["Departamento"][index] = row["Departamento"]
            
            row["Municipio"] = normalizar(row["Municipio"])
            v["Municipio"][index] = row["Municipio"]
            
            row["ZonaHidrografica"] = normalizar(row["ZonaHidrografica"])
            v["ZonaHidrografica"][index] = row["ZonaHidrografica"]
            
    if (x1==t):
        
        v["Departamento"] = pd.DataFrame(v["Departamento"].str.lower())
        v["Municipio"] = pd.DataFrame(v["Municipio"].str.lower())
        v["ZonaHidrografica"] = pd.DataFrame(v["ZonaHidrografica"].str.lower())
        
        for index, row in v.iterrows():
            if (row["ValorObservado"]< -10.0):
                v["ValorObservado"][index]="<nil>"
                p_vec=[row["CodigoEstacion"],row["ValorObservado"],row["FechaObservación"]]
                P_null.append(p_vec)
                print("Se encontro un valor menor a cero de= ",
                      row["ValorObservado"], ", en la fecha= ", row["FechaObservacion"])
                
            if (row["ValorObservado"] > 60.0):
                v["ValorObservado"][index]="<nil>"
                p_vec=[row["CodigoEstacion"],row["ValorObservado"],row["FechaObservación"]]
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
                v["Departamento"][index] = row["Departamento"]
            if x_mun != None:
                row["Municipio"] = "bogota"
                v["Municipio"][index] = row["Municipio"]
            if x_dep_sa != None:
                row["Departamento"] = "san andres"
                v["Departamento"][index] = row["Departamento"]
                
           # Corrección de tildes, ñ y comas 
            row["Departamento"],x = normalizar(row["Departamento"])
            
            if x != None:
                v["Departamento"][index] = row["Departamento"]
            
            row["Municipio"],x = normalizar(row["Municipio"])
            
            if x != None:
                v["Municipio"][index] = row["Municipio"]
            
            row["ZonaHidrografica"],x = normalizar(row["ZonaHidrografica"])
            
            if x != None:
                v["ZonaHidrografica"][index] = row["ZonaHidrografica"]
                
    print("ingresando paso",cont)
    v.to_sql(name='precipitacion',con=sqlite_connection,index=False,if_exists='append') 
    cont=cont+step
    del v
    #print(cont,"_",step)    
sqlite_connection.close()   


#  2.3 información de la base de datos
#lucy
#eng = 'sqlite:////home/marcelae/Desktop/FACOM/DATA3.db'
#luisa
#eng='sqlite:////media/luisa/Datos/documentos/FACOM/gits/FACOM/DATA3.db'
#lucy2
eng='sqlite:////home/marcela/Desktop/FACOM/bases_de_datos/temperatura_1.db'

#------------------------#----------------------------#-----------------------#
#  3. Valores individuales por codigo de estación para las columnas
myquery_unique='''
SELECT DISTINCT "CodigoEstacion","NombreEstacion","Municipio","Departamento", "ZonaHidrografica"
FROM temperatura
'''
df_ubi = SQL_PD(myquery_unique,eng)



#Se elimnan toda la información que sea completamente nula
'''
# Elimina la fila con los valores nulos
for i in range(len(df_ubi)):
    if df_ubi["Municipio"][i] == "<nil>":
        df_ubi = df_ubi.drop([i],axis=0)
'''

# La zona hidrografica aún tiene valores nulos en las posiciones 204 254 277 306 318 340 385
df_ubi.to_csv(r'/home/marcelae/Desktop/FACOM/ubicacion_temperatura.csv', index=None, sep=';')
#------------------------#----------------------------#-----------------------#
#  4. se genera el archivo con la informaición por estación


#  4.1 Codigos individuales 

my_query1='''
SELECT  DISTINCT CodigoEstacion FROM temperatura
'''
codigo = SQL_PD(my_query1,eng)
print(codigo)

#  4.2 Nombres de las columnas para el archivo final y vector para guardar la información
titulos=["Codigo Estacion","Nombre de estacion","Municipio","Departamento", "Zona Hidrográfica","Latitud"
         ,"Longitud","Fecha Inicial","Fecha Final","Numerofilas y columnas",
         "Máximo","Mínimo","Promedio","Desviación Estándar","Mediana"]
vector=[titulos]

#  4.3 Lectura del archivo 
print(" se empieza a leer por columna")

for i in tqdm (range(550)):
#for i in tqdm(codigo):
    # se determina el valor i
    cod = codigo["CodigoEstacion"][i]
    
    #--------------------------------------------------------#
    
    #Valores individuales de columna
    my_query3='''
    SELECT DISTINCT NombreEstacion,Departamento,Municipio,ZonaHidrografica,Latitud,Longitud,DescripcionSensor,UnidadMedida 
    FROM temperatura
    WHERE (codigoestacion = {})
    '''.format(int(cod))
    df_unicos = SQL_PD(my_query3,eng)
    
    #--------------------------------------------------------#

    #Se obtiene el valor observado y la fecha del valor para la estación de analisis
    my_query2='''
    SELECT FechaObservacion,ValorObservado, 
    FROM temperatura
    WHERE (codigoestacion = {})
    '''.format(int(cod))
    df_est = SQL_PD(my_query2,eng)
    
    #--------------------------------------------------------#

    #fechas
    df_est["fecha"]=pd.to_datetime(df_est['FechaObservacion'],format='%m/%d/%Y %I:%M:%S %p')
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
    
    #--------------------------------------------------------#

    #Valores unicos
    #latitud y longitud
    lat=df_unicos["Latitud"][0]
    lon=df_unicos["Longitud"][0]
    #Municipio y departamento
    mu=df_unicos["Municipio"][0]
    dep=df_unicos["Departamento"][0]
    #Zona hidrografica y nombre de la estación
    zh=df_unicos["ZonaHidrografica"][0]
    ne=df_unicos["NombreEstacion"][0]
    #descrición del sensor y unidades
    desS=df_unicos["DescripcionSensor"][0]
    unidades=df_unicos["UnidadMedida"][0]
    print("")
    print("#---------------------------#")
    print("Estación",cod)
    print("")
    print("INFORMACIÓN INICIAL")
    print("")
    print("1. La fecha inicial =",df_est["fecha"][0] )
    print("2. La fecha final =",df_est["fecha"][n-1] )
    print("3. Muestreo valores iniciales =",(df_est["fecha"][1]-df_est["fecha"][0]).seconds/60, "min")
    print("4. Muestreo valores finales =",(df_est["fecha"][n-1]-df_est["fecha"][n-2]).seconds/60, "min")
    print("5. La cantidad de filas y columnas =",shape )
    print("6. El nombre de las columnas es=",columns_names)
    print("7. Las primeras filas son= ")
    print(df_est.head())
    print("8. Las últimas filas= ")
    print(df_est.tail())
    print("")
    print("LATITUD Y LONGITUD")
    print("")
    print("9. latitud=", lat[0])
    print("10. longitud=", lon[0])
    print("")
    print("MUNICIPIO, DEPARTAMENTO, ZONA HIDROGRAFICA Y NOMBRE DE LA ESTACIÓN")
    print("")
    print("11. Municipio= ", mu[0])
    print("12. Departamento= ", dep[0])
    print("13. Zona Hidrografica= ", zh[0])
    print("14. Nombre de la estación= ", ne[0])
    print("")
    print("UNIDADES Y OTRAS DESCRIPCIONES")
    print("")
    print("15. Unidades de la variable de estudio= ", unidades[0])
    print("16. Descripción del sensor= ", desS[0])
    print("")

    #--------------------------------------------------------#
        
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
    print("17. Valor máximo= ", maxi)
    print("18. Valor mínimo= ", mini)
    print("19. Valor medio= ", media)
    print("20. Desviación estandar", desviacion)
    print("21. Mediana= ", mediana)


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
    
    c=[cod,ne[0],mu[0],dep[0],zh[0],lat[0],lon[0],df_est["fecha"][0],df_est["fecha"][n-1],
       (df_est["fecha"][1]-df_est["fecha"][0]).seconds/60,(df_est["fecha"][n-1]-df_est["fecha"][n-2]).seconds/60, 
       shape,maxi,mini,media,desviacion,mediana]
    
    vector.append(c)
    #print(vector)
    print("termina" ,i)
    print("#---------------------------#")

df=pd.DataFrame(vector)
df.head()
   
df.to_csv(r'/media/luisa/Datos/documentos/FACOM/gits/FACOM/temperatura.csv', 
          header=None, index=None, sep=';')
print("se guarda el archivo")

#------------------------#----------------------------#-----------------------#
#------------------------#----------------------------#-----------------------#
#------------------------#----------------------------#-----------------------#
#------------------------#----------------------------#-----------------------#
#------------------------#----------------------------#-----------------------#