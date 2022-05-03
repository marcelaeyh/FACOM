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
eng = 'sqlite:////home/marcelae/Desktop/FACOM/db/temperatura_2.db'
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

#---------------------------------------#------------------------------------#
# abril 29 de 2022  optimización de la lectura del archivo de salida csv


cod = 21201200
#Valores individuales de columna
my_query3='''
SELECT DISTINCT NombreEstacion,Departamento,Municipio,ZonaHidrografica,Latitud,Longitud,DescripcionSensor,UnidadMedida 
FROM temperatura
WHERE (codigoestacion = {})
'''.format(int(cod))
df_est = SQL_PD(my_query3,eng)
print(df_est)
print(df_est["NombreEstacion"][0])
df_est.head()


#---------------------------------------#------------------------------------#
#abril 29 de 2022 encontrar los codigos de estación para el profe daniel


#Notas adicionales, la información de los aeropuertos de julio tiene 46 estaciones, 
#el de el profesor daniel tiene 17.


#eng = 'sqlite:////home/marcelae/Desktop/FACOM/db/temperatura_2.db'
eng = 'sqlite:////home/marcelae/Desktop/FACOM/db/precipitacion_2.db'



#archivo de julio con la base de datos de precipitación
datos=pd.read_csv("/home/marcelae/Desktop/FACOM/otros_documentos/Aeropuertos.csv", usecols=[2,3])
datos.columns=["lon","lat"]
datos.tail()

#archivo con estaciones no encontradas
titulos1=["lat","lon"]
vector1=[titulos1]

#archivo con estaciones encontradas
titulos=["CodigoEstacion","NombreEstacion","Departamento","Municipio","ZonaHidrografica","Latitud","Longitud"]
vector=[titulos]
variacion=0.1

for i in  tqdm(range(len(datos))):
    my_query3='''
    SELECT DISTINCT CodigoEstacion,NombreEstacion,Departamento,Municipio,ZonaHidrografica,Latitud,Longitud
    FROM precipitacion
    WHERE (Latitud <= {} AND Latitud >= {}) AND (Longitud <= {} AND Longitud >= {})
    '''.format(datos["lat"][i]+variacion,datos["lat"][i]-variacion,datos["lon"][i]+variacion,datos["lon"][i]-variacion)

    df_est = SQL_PD(my_query3,eng)
    n=len(df_est)
    if n != 0 :
        #print("el paso de tiempo ", i, " tiene información disponible")
        c=(df_est["CodigoEstacion"][0],df_est["NombreEstacion"][0],df_est["Departamento"][0],
                      df_est["Municipio"][0],df_est["ZonaHidrografica"][0],df_est["Latitud"][0],df_est["Longitud"][0])
        vector.append(c)
        
    else:
        print("el paso de tiempo ",i, "no tiene información disponible en las coordenadas"
              ,"(",datos["lon"][i],",",datos["lat"][i],")")
        c1=(datos["lon"][i],datos["lat"][i])
        vector1.append(c1)
 
print(" el archivo final tiene ", len(vector), " filas")           
#print(vector)

#guardar el archivo csv
df=pd.DataFrame(vector)
df_noencontrados=pd.DataFrame(vector1)


#luisa 
#df.to_csv(r'/media/luisa/Datos/documentos/FACOM/gits/FACOM/temperatura.csv',header=None, index=None, sep=';')
#lucy
df.to_csv(r'/home/marcelae/Desktop/FACOM/aeropuertos/julio_estacionesAeropuertos.csv',header=None, index=None, sep=';')
df_noencontrados.to_csv(r'/home/marcelae/Desktop/FACOM/aeropuertos/julio_NoE.csv',header=None, index=None, sep=';')

print("se guarda el archivo")

#-----------------------------------------------------------#-----------------------------------#

