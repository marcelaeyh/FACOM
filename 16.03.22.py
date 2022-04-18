# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 16:18:36 2022

@author: Luisa

Apartir del archivo original de csv se extrae la información para
"""

#------------------------------------------------------------------------------
#1. IMPORTAR LIBRERIAS
import pandas as pd
import  numpy as np
from datetime import datetime
#-----------------------------------------------------------------------------
#2. LECTURAS DE DATOS
m="/home/luisab/Documents/FACOM/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv" 
n="/home/luisab/Documents/FACOM/Precipitaci_n.csv"

#-----------------------------------------------------------------------------
#3. FUNCIONES
#3.1 fUNCIÓN PARA ENCONTRAR LOS TIPO DE DATOS QUE HAY EN UN VECTOR
def type_vector(n,address):
    name=[]
    for i in range(n+1):
        v=0
        v=pd.read_csv(address,usecols=[i])
        print("* Se lee el arcivo en la columna",i)
        df=pd.DataFrame(v)
        df.columns=["A"]
        print("    Se cambia el nombre de la columna a A",i)
        name.append(str(df["A"].dtype))
        #print("  El tipo de variable en la columna ",i, "es:  ",name[i])
    return(name)

#3.2 GUARDAR UNA COLUMNA EN UNA VARIABLE
#se cambio el nombre de la función, de ordenar_columna a columna.
def columna(ubicacion,address1):
    name=[]
    v=0
    v=pd.read_csv(address1,usecols=[ubicacion])
    print("La información guardada ",ubicacion, " lista!")
print("Se cargaron las librerias y las funciones")    
    
#NOTA: CORRER INICIALMENTE DESDE ACÁ,

#------------------------------------------------------------------------------
#EJERCICIO PARA ENTENDER CÓMO MANEJAR DATOS MUY EXTENSOS

#Link:https://towardsai.net/p/data-science/efficient-pandas-using-chunksize-for-large-data-sets-c66bf3037f93

#Ejemplo 1
# x a continuación hay una lista. Que es un objeto iterable.
#x = [1, 2, 3, 'hola', 5, 7]
# pasar x al método iter() lo convierte en un iterador.
#y = iter(x)
# Comprobando tipo(y)
#print(type(y))

#Ejemplo 2
#m1=pd.read_csv(m,usecols=[2])
#Se cambia el nombre de la columna por "fecha"
#m1.columns=["fecha"]
#Se convierte en "datatime" la columna fecha.
#m1['fecha']= pd.to_datetime(m1['fecha'])
# Pasemos el marco de datos df, al método iter()                             
#m2=iter(m1)
#print(type(m2))

#Ejemplo 3
#for i in range(6): print(next(y))
# Se muestra un error si se llama a next después de que todos
# los elementos se hayan impreso desde un objeto iterador

#Verifiquemos el consumo de memoria 
#ratings_memory = m1.memory_usage().sum()
#print('La memoria actual total es-', ratings_memory,'Bytes.')
#------------------------------------------------------------------------------

print(" Comienza el analisis del archivo HD")

#HIDROMETROROLOGIA

#------------------------------------------------------------------------------
#EXTRAER EL TIPO DE DATO QUE HAY EN CADA COLUMNA
HD_type=type_vector(10,m)
print(HD_type)   
np.savetxt("/home/luisab/Documents/FACOM/documents/type_columns_HD.csv", HD_type,fmt='%s')   
#------------------------------------------------------------------------------
#PRIMERA Y ULTIMA FECHA, ADEMÁS INTERVALO
FECHA_HD=pd.read_csv(m,usecols=[2])
#Se cambia el nombre de la columna por "fecha"
FECHA_HD.columns=["fecha"]
# Obtengamos una lista de las fechas que contiene
FECHA_HD_unique = list(FECHA_HD['fecha'].unique())
# Ordenemos, como s un str no lo organizo 
FECHA_HD_unique = sorted(FECHA_HD_unique, reverse=True)
# Guardamos el archivo
#np.savetxt("/home/luisa/Escritorio/Semestre_Actual/FACOM/fechas.csv", rate_keys,fmt='%s')
#Visualizar los primeros y ultimos datos para la fecha
FECHA_HD_unique_df= pd.DataFrame(FECHA_HD_unique)
FECHA_HD_unique_df.columns=["fecha"]
FECHA_HD_unique_df['fecha']= pd.to_datetime(FECHA_HD_unique_df['fecha'])
FECHA_HD_unique_df.sort_values(by='fecha', inplace=True)
FECHA_HD_unique_df.head(10)
FECHA_HD_unique_df.tail(10)
# Guardamos el archivo
np.savetxt("fechas_HD.csv", 
           FECHA_HD_unique_df,fmt='%s')

#------------------------------------------------------------------------------
#INFORMACIÓN DE VARIABLES 

#1. CÓDIGO ESTACIÓN
CDE_HD=pd.read_csv(m,usecols=[0])
CDE_HD_memoria = CDE_HD.memory_usage().sum()
print('La memoria total actual de la variable',"CodigoEstacion",'es-', CDE_HD_memoria,'Bytes.')
CDE_HD.columns=["CodigoEstacion"]
CDE_HD_unique=list(CDE_HD['CodigoEstacion'].unique())
CDE_HD_unique= sorted(CDE_HD_unique)
np.savetxt("/home/luisab/Documents/FACOM/documents/CodigoEstacion_HD.csv", 
           CDE_HD_unique,fmt='%s')

#2. CÓDIGO SENSOR
CDS_HD=pd.read_csv(m,usecols=[1])
CDS_HD_memoria = CDS_HD.memory_usage().sum()
print('La memoria total actual de la variable',"Codigo de Sensor",'es-', 
      CDS_HD_memoria,'Bytes.')
CDS_HD.columns=["CodigoSensor"]
CDS_HD_unique=list(CDS_HD['CodigoSensor'].unique())
CD_HDS_unique= sorted(CDS_HD_unique)
np.savetxt("/home/luisab/Documents/FACOM/documents/CodigoSensor_HD.csv", 
           CDS_HD_unique,fmt='%s')

#3. NOMBRE ESTACIÓN
NE_HD=pd.read_csv(m,usecols=[4])
NE_HD_memoria = NE_HD.memory_usage().sum()
print('La memoria total actual de la variable',"Nombre de Estaciones",'es-', 
      NE_HD_memoria,'Bytes.')
NE_HD.columns=["NombreEstacion"]
NE_HD_unique=list(NE_HD['NombreEstacion'].unique())
NE_HD_unique= sorted(NE_HD_unique)
np.savetxt("/home/luisab/Documents/FACOM/documents/NombresEstaciones_HD.csv", 
           NE_HD_unique,fmt='%s')

#4. DEPARTAMENTOS
Departamentos_HD=pd.read_csv(m,usecols=[5])
Departamentos_HD_memoria = Departamentos_HD.memory_usage().sum()
print('La memoria total actual de la variable',"Departamentos",'es-', 
      Departamentos_HD_memoria,'Bytes.')
Departamentos_HD.columns=["Departamentos"]
Departamentos_HD_unique=list(Departamentos_HD['Departamentos'].unique())
Departamentos_HD_unique= sorted(Departamentos_HD_unique)
np.savetxt("/home/luisab/Documents/FACOM/documents/Departamentos_HD.csv", 
           Departamentos_HD_unique,fmt='%s')

#5. MUNICIPIOS
Municipios_HD=pd.read_csv(m,usecols=[6])
Municipios_HD_memoria = Municipios_HD.memory_usage().sum()
print('La memoria total actual de la variable',"Municipios",'es-', 
      Municipios_HD_memoria,'Bytes.')
Municipios_HD.columns=["Municipios"]
Municipios_HD_unique=list(Municipios_HD['Municipios'].unique())
Municipios_HD_unique= sorted(Municipios_HD_unique)
np.savetxt("/home/luisab/Documents/FACOM/documents/Municipios_HD.csv", 
           Municipios_HD_unique,fmt='%s')
print("Fin del analisis del archivo HD")
#------------------------------------------------------------------------------
#PRECIPITACIÓN
print("Inicio del analisis del archivo P")


#------------------------------------------------------------------------------

P_type=type_vector(10,n)
print(P_type)   
np.savetxt("/home/luisab/Documents/FACOM/documents/type_columns_HD.csv", P_type,fmt='%s') 

#PRIMERA Y ULTIMA FECHA, ADEMÁS INTERVALO
FECHA_P=pd.read_csv(n,usecols=[2])
FECHA_P.tail(20)
#Se cambia el nombre de la columna por "fecha"
FECHA_P.columns=["fecha"]

# Obtengamos una lista de las fechas que contiene
FECHA_P_unique = list(FECHA_P['fecha'].unique())
np.savetxt("/home/luisab/Documents/FACOM/documents/fechas_P_sinordenar.csv", 
           FECHA_P_unique,fmt='%s')
# Ordenemos, como s un str no lo organizo 
#FECHA_unique = sorted(FECHA_unique, reverse=True)
# Guardamos el archivo
#np.savetxt("/home/luisa/Escritorio/Semestre_Actual/FACOM/fechas.csv", rate_keys,fmt='%s')
#Visualizar los primeros y ultimos datos para la fecha
FECHA_P_unique_df= pd.DataFrame(FECHA_P_unique)
FECHA_P_unique_df.columns=["fecha"]
FECHA_P_unique_df['fecha']= pd.to_datetime(FECHA_P_unique_df['fecha'])
FECHA_P_unique_df.sort_values(by='fecha', inplace=True)
FECHA_P_unique_df.head(10)
FECHA_P_unique_df.tail(10)
# Guardamos el archivo
np.savetxt("/home/luisab/Documents/FACOM/documents/fechas_P.csv", 
           FECHA_P_unique_df,fmt='%s')
#------------------------------------------------------------------------------
#INFORMACIÓN DE VARIABLES 

#1. CÓDIGO ESTACIÓN
CDE_P=pd.read_csv(n,usecols=[0])
CDE_P_memoria = CDE_P.memory_usage().sum()
print('La memoria total actual de la variable',"CodigoEstacion",'es-', CDE_P_memoria,'Bytes.')
CDE_P.columns=["CodigoEstacion"]
CDE_P_unique=list(CDE_P['CodigoEstacion'].unique())
CDE_P_unique= sorted(CDE_P_unique)
np.savetxt("/home/luisab/Documents/FACOM/documents/CodigoEstacion_P.csv", 
           CDE_P_unique,fmt='%s')

#2. CÓDIGO SENSOR
CDS_P=pd.read_csv(n,usecols=[1])
CDS_P_memoria = CDS_P.memory_usage().sum()
print('La memoria total actual de la variable',"Codigo de Sensor",'es-', 
      CDS_P_memoria,'Bytes.')
CDS_P.columns=["CodigoSensor"]
CDS_P_unique=list(CDS_P['CodigoSensor'].unique())
CDS_P_unique= sorted(CDS_P_unique)
np.savetxt("/home/luisab/Documents/FACOM/documents/CodigoSensor_P.csv", 
           CDS_P_unique,fmt='%s')

#3. NOMBRE ESTACIÓN
NE_P=pd.read_csv(n,usecols=[4])
NE_P_memoria = NE_P.memory_usage().sum()
print('La memoria total actual de la variable',"Nombre de Estaciones",'es-', NE_P_memoria,'Bytes.')
NE_P.columns=["NombreEstacion"]
NE_P_unique=list(NE_P['NombreEstacion'].unique())
NE_P_unique= sorted(NE_P_unique)
np.savetxt("/home/luisab/Documents/FACOM/documents/NombresEstaciones_P.csv", 
           NE_P_unique,fmt='%s')

#4. DEPARTAMENTOS
Departamentos_P=pd.read_csv(n,usecols=[5])
Departamentos_P_memoria = Departamentos_P.memory_usage().sum()
print('La memoria total actual de la variable',"Departamentos",'es-', 
      Departamentos_P_memoria,'Bytes.')
Departamentos_P.columns=["Departamentos"]
Departamentos_P_unique=list(Departamentos_P['Departamentos'].unique())
Departamentos_P_unique= sorted(Departamentos_P_unique)
np.savetxt("/home/luisab/Documents/FACOM/documents/Departamentos_P.csv", 
           Departamentos_P_unique,fmt='%s')

#5. MUNICIPIOS
Municipios_P=pd.read_csv(n,usecols=[6])
Municipios_P_memoria = Municipios_P.memory_usage().sum()
print('La memoria total actual de la variable',"Municipios",'es-', 
      Municipios_P_memoria,'Bytes.')
Municipios_P.columns=["Municipios"]
Municipios_P_unique=list(Municipios_P['Municipios'].unique())
Municipios_P_unique= sorted(Municipios_P_unique)
np.savetxt("/home/luisab/Documents/FACOM/documents/Municipios_P.csv", 
           Municipios_P_unique,fmt='%s')

print("Fin del analisis del archivo P")
#------------------------------------------------------------------------------
#Seleccionar y filtrar por 

#------------------------------------------------------------------------------
#¿Seria bueno primero filtrar por estaciones?
#7. Revisar que todos los elementos de una columna sean del mismo tipo:

from tqdm import tqdm # libreria para saber el tiempo de ejecución

# address = Ubicación de la base de datos
# column = Posición de la columna a buscar 

#Como se revisan los primeros datos, la suposición es que los primeros datos de
#cada columna son correctos.
def buscar(ubicacion, address1):
    column=columna(ubicacion,address1)
    
    # Compara dato a dato que todos tengan en formato correcto
    column.columns=["A"]
    for i in tqdm(range(len(column))):
        tipo = type(column["A"][0])
        if type(column["A"][i]) != tipo:
            print("Este elemento no es ", tipo, column["A"][i],"Está en la posición", i)
            
            

m5=buscar(1,m)





