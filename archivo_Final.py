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
eng = 'sqlite:////home/marcelae/Desktop/FACOM/db/precipitacion_2.db'
#luisa
#eng='sqlite:////media/luisa/Datos/documentos/FACOM/gits/FACOM/DATA3.db'
#lucy2
#eng='sqlite:////home/marcela/Desktop/FACOM/bases_de_datos/temperatura_1.db'

#------------------------#----------------------------#-----------------------#
#  3. Valores individuales por codigo de estación para las columnas
myquery_unique='''
SELECT DISTINCT "CodigoEstacion","NombreEstacion","Municipio","Departamento", "ZonaHidrografica"
FROM precipitacion
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
df_ubi.to_csv(r'/home/marcelae/Desktop/FACOM/otros_documentos/ubicacion_precipitacion.csv', index=None, sep=';')
#------------------------#----------------------------#-----------------------#
#  4. se genera el archivo con la informaición por estación

#columnas son los nombres de las columnas para buscar, tabla es el nombre de la
#tabla en la que se va a buscar, por ejemplo:
#columnas="Municipio", tabla="precipitacion"
def my_query_distinct(columnas,tabla,eng):
    my_query='''
    SELECT DISTINCT {} 
    FROM {}
    '''.format(columnas,tabla)
    df = SQL_PD(my_query,eng)
    return df

#columnas son los nombres de las columnas para buscar, tabla es el nombre de la
#tabla en la que se va a buscar, where es la condición de busqueda, por ejemplo :
#columnas="Municipio", tabla="precipitacion", where="CodigoEstacion = {}"
def my_query_distinct_where(columnas,tabla,eng,where,cod):
    my_query='''
    SELECT DISTINCT {} 
    FROM {}
    WHERE ({}={})
    '''.format(columnas,tabla,where,cod)
    df = SQL_PD(my_query,eng)
    return df

def my_query_where(columnas,tabla,eng,where,cod):
    my_query='''
    SELECT {} 
    FROM {}
    WHERE ({}={})
    '''.format(columnas,tabla,where,cod)
    df = SQL_PD(my_query,eng)
    return df

def analisis_variable(tabla, eng,direccion,direccion2,direccion3):
    #creación de vectores
    titulos=["Codigo Estacion","Nombre de estacion","Municipio","Departamento", "Zona Hidrográfica","Latitud"
             ,"Longitud","Fecha Inicial","Fecha Final","Muestreo valores iniciales","Muestreo valores finales","Numerofilas y columnas",
             "Máximo","Mínimo","Promedio","Desviación Estándar","Mediana"]
    vector=[titulos]
    
    #encontrar los codigos de la base de datos ingresada
    columnas="CodigoEstacion"
    datos=my_query_distinct(columnas,tabla,eng)
    for i in tqdm(range(len(datos))):
        cod = datos["CodigoEstacion"][i]
        #valores individuales de la base de datos para el codigo
        columnas1 = "NombreEstacion,Departamento,Municipio,ZonaHidrografica,Latitud,Longitud,DescripcionSensor,UnidadMedida"
        where = "CodigoEstacion"
        unicos_df = my_query_distinct_where(columnas1,tabla,eng,where,cod)
        #Valores variables de fecha y valor observado
        columnas2="FechaObservacion,ValorObservado "
        variables_df=my_query_where(columnas2,tabla,eng,where,cod)
        
        #-------------------------------------------------------------------#
        
        #fechas
        variables_df["fecha"]=pd.to_datetime(variables_df['FechaObservacion'],format='%m/%d/%Y %I:%M:%S %p')
        #organizar las filas de mayor a menor con respecto a la fecha
        variables_df = variables_df.sort_values(by='fecha')
        #Se resetean los indices
        variables_df=variables_df.reset_index(drop=True)
        #longitud de filas
        n=len(variables_df)
        #longitud de columnas
        shape = variables_df.shape
        #Obtener el nombre de las columnas
        #columns_names = variables_df.columns.values
        
        #Valores unicos
        #latitud y longitud
        lat=unicos_df["Latitud"][0]
        lon=unicos_df["Longitud"][0]
        #Municipio y departamento
        mu=unicos_df["Municipio"][0]
        dep=unicos_df["Departamento"][0]
        #Zona hidrografica y nombre de la estación
        zh=unicos_df["ZonaHidrografica"][0]
        ne=unicos_df["NombreEstacion"][0]
        #descrición del sensor y unidades
        desS=unicos_df["DescripcionSensor"][0]
        unidades=unicos_df["UnidadMedida"][0]
        
        print("")
        print("#---------------------------#")
        print("Estación",cod)
        print("")
        print("INFORMACIÓN INICIAL")
        print("")
        print("1. La fecha inicial =",variables_df["fecha"][0] )
        print("2. La fecha final =",variables_df["fecha"][n-1] )
        print("3. Muestreo valores iniciales =",(variables_df["fecha"][1]-
                                                 variables_df["fecha"][0]).seconds/60, "min")
        print("4. Muestreo valores finales =",(variables_df["fecha"][n-1]-
                                               variables_df["fecha"][n-2]).seconds/60, "min")
        print("5. La cantidad de filas y columnas =",shape )
        #print("6. El nombre de las columnas es=",columns_names)
        print("7. Las primeras filas son= ")
        print(variables_df.head())
        print("8. Las últimas filas= ")
        print(variables_df.tail())
        print("")
        print("LATITUD Y LONGITUD")
        print("")
        print("9. latitud=", lat)
        print("10. longitud=", lon)
        print("")
        print("MUNICIPIO, DEPARTAMENTO, ZONA HIDROGRAFICA Y NOMBRE DE LA ESTACIÓN")
        print("")
        print("11. Municipio= ", mu)
        print("12. Departamento= ", dep)
        print("13. Zona Hidrografica= ", zh)
        print("14. Nombre de la estación= ", ne)
        print("")
        print("UNIDADES Y OTRAS DESCRIPCIONES")
        print("")
        print("15. Unidades de la variable de estudio= ", unidades)
        print("16. Descripción del sensor= ", desS)
        print("")
        
        #CALCULOS
        #max, min, promedio
        #Valor máximo
        maxi=variables_df.ValorObservado.max()
        mini=variables_df.ValorObservado.min()
        media=variables_df.ValorObservado.mean()
        desviacion=np.std(variables_df.ValorObservado)
        mediana=np.median(variables_df.ValorObservado)

        print("")
        print("ESTADISTICOS")
        print("")
        print("17. Valor máximo= ", maxi)
        print("18. Valor mínimo= ", mini)
        print("19. Valor medio= ", media)
        print("20. Desviación estandar", desviacion)
        print("21. Mediana= ", mediana)


        variables_df["year"]=pd.to_datetime(variables_df['fecha']).dt.year 
        variables_df["month"]=pd.to_datetime(variables_df['fecha']).dt.month
        variables_df["day"]=pd.to_datetime(variables_df['fecha']).dt.day  
        variables_df["hour"]=pd.to_datetime(variables_df['fecha']).dt.hour
        month=list(variables_df["month"].unique())
        month.sort() 
        hour=list(variables_df["hour"].unique())
        hour.sort()
        
        H=[]
        for j in tqdm(hour):
            hora=variables_df[variables_df.hour==j]
            mean_h=hora.ValorObservado.mean(skipna=True)
            H.append(mean_h)
            #print("Ingresa")
        
        print("")
        print("GRAFICOS")
        print("")
        
        plt.figure(figsize=(10,5))
        plt.title("Ciclo medio diurno \n Estación " +str(cod) +" - "+ne
                  , size=20, loc='center', pad=8)
        plt.plot(hour,H)
        plt.xlabel("Tiempo (horas)")
        plt.ylabel(desS+" ("+unidades+")")
        plt.grid()
        plt.savefig(direccion3+'CMD'  + '_IDEAM-' + str(cod) + '_' + str(i) + '.png') 
        
        Ma_mes=[]
        for j in tqdm(month):
            mes=variables_df[variables_df.month==j]
            mean_m=mes.ValorObservado.mean(skipna=True)
            Ma_mes.append(mean_m)
            #print("Ingresa el promed|io del mes",j)
        meses=np.array(["Ene","Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", 
                        "Sep","Oct", "Nov", "Dic"])
        
        plt.figure(figsize=(10,5))
        plt.title("Ciclo medio anual \n Estación " +str(cod) +" - "+ne
                  , size=20, loc='center', pad=8)
        #plt.title("Ciclo medio anual \n Estación" )
        plt.plot(meses,Ma_mes)
        plt.xlabel("Tiempo en meses")
        plt.ylabel(desS+" ("+unidades+")")
        plt.grid()
        plt.savefig(direccion+'CMA'  + '_IDEAM-' + str(cod) + '_' + str(i) + '.png')  

        c=[cod,ne,mu,dep,zh,lat,lon,variables_df["fecha"][0],variables_df["fecha"][n-1],
           (variables_df["fecha"][1]-variables_df["fecha"][0]).seconds/60,
           (variables_df["fecha"][n-1]-variables_df["fecha"][n-2]).seconds/60, 
           shape,maxi,mini,media,desviacion,mediana]
        
        vector.append(c)
        #print(vector)
        print("termina" ,i, "-",cod)
        print("#---------------------------#")
    print("se termina de analizar la base de datos")
    df_final=pd.DataFrame(vector)
    df_final.to_csv(direccion2,sep=";")
    return(df_final)

    

#df=pd.DataFrame(vector)
direccion="/home/marcelae/Desktop/FACOM/png/precipitacion_completo/anual/"
direccion2="/home/marcelae/Desktop/FACOM/otros_documentos/prueba.csv"
direccion3="/home/marcelae/Desktop/FACOM/png/precipitacion_completo/diurno/"
tabla="precipitacion"
p=analisis_variable(tabla, engp,direccion,direccion2,direccion3)
#------------------------#----------------------------#-----------------------#
#------------------------#----------------------------#-----------------------#
#------------------------#----------------------------#-----------------------#
#------------------------#----------------------------#-----------------------#
#------------------------#----------------------------#-----------------------#