#lucy
#eng = 'sqlite:////home/marcelae/Desktop/FACOM/db/temperatura_2.db'
eng = 'sqlite:////home/marcelae/Desktop/FACOM/db/precipitacion_2.db'
#luisa
#eng="sqlite:////media/luisa/Datos/FACOM/gits/FACOM/db/precipitacion_2.db"

#El de daniel ya tiene todas las correcciones

# archivo del profe Daniel con la base de datos de precipitación
#lucy
datos=pd.read_csv("/home/marcelae/Desktop/FACOM/aeropuertos/airport_coord.csv", usecols=[1,2])
#lusia
#datos=pd.read_csv("/media/luisa/Datos/FACOM/gits/FACOM/aeropuertos/airport_coord.csv", usecols=[1,2])

datos.columns=["lon","lat"]
datos.tail()

#archivo con estaciones no encontradas
titulos1=["lat","lon"]
vector1=[titulos1]

#archivo con estaciones encontradas
titulos=["i","CodigoEstacion","NombreEstacion","Departamento","Municipio","ZonaHidrografica","Latitud","Longitud"]
vector=[titulos]

#cuando encuentra más de 1 estación
titulos2=["i","CodigoEstacion","NombreEstacion","Departamento","Municipio","ZonaHidrografica","Latitud","Longitud"]
vector2=[titulos2]
variacion=0.1

for i in  tqdm(range(len(datos))):
    my_query3='''
    SELECT DISTINCT CodigoEstacion,NombreEstacion,Departamento,Municipio,ZonaHidrografica,Latitud,Longitud
    FROM precipitacion
    WHERE (Latitud <= {} AND Latitud >= {}) AND (Longitud <= {} AND Longitud >= {})
    '''.format(datos["lat"][i]+variacion,datos["lat"][i]-variacion,datos["lon"][i]+variacion,datos["lon"][i]-variacion)

    df_est = SQL_PD(my_query3,eng)
    n=len(df_est)
    if n== 0 :
        print("el paso de tiempo ",i, "no tiene información disponible en las coordenadas"
              ,"(",datos["lon"][i],",",datos["lat"][i],")")
        c1=(datos["lon"][i],datos["lat"][i])
        vector1.append(c1)
    if n != 0 :
        if n == 1:
            
            #print("el paso de tiempo ", i, " tiene información disponible")
            c=(i,df_est["CodigoEstacion"][0],df_est["NombreEstacion"][0],df_est["Departamento"][0],
                      df_est["Municipio"][0],df_est["ZonaHidrografica"][0],df_est["Latitud"][0],
                      df_est["Longitud"][0])
            print(i, "- El codigo de estación es= ",df_est["CodigoEstacion"][0] )
            vector.append(c)
        elif n > 1:
            print("el paso de tiempo ",i, " tiene ",n," estaciones que coindice")
            for j in range(n):
                print(i, "- El codigo de estación es= ",df_est["CodigoEstacion"][j] )
                c2=(i,df_est["CodigoEstacion"][j],df_est["NombreEstacion"][j],df_est["Departamento"][j],
                          df_est["Municipio"][j],df_est["ZonaHidrografica"][j],df_est["Latitud"][j],
                          df_est["Longitud"][j])
                vector2.append(c2)
            
    
 
print(" el archivo final tiene ", len(vector), " filas")           
#print(vector)

#guardar el archivo csv
df=pd.DataFrame(vector)
df_noencontrados=pd.DataFrame(vector1)
df_varios=pd.DataFrame(vector2)
#luisa 
#df.to_csv(r'/media/luisa/Datos/documentos/FACOM/gits/FACOM/temperatura.csv',header=None, index=None, sep=';')
#lucy
df.to_csv(r'/home/marcelae/Desktop/FACOM/aeropuertos/daniel_estacionesAeropuertos.csv',header=None, index=None, sep=';')
df_noencontrados.to_csv(r'/home/marcelae/Desktop/FACOM/aeropuertos/daniel_NoE.csv',header=None, index=None, sep=';')
df_varios.to_csv(r'/home/marcelae/Desktop/FACOM/aeropuertos/daniel_varios.csv',header=None, index=None, sep=';')

