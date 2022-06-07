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
#datos=pd.read_csv(r'/home/marcelae/Desktop/FACOM/aeropuertos/Final_CodigoEstacion_Aeropuertos.csv',
#                  usecols=[1])
#Lucy2
datos=pd.read_csv(r'/home/marcela/Desktop/FACOM/aeropuertos/Final_CodigoEstacion_Aeropuertos.csv',
                  usecols=[1],skiprows=range(3,19))
datos

#lucy
eng = 'sqlite:////home/marcela/Desktop/FACOM/db/temperatura_2.db'
#eng = 'sqlite:////home/marcelae/Desktop/FACOM/db/precipitacion_2.db'
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
    FROM temperatura
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
    FROM temperatura
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
vector_df.to_csv(r'/home/marcela/Desktop/FACOM/aeropuertos/amazonas_TDaniel_2018.csv',
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
# 2 de mayo - Marcela - identificacion de estaciones de las bases de datos en el catalogo nacional
# pruebas de archivo temperatura y precipitacion

engt= 'sqlite:////home/marcelae/Desktop/FACOM/db/temperatura_2.db'
engp= 'sqlite:////home/marcelae/Desktop/FACOM/db/precipitacion_2.db'
#------------------------#----------------------------#-----------------------#

# Se descarga el catalogo de estaciones
catalogo = pd.read_csv(r"/home/marcelae/Desktop/FACOM/otros_documentos/Cat_logo_Nacional_de_Estaciones_del_IDEAM.csv",usecols=[0])

# Se crean dos columnas para almacenar los datos
catalogo["p"]=np.zeros(len(catalogo))
catalogo["t"]=np.zeros(len(catalogo))
catalogo

# Se busca la informacion de los codigos distintos para temperatura y precipitacion
my_query3='''
SELECT DISTINCT CodigoEstacion
FROM precipitacion
'''

df_p = SQL_PD(my_query3,engp)

my_query2='''
SELECT DISTINCT CodigoEstacion
FROM temperatura
'''

df_t = SQL_PD(my_query2,engt)

# Listas vacias para almacenar
malos_t=[]
malos_p=[]

# Busqueda de las estaciones de precipitacion
for i in range(len (df_p)):
    b=0
    cod=df_p["CodigoEstacion"][i]

    for j in range(len(catalogo)):
        if catalogo["Codigo"][j] ==cod :
            # cuando encuentra la estacion en el catalogo reemplaza el 0.0 por 1
            catalogo["p"][j]=1
            b=1
            
    if b==0:
        # Si no la encuentra en el catalogo, la guarda para analizarla despues
        print(cod, "de la tabla precipitacion no se econtró en el catalogo")
        malos_p.append(cod)
 
# Busqueda de las estaciones de temperatura           
for i in range(len(df_t)):
    b=0
    cod=df_t["CodigoEstacion"][i]
    
    for j in range(len(catalogo)):
        if catalogo["Codigo"][j] ==cod :
            # cuando encuentra la estacion en el catalogo reemplaza el 0.0 por 1
            catalogo["t"][j]=1
            b=1
            
    if b==0:
        # Si no la encuentra en el catalogo, la guarda para analizarla despues
        print(cod, "de la tabla temperatura no se econtró en el catalogo")
        malos_t.append(cod)
   
# Convierte a dataframe y guarda en csv
malos_p = pd.DataFrame(malos_p)
malos_t = pd.DataFrame(malos_t)

catalogo.to_csv(r'/home/marcelae/Desktop/FACOM/Estaciones/existencia_estaciones_catalogo.csv', 
                index=None, sep=';')

malos_p.to_csv(r'/home/marcelae/Desktop/FACOM/Estaciones/noexisten_precipitacion.csv',
                 header=None, index=None, sep=';')

malos_t.to_csv(r'/home/marcelae/Desktop/FACOM/Estaciones/noexisten_temperatura.csv',
                 header=None, index=None, sep=';')

#----------------------------------------#--------------------------------#
#2 de mayo de 2022  - Luisa
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

# ------------------------------------------------------------------#-----------------------------------------------------
#mayo 5 de 2022 marcela 
#estaciones de prueba

#Lucy2
engt = 'sqlite:////home/marcela/Desktop/FACOM/db/temperatura_2.db'
engp = 'sqlite:////home/marcela/Desktop/FACOM/db/precipitacion_2.db'

# Estaciones fuera de servicio y en pruebas
my_query='''
SELECT DISTINCT CodigoEstacion, NombreEstacion, Departamento, Municipio
FROM precipitacion
WHERE NombreEstacion
LIKE "%pruebas%"
'''

df_t = SQL_PD(my_query,engt)
df_p = SQL_PD(my_query,engp)


#---------------------------#------------------------------------#

#Mayo 5  de 2022 luisa

#Esta función permite analizar un data frame con tres columnas (FechaObservación, 
# CodigoEstacion y ValorObservado) para la variable de precipitación
#direccion1 = dirección donde se va a guardar los png de los CMA
#direccion2 = Dirección donde se va a guardar los png de los CMD
#direccion3 = Dirección donde se va a guardar el archivo de salida final


def col3_analisis_p(df_v,direccion1,direccion2,direccion3):
    df_v["fecha"]=pd.to_datetime(df_v["FechaObservacion"])
    cod=df_v.CodigoEstacion.unique()
    n_1=len(cod)
    titulos=["CodigoEstacion","FechaInicial","FechaFinal","dxI","dxF","tamaño","Maximo"
             ,"Minimo","Promedio","DesviacionEstandar","Mediana"]
    vector=[titulos]
    exep=["CodigoEstacion"]
    for i in tqdm(range(n_1)):
        cod_q=cod[i]
        df=df_v[df_v.CodigoEstacion==cod_q]
        #df=pd.DataFrame(df)
        df = df.reset_index()
        print("Se guarda la estacion", cod_q)
    
        try:
            
            #longitud de filas
            n=len(df)
            #longitud de columnas
            shape = df.shape
            #Obtener el nombre de las columnas
            #columns_names = variables_df.columns.values
            #Paso de tiempo
            if n <=1 :
                print("SOLO TIENE UNA FECHA REGISTRADA")
                dxi=None
                dxf=None
                
            if n > 1:
                if df["fecha"][0] != df["fecha"][1]:
                    dxi=(df["fecha"][1]-df["fecha"][0]).seconds/60    
                else:
                    dxi=None
                    
                if df["fecha"][n-1] != df["fecha"][n-2]:
                    dxf=(df["fecha"][n-1]-df["fecha"][n-2]).seconds/60    
                else:
                    dxf=None
                
            print("")
            print("#---------------------------#")
            print("Estación",cod_q)
            print("")
            print("INFORMACIÓN INICIAL")
            print("")
            print("1. La fecha inicial =",df["fecha"][0] )
            print("2. La fecha final =",df["fecha"][n-1] )
            print("3. Muestreo valores iniciales =",dxi, "min")
            print("4. Muestreo valores finales =",dxf, "min")
            print("5. La cantidad de filas y columnas =",shape )
            #print("6. El nombre de las columnas es=",columns_names)
            print("7. Las primeras filas son= ")
            print(df.head())
            print("8. Las últimas filas= ")
            print(df.tail())
            print("")
            #CALCULOS
            #max, min, promedio
            #Valor máximo
            maxi=round(df.ValorObservado.max(),3)
            mini=round(df.ValorObservado.min(),3)
            media=round(df.ValorObservado.mean(),3)
            desviacion=round(np.std(df.ValorObservado),3)
            mediana=round(np.median(df.ValorObservado),3)
    
            print("")
            print("ESTADISTICOS")
            print("")
            print("17. Valor máximo= ", maxi)
            print("18. Valor mínimo= ", mini)
            print("19. Valor medio= ", media)
            print("20. Desviación estandar", desviacion)
            print("21. Mediana= ", mediana)
            
            df["year"]=pd.to_datetime(df['fecha']).dt.year 
            df["month"]=pd.to_datetime(df['fecha']).dt.month
            df["day"]=pd.to_datetime(df['fecha']).dt.day  
            df["hour"]=pd.to_datetime(df['fecha']).dt.hour
            month=list(df["month"].unique())
            month.sort() 
            hour=list(df["hour"].unique())
            hour.sort()
            
            print("")
            print("GRAFICOS")
            print("")
            
            #ciclo diurno
            H=[]
            for j in tqdm(hour):
                hora=df[df.hour==j]
                mean_h=hora.ValorObservado.mean(skipna=True)
                H.append(mean_h)
                #print("Ingresa")
            #grafico
            plt.figure(figsize=(10,5))
            plt.title("Ciclo Medio Diurno \n Estación " +str(cod_q) 
                      , size=20, loc='center', pad=8)
            plt.plot(hour,H,color="slateblue",label=("Precipitacion -",str(cod_q)))
            plt.xlabel("Tiempo (horas)")
            plt.ylabel("Precipitacion [mm]")
            plt.grid()
            plt.legend()
            plt.minorticks_on()
            plt.savefig(direccion2+'CMD'  + '_IDEAM-' + str(cod_q) + '_' + str(i) + '.png') 
            
            
            #ciclo medio anual
            
            if len(month) != 12:
                lista=[1,2,3,4,5,6,7,8,9,10,11,12]
                dif_1=set(lista).difference(set(month))
                dif_2=set(month).difference(set(lista))
                dif=list(dif_1.union(dif_2))
                len_dif=len(dif)
                for k in range(len(dif)):
                    month.append(dif[k])
                month.sort()
                
            Ma_mes=[]
            for j in tqdm(month):
                mes=df[df.month==j]
                mean_m=mes.ValorObservado.mean(skipna=True)
                Ma_mes.append(mean_m)
                #print("Ingresa el promed|io del mes",j)
            meses=np.array(["Ene","Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", 
                            "Sep","Oct", "Nov", "Dic"])
            
            plt.figure(figsize=(10,5))
            plt.title("Ciclo Anual \n Estación= " +str(cod_q) 
                      , size=20, loc='center', pad=8)
            #plt.title("Ciclo medio anual \n Estación" )
            plt.plot(meses,Ma_mes,color="indigo",label=("Precipitacion -",str(cod_q)))
            plt.legend()
            plt.xlabel("Tiempo (meses)")
            plt.ylabel("Precipitación [mm]")
            plt.grid()
            plt.minorticks_on()
            plt.savefig(direccion1+'CMA'  + '_IDEAM-' + str(cod_q) + '_' + str(i) + '.png')  
            
            #se guarda el archivo
    
            c=[cod_q,df["fecha"][0],df["fecha"][n-1],dxi,dxf,shape,maxi,mini,media,
               desviacion,mediana]
            vector.append(c)
            #print(vector)
            print("termina" ,i, "-",cod_q)
            print("#---------------------------#")
        except:
            print("La estación", cod_q, "No pudo ser ingresada")
            exep.append(cod_q)
            
    print("se termina de analizar la base de datos")
    df_final=pd.DataFrame(vector)
    df_final.to_csv(direccion3,sep=";")
    return(df_final,exep)    

def col3_analisis_t(df_v,direccion1,direccion2,direccion3):
    df_v["fecha"]=pd.to_datetime(df_v["FechaObservacion"])
    cod=df_v.CodigoEstacion.unique()
    n_1=len(cod)
    titulos=["CodigoEstacion","FechaInicial","FechaFinal","dxI","dxF","Tamaño","Maximo"
             ,"Minimo","Promedio","DesviacionEstandar","Mediana"]
    vector=[titulos]
    exep=["CodigoEstacion"]
    for i in tqdm(range(n_1)):
        cod_q=cod[i]
        df=df_v[df_v.CodigoEstacion==cod_q]
        #df=pd.DataFrame(df)
        df = df.reset_index()
        print("Se guarda la estacion", cod_q)
    
        try:
            
            #longitud de filas
            n=len(df)
            #longitud de columnas
            shape = df.shape
            #Obtener el nombre de las columnas
            #columns_names = variables_df.columns.values
            #Paso de tiempo
            if n <=1 :
                print("SOLO TIENE UNA FECHA REGISTRADA")
                dxi=None
                dxf=None
                
            if n > 1:
                if df["fecha"][0] != df["fecha"][1]:
                    dxi=(df["fecha"][1]-df["fecha"][0]).seconds/60    
                else:
                    dxi=None
                    
                if df["fecha"][n-1] != df["fecha"][n-2]:
                    dxf=(df["fecha"][n-1]-df["fecha"][n-2]).seconds/60    
                else:
                    dxf=None
                
            print("")
            print("#---------------------------#")
            print("Estación",cod_q)
            print("")
            print("INFORMACIÓN INICIAL")
            print("")
            print("1. La fecha inicial =",df["fecha"][0] )
            print("2. La fecha final =",df["fecha"][n-1] )
            print("3. Muestreo valores iniciales =",dxi, "min")
            print("4. Muestreo valores finales =",dxf, "min")
            print("5. La cantidad de filas y columnas =",shape )
            #print("6. El nombre de las columnas es=",columns_names)
            print("7. Las primeras filas son= ")
            print(df.head())
            print("8. Las últimas filas= ")
            print(df.tail())
            print("")
            #CALCULOS
            #max, min, promedio
            #Valor máximo
            maxi=round(df.ValorObservado.max(),3)
            mini=round(df.ValorObservado.min(),3)
            media=round(df.ValorObservado.mean(),3)
            desviacion=round(np.std(df.ValorObservado),3)
            mediana=round(np.median(df.ValorObservado),3)
    
            print("")
            print("ESTADISTICOS")
            print("")
            print("17. Valor máximo= ", maxi)
            print("18. Valor mínimo= ", mini)
            print("19. Valor medio= ", media)
            print("20. Desviación estandar", desviacion)
            print("21. Mediana= ", mediana)
            
            df["year"]=pd.to_datetime(df['fecha']).dt.year 
            df["month"]=pd.to_datetime(df['fecha']).dt.month
            df["day"]=pd.to_datetime(df['fecha']).dt.day  
            df["hour"]=pd.to_datetime(df['fecha']).dt.hour
            month=list(df["month"].unique())
            month.sort() 
            hour=list(df["hour"].unique())
            hour.sort()
            
            print("")
            print("GRAFICOS")
            print("")
            
            #ciclo diurno
            H=[]
            for j in tqdm(hour):
                hora=df[df.hour==j]
                mean_h=hora.ValorObservado.mean(skipna=True)
                H.append(mean_h)
                #print("Ingresa")
            #grafico
            plt.figure(figsize=(10,5))
            plt.title("Ciclo Medio Diurno \n Estación " +str(cod_q) 
                      , size=20, loc='center', pad=8)
            plt.plot(hour,H,color="palevioletred",label=("Temperatura -",str(cod_q)))
            plt.xlabel("Tiempo (horas)")
            plt.ylabel("Temperatura [°C]")
            plt.grid()
            plt.legend()
            plt.minorticks_on()
            plt.savefig(direccion2+'CMD'  + '_IDEAM-' + str(cod_q) + '_' + str(i) + '.png') 
            
            
            #ciclo medio anual
            
            if len(month) != 12:
                lista=[1,2,3,4,5,6,7,8,9,10,11,12]
                dif_1=set(lista).difference(set(month))
                dif_2=set(month).difference(set(lista))
                dif=list(dif_1.union(dif_2))
                len_dif=len(dif)
                for k in range(len(dif)):
                    month.append(dif[k])
                month.sort()
                
            Ma_mes=[]
            for j in tqdm(month):
                mes=df[df.month==j]
                mean_m=mes.ValorObservado.mean(skipna=True)
                Ma_mes.append(mean_m)
                #print("Ingresa el promed|io del mes",j)
            meses=np.array(["Ene","Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", 
                            "Sep","Oct", "Nov", "Dic"])
            
            plt.figure(figsize=(10,5))
            plt.title("Ciclo Anual 2018\n Estación= " +str(cod_q) 
                      , size=20, loc='center', pad=8)
            #plt.title("Ciclo medio anual \n Estación" )
            plt.plot(meses,Ma_mes,color="crimson",label=("Temperatura -",str(cod_q)))
            plt.legend()
            plt.xlabel("Tiempo (meses)")
            plt.ylabel("Temperatura [°C]")
            plt.grid()
            plt.minorticks_on()
            plt.savefig(direccion1+'CMA'  + '_IDEAM-' + str(cod_q) + '_' + str(i) + '.png')  
            
            #se guarda el archivo
    
            c=[cod_q,df["fecha"][0],df["fecha"][n-1],dxi,dxf,shape,maxi,mini,media,
               desviacion,mediana]
            vector.append(c)
            #print(vector)
            print("termina" ,i, "-",cod_q)
            print("#---------------------------#")
        except:
            print("La estación", cod_q, "No pudo ser ingresada")
            exep.append(cod_q)
            
    print("se termina de analizar la base de datos")
    df_final=pd.DataFrame(vector)
    df_final.to_csv(direccion3,sep=";")
    return(df_final,exep)

#precipitacion
#lucy
dfp=pd.read_csv(r"/home/marcelae/Desktop/FACOM/aeropuertos/entrega/precipitacion_2018_AeropuertosPD.csv")
#luisa
#dfp=pd.read_csv(r"/media/luisa/Datos/FACOM/gits/FACOM/aeropuertos/entrega/precipitacion_2018_AeropuertosPD.csv")
dfp.columns=["FechaObservacion", "CodigoEstacion", "ValorObservado"]
direccion1p="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/png/anual_p/"
direccion2p="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/png/diurno_p/"
direccion3p="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/aeropuertos_p_2018.csv"
p,exep_p=col3_analisis_p(dfp,direccion1p,direccion2p,direccion3p)

#temperatura
dft=pd.read_csv(r"/home/marcelae/Desktop/FACOM/aeropuertos/entrega/temperatura_2018_AeropuertosPD.csv",sep=";")
dft.columns=["FechaObservacion", "CodigoEstacion", "ValorObservado"]

direccion1t="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/png/anual_t/"
direccion2t="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/png/diurno_t/"
direccion3t="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/aeropuertos_t_2018.csv"
t,exep_t=col3_analisis_t(dft,direccion1t,direccion2t,direccion3t)

#################################################3


#d_A_entrada= dirección del archivo de entrada para comparar,
#usecols_AE= columnas de referencia del archivo de entrada (lon y lat en ese orden)

#hallar las coordenadas cercanas a unas de referencia, en una base de datos, en un área cuadrada
def rangocuadrado_coordenadas(d_A_entrada,usecols_AE,variacion_lat,variacion_lon
                              ,direccion1,direccion2,direccion3,eng,tabla):
    #se ingresa la información de entrada
    datos = pd.read_csv( d_A_entrada, usecols=usecols_AE)
    #se realiza el cambio en los nombres de las columnas para realizar un append
    datos.columns = ["lon","lat"]
    
    #Se crean los vectores para guardar
    
    #archivo con estaciones no encontradas
    titulos1 = ["lon","lat"]
    vector1 = [titulos1]
    #archivo con estaciones encontradas
    titulos = ["i","CodigoEstacion","NombreEstacion","Departamento","Municipio",
             "ZonaHidrografica","Latitud","Longitud"]
    vector = [titulos]
    #cuando encuentra más de 1 estación
    titulos2 = ["i","CodigoEstacion","NombreEstacion","Departamento","Municipio",
              "ZonaHidrografica","Latitud","Longitud"]
    vector2 = [titulos2]
    
    for i in  tqdm(range(len(datos))):
        my_query3='''
        SELECT DISTINCT CodigoEstacion,NombreEstacion,Departamento,Municipio,ZonaHidrografica,Latitud,Longitud
        FROM {}
        WHERE (Latitud <= {} AND Latitud >= {}) AND (Longitud <= {} AND Longitud >= {})
        '''.format(tabla,datos["lat"][i]+variacion_lat , datos["lat"][i]-variacion_lat ,datos["lon"][i]+variacion_lon,datos["lon"][i]-variacion_lon)
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
    print(" el archivo final tiene ", len(vector), " filas unicas")
    
    #se guarda la información
    #guardar el archivo csv
    df=pd.DataFrame(vector)
    df_noencontrados=pd.DataFrame(vector1)
    df_varios=pd.DataFrame(vector2)
    
    df.to_csv(direccion1,header=None, index=None, sep=';')
    df_noencontrados.to_csv(direccion2,header=None, index=None, sep=';')
    df_varios.to_csv(direccion3,header=None, index=None, sep=';')
    print("se guardan los archivos para ")

#direccion1 = archivo de salida de los coordenadas que solo tienen una coincidencia
#direccion2 = archivo de salida de los coordenadas que no tienen coincidencia
#direccion3 = archivo de salida de los coordenadas que tienen varias coincidencia  
        
        


#daniel
d_A_entradad="/home/marcelae/Desktop/FACOM/aeropuertos/airport_coord.csv"
usecols_AEd=[1,2]
variacion_latd=(0.09/2)
variacion_lond=(0.17921/2) 
direccion1d="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/analisis_por_lat_lon/C1.csv"
direccion2d="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/analisis_por_lat_lon/sinC.csv"
direccion3d="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/analisis_por_lat_lon/variasC.csv" 


#julio
d_A_entradaj="/home/marcelae/Desktop/FACOM/aeropuertos/Aeropuertos.csv"
usecols_AEj=[2,3]
variacion_latj=0.009
variacion_lonj=0.017921  

direccion1j="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/julio/analisis_por_lat_lon/C1.csv"
direccion2j="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/julio/analisis_por_lat_lon/sinC.csv"
direccion3j="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/julio/analisis_por_lat_lon/variasC.csv"
  

engt = "sqlite:////home/marcelae/Desktop/FACOM/db/temperatura_2.db"
engp = "sqlite:////home/marcelae/Desktop/FACOM/db/precipitacion_2.db"
tablap="precipitacion"
tablat="temperatura"


#daniel
rangocuadrado_coordenadas(d_A_entradad,usecols_AEd,variacion_latd,variacion_lond,
                          direccion1d,direccion2d,direccion3d,engt,tablat)

#julio
rangocuadrado_coordenadas(d_A_entradaj,usecols_AEj,variacion_latj,variacion_lonj,
                          direccion1j,direccion2j,direccion3j,engt,tablat)
#-------------------------------------------#-----------------------------------#
#mayo 9 de 2022 pruebas con el profe Esteban


my_query='''
SELECT CodigoEstacion,FechaObservacion,Departamento
FROM precipitacion
WHERE Departamento = "antioquia"
'''
v1 = SQL_PD(my_query,engp)

cod=v1.CodigoEstacion.unique()
v1["FechaObservacion"]=pd.to_datetime(v1["FechaObservacion"],format='%m/%d/%Y %I:%M:%S %p')

for i in cod:
    ok = v1.CodigoEstacion==i
    print((v1["Departamento"][ok]).unique(),i,
          (v1["FechaObservacion"][ok]).max(),
          (v1["FechaObservacion"][ok]).min())
v1.min()

print(len(v1[v1.CodigoEstacion==47017070]))
# -----------------------------------------------------------------------
# junio 6 de 2022 
import pandas as pd
import  numpy as np
from datetime import datetime
from tqdm import tqdm              # libreria para saber el tiempo de ejecución
from sqlalchemy import create_engine
import os
import math
import re
import matplotlib.pyplot as plt #Para graficar

eng = 'sqlite:////home/marcelae/Desktop/FACOM/2_db/presion.db'

def my_query_distinct(columnas,tabla,eng):
    my_query='''
    SELECT DISTINCT {} 
    FROM {}
    '''.format(columnas,tabla)
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


def my_query_distinct_where(columnas,tabla,eng,where,cod):
    my_query='''
    SELECT DISTINCT {} 
    FROM {}
    WHERE ({}={})
    '''.format(columnas,tabla,where,cod)
    df = SQL_PD(my_query,eng)
    return df

def analisis_variable(tabla, eng,direccion2):
    #creación de vectores
    titulos=["Codigo Estacion","Nombre de estacion","Municipio","Departamento", "Zona Hidrográfica","Latitud"
             ,"Longitud","Fecha Inicial","Fecha Final","Muestreo valores iniciales","Muestreo valores finales","Numerofilas y columnas",
             "Máximo","Mínimo","Promedio","Desviación Estándar","Mediana"]
    vector=[titulos]
    exep=["codigos"]
    
    #encontrar los codigos de la base de datos ingresada
    columnas="CodigoEstacion"
    datos=my_query_distinct(columnas,tabla,eng)
    for i in tqdm(range(len(datos))):
    #try:
        cod = datos["CodigoEstacion"][i]
        #cod=21201580
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
        #Paso de tiempo
        if n <=1 :
            print("SOLO TIENE UNA FECHA REGISTRADA")
            dxi=None
            dxf=None
            
        if n > 1:
            if variables_df["fecha"][0] != variables_df["fecha"][1]:
                dxi=(variables_df["fecha"][1]-variables_df["fecha"][0]).seconds/60    
            else:
                dxi=None
                
            if variables_df["fecha"][n-1] != variables_df["fecha"][n-2]:
                dxf=(variables_df["fecha"][n-1]-variables_df["fecha"][n-2]).seconds/60    
            else:
                dxf=None
        
        print("")
        print("#---------------------------#")
        print("Estación",cod)
        print("")
        print("INFORMACIÓN INICIAL")
        print("")
        print("1. La fecha inicial =",variables_df["fecha"][0] )
        print("2. La fecha final =",variables_df["fecha"][n-1] )
        print("3. Muestreo valores iniciales =",dxi, "min")
        print("4. Muestreo valores finales =",dxf, "min")
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
        
        c=[cod,ne,mu,dep,zh,lat,lon,variables_df["fecha"][0],variables_df["fecha"][n-1],
           dxi,dxf,shape,maxi,mini,media,desviacion,mediana]
        
        vector.append(c)
        #print(vector)
        print("termina" ,i, "-",cod)
        print("#---------------------------#")
    
    #except:
        #print("La estación", cod, "No pudo ser ingresada")
        exep.append(cod)
        
    print("se termina de analizar la base de datos")
    df_final=pd.DataFrame(vector)
    df_final.to_csv(direccion2,sep=";")
    return(df_final,exep)
    
analisis_variable('presion',eng,'/home/marcelae/Desktop/FACOM/1_Proyectos/2_Estaciones/CSV/presion_informacion.csv')