print("se guarda el archivo")
#-------------------------------------------------#--------------------------------#

# 30 de abril de 2022 prueba para sacar la información

#se va a sacar la información de las estaciones que se tienen hasta el momento para el profesor Daniel
#en el año 2018.

#Se saca la información
#luisa
#datos=pd.read_csv(r'/media/luisa/Datos/FACOM/gits/FACOM/aeropuertos/Final_CodigoEstacion_Aeropuertos.csv',
#                  usecols=[1],skiprows=range(1,3))

#lucy
datos=pd.read_csv(r'/home/marcelae/Desktop/FACOM/aeropuertos/Final_CodigoEstacion_Aeropuertos.csv',
                  usecols=[1],skiprows=(range(3,19)))
datos

#lucy
#eng = 'sqlite:////home/marcelae/Desktop/FACOM/db/temperatura_2.db'
eng = 'sqlite:////home/marcelae/Desktop/FACOM/db/precipitacion_2.db'
#luisa
#eng="sqlite:////media/luisa/Datos/FACOM/gits/FACOM/db/precipitacion_2.db"


#crean los vectores para guardar la información
titulosunicos=["CodigoEstacion","NombreEstacion","Departamento","Municipio",
         "ZonaHidrografica","Latitud","Longitud"]
unicos=[titulosunicos]
cod_verificar=["Codigo"]

#vector para almacenar los resultados del 2018
titulos=["fecha","CodigoEstacion","ValorObservado"]
vector=[titulos]
vector=pd.DataFrame(vector)
vector.columns=["fecha","CodigoEstacion","ValorObservado"]
vector=vector.drop([0],axis=0)
vector

for i in tqdm(range(len(datos))) :
    cod=datos["CodigoEstacion"][i]
    
    my_query2='''
    SELECT  DISTINCT CodigoEstacion,NombreEstacion,Departamento,Municipio,
    ZonaHidrografica,Latitud,Longitud
    FROM precipitacion
    WHERE (codigoestacion = {})
    '''.format(int(cod))

    df = SQL_PD(my_query2,eng)
    n=len(df)
    if n==1 :
        print(cod, " Tiene información única.")
        a=(df["CodigoEstacion"][0],df["NombreEstacion"][0],df["Departamento"][0],
                  df["Municipio"][0],df["ZonaHidrografica"][0],df["Latitud"][0],
                  df["Longitud"][0])
        unicos.append(a)   
    else:
        print( "El codigo ",cod,"tiene más de un valor unico, verificar.")
        cod_verificar.append(cod)
        
    print("--------#----------------#-------")
    
    my_query1='''
    SELECT  CodigoEstacion,FechaObservacion,ValorObservado
    FROM precipitacion
    WHERE (codigoestacion = {})
    '''.format(int(cod))

    df = SQL_PD(my_query1,eng)

    df["fecha"]=pd.to_datetime(df["FechaObservacion"],format='%m/%d/%Y %I:%M:%S %p')
    df.index=df["fecha"]
    df.drop(["FechaObservacion","fecha"],axis=1,inplace=True)
    df_2018=df.loc["2018-01":"2018-12"]
    df_2018=df_2018.sort_values("fecha")
    df_2018.reset_index(inplace=True)
    

    print("ingresan los valores para el año 2018 de la estación= ", cod)
    vector=vector.append(df_2018,ignore_index=True)
    print("termina= ", cod)
    
#Se almacenan los dataframe
unicos_df=pd.DataFrame(unicos)
vector_df=pd.DataFrame(vector)
cod_verificar_df=pd.DataFrame(cod_verificar)

vector_df = vector_df.sort_values("fecha")
vector_df

#guardar archivos
vector_df.to_csv(r'/home/marcelae/Desktop/FACOM/aeropuertos/amazonas_PDaniel_2018.csv',
                 header=None, index=None, sep=';')
unicos_df.to_csv(r'/home/marcelae/Desktop/FACOM/aeropuertos/unicosa_PDaniel.csv',
                 header=None, index=None, sep=';')
cod_verificar_df.to_csv(r'/home/marcelae/Desktop/FACOM/aeropuertos/revisarcoda_PDaniel.csv',
                 header=None, index=None, sep=';')

daniel = pd.read_csv("/home/marcelae/Desktop/FACOM/aeropuertos/aeropuertos_PDaniel_2018.csv",sep=';')
daniel
daniel.append(vector_df)
vector_df["CodigoEstacion"] = vector_df["CodigoEstacion"].replace(["4815010"],"4815050")
vector_df

#-----------------------------------#------------------------------------#----------#
#estaciones para revisar
#luisa
#datos=pd.read_csv(r"/media/luisa/Datos/FACOM/gits/FACOM/aeropuertos/revisarcod_PDaniel.csv")
#lucy
datos=pd.read_csv(r"/home/marcelae/Desktop/FACOM/aeropuertos/revisarcod_PDaniel.csv")
#lucy
#eng = 'sqlite:////home/marcelae/Desktop/FACOM/db/temperatura_2.db'
eng = 'sqlite:////home/marcelae/Desktop/FACOM/db/temperatura_2.db'
#luisa
#eng="sqlite:////media/luisa/Datos/FACOM/gits/FACOM/db/precipitacion_2.db"

cod=datos["Codigo"][4]

my_query2='''
SELECT CodigoEstacion,FechaObservacion,ValorObservado,NombreEstacion,Departamento,Municipio,
ZonaHidrografica,Latitud,Longitud
FROM temperatura
WHERE (codigoestacion = {})
'''.format(int(cod))
df = SQL_PD(my_query2,eng)
df

for i in tqdm(range(len(datos))) :
    cod=datos["Codigo"][i]
    
    my_query2='''
    SELECT  DISTINCT CodigoEstacion,NombreEstacion,Departamento,Municipio,
    ZonaHidrografica,Latitud,Longitud
    FROM precipitacion
    WHERE (codigoestacion = {})
    '''.format(int(cod))

    df = SQL_PD(my_query2,eng)
    print("La estación ",cod, "tiene valores =")
    print(df)
    
#-----------------------------------#------------------------------------#----------#
#2 de mayo se trabaja en el archivo de entrega de daniel
    
    
    
#lucy
datos=pd.read_csv(r'/home/marcelae/Desktop/FACOM/aeropuertos/Final_CodigoEstacion_Aeropuertos.csv',
                  usecols=[1],skiprows=(range(3,19)))
datos

#lucy
#eng = 'sqlite:////home/marcelae/Desktop/FACOM/db/temperatura_2.db'
eng = 'sqlite:////home/marcelae/Desktop/FACOM/db/precipitacion_2.db'


#  4.2 Nombres de las columnas para el archivo final y vector para guardar la información
titulos=["Codigo Estacion","Nombre de estacion","Municipio","Departamento", "Zona Hidrográfica","Latitud"
         ,"Longitud","Fecha Inicial","Fecha Final","Muestreo valores iniciales","Muestreo valores finales","Numerofilas y columnas",
         "Máximo","Mínimo","Promedio","Desviación Estándar","Mediana"]
vector=[titulos]

#  4.3 Lectura del archivo 
print(" se empieza a leer por columna")

for i in tqdm (range(len(datos))):
#for i in tqdm(codigo):
    # se determina el valor i
    cod = datos["CodigoEstacion"][i]
    
    #--------------------------------------------------------#
    
    #Valores individuales de columna
    my_query3='''
    SELECT DISTINCT NombreEstacion,Departamento,Municipio,ZonaHidrografica,Latitud,Longitud,DescripcionSensor,UnidadMedida 
    FROM precipitacion
    WHERE (codigoestacion = {})
    '''.format(int(cod))
    df_unicos = SQL_PD(my_query3,eng)
    
    #--------------------------------------------------------#

    #Se obtiene el valor observado y la fecha del valor para la estación de analisis
    my_query2='''
    SELECT FechaObservacion,ValorObservado 
    FROM precipitacion
    WHERE (codigoestacion = {})
    '''.format(int(cod))
    df_est = SQL_PD(my_query2,eng)
    
    #--------------------------------------------------------#
    df["fecha"]=pd.to_datetime(df["FechaObservacion"],format='%m/%d/%Y %I:%M:%S %p')
    df.index=df["fecha"]
    df.drop(["FechaObservacion","fecha"],axis=1,inplace=True)
    df_2018=df.loc["2018-01":"2018-12"]
    df_2018=df_2018.sort_values("fecha")
    df_2018.reset_index(inplace=True)

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
        print("Ingresa el promed|io del mes",i)
    meses=np.array(["Ene","Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", 
                    "Sep","Oct", "Nov", "Dic"])
    print("")
    print("GRAFICOS")
    print("")
    plt.figure(figsize=(10,5))
    plt.title('Temperatura Superficial (°C) \n Promedio Anual de \n' + meses[i]+ 
              ' 2011-2015', size=20, loc='center', pad=8)
    plt.title("Ciclo medio anual \n Estación" )
    plt.plot(meses,Ma_mes)
    plt.xlabel("tiempo (meses)")
    plt.ylabel("precipitación "+unidades)
    plt.grid()

    c=[cod,ne,mu,dep,zh,lat,lon,df_est["fecha"][0],df_est["fecha"][n-1],
       (df_est["fecha"][1]-df_est["fecha"][0]).seconds/60,(df_est["fecha"][n-1]-df_est["fecha"][n-2]).seconds/60, 
       shape,maxi,mini,media,desviacion,mediana]
    
    
    
    vector.append(c)
    #print(vector)
    print("termina" ,i)
    print("#---------------------------#")

df=pd.DataFrame(vector)
df

#------------------------#----------------------------#-----------------------#

# 2 de mayo, catalogo de estaciones

engt= 'sqlite:////home/marcelae/Desktop/FACOM/db/temperatura_2.db'
engp= 'sqlite:////home/marcelae/Desktop/FACOM/db/precipitacion_2.db'
#------------------------#----------------------------#-----------------------#

catalogo = pd.read_csv(r"/home/marcelae/Desktop/FACOM/otros_documentos/Cat_logo_Nacional_de_Estaciones_del_IDEAM.csv",usecols=[0])

catalogo["p"]=np.zeros(len(catalogo))
catalogo["t"]=np.zeros(len(catalogo))
catalogo


for i in range(len (catalogo)):
    cod=catalogo["Codigo"][i]
    #Lectura de codigos en ambas bases de datos
    #od=52057100
   
   
    my_query3='''
    SELECT DISTINCT CodigoEstacion
    FROM precipitacion
    WHERE "CodigoEstacion" = {}
    '''.format(int(cod))
    df_p = SQL_PD(my_query3,engp)

    my_query2='''
    SELECT DISTINCT CodigoEstacion
    FROM temperatura
    WHERE "CodigoEstacion" = {}
    '''.format(int(cod))
    df_t = SQL_PD(my_query2,engt)
   
    if df_p["CodigoEstacion"][0] ==cod :
        print(cod,"Tiene precipitacion")
        catalogo["p"][i]=1
    if df_t["CodigoEstacion"][0] ==cod :
        print(cod,"Tiene temperatura")
        catalogo["t"][i]=1
   
#----------------------------------------#--------------------------------#
#2 de mayo de 2022 
engt= 'sqlite:////home/marcelae/Desktop/FACOM/db/temperatura_2.db'
engp= 'sqlite:////home/marcelae/Desktop/FACOM/db/precipitacion_2.db'
cod=26135502
#------------------------#----------------------------#--------------
#Organizando la función para sacar estadisticos


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

