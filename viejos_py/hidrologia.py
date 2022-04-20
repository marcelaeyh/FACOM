# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 16:18:36 2022

@author: Luisa
"""

#------------------------------------------------------------------------------
#1. IMPORTAR LIBRERIAS
import pandas as pd
import  numpy as np
from datetime import datetime
#-----------------------------------------------------------------------------
#2. LECTURAS DE DATOS
m="DHCREI.csv" 
n="P.csv"
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
        print("  Se cambia el nombre de la columna a A",i)
        name.append(str(df["A"].dtype))
        print(name)
        #print("  El tipo de variable en la columna ",i, "es:  ",name[i])
    return(name)

#3.2 GUARDAR UNA COLUMNA EN UNA VARIABLE Y GUARDAR COMO ARCHIVO TXT
#Ubicacion es una variable númerica, indica la posición que se desea guardar
#Address1, es para indicar la ubicación del archivo de entrada
#Address2, es para indicar la ubicación del archivo de salida
#name, es para indicar el nombre del archivo de salida

def ordenar_columna_guardar(ubicacion,address1,address2,nombre):
    name=[]
    v=0
    v=pd.read_csv(address1,usecols=[ubicacion])
    print("se guarda el archivo como", nombre, " en la dirección", address2)
    print("La columna guardada es",ubicacion)
    np.savetxt(address2+nombre, m1,fmt='%s')
    return(v)

#3.3 GUARDAR UNA COLUMNA EN UNA VARIABLE
#se cambio el nombre de la función, de ordenar_columna a columna.
def columna(ubicacion,address1):
    name=[]
    v=0
    v=pd.read_csv(address1,usecols=[ubicacion])
    print("La información guardada ",ubicacion, " lista!")
    
    



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



#HIDROMETROROLOGIA






#------------------------------------------------------------------------------
#EXTRAER EL TIPO DE DATO QUE HAY EN CADA COLUMNA
m1=type_vector(10,m)
print(m1)   
np.savetxt("/home/luisa/Escritorio/Semestre_Actual/FACOM/prueba.csv", m1,fmt='%s')   
#------------------------------------------------------------------------------
#PRIMERA Y ULTIMA FECHA, ADEMÁS INTERVALO
FECHA=pd.read_csv(m,usecols=[2])
#Se cambia el nombre de la columna por "fecha"
FECHA.columns=["fecha"]

# Obtengamos una lista de las fechas que contiene
FECHA_unique = list(m1['fecha'].unique())
# Ordenemos, como s un str no lo organizo 
FECHA_unique = sorted(FECHA_unique, reverse=True)
# Guardamos el archivo
#np.savetxt("/home/luisa/Escritorio/Semestre_Actual/FACOM/fechas.csv", rate_keys,fmt='%s')
#Visualizar los primeros y ultimos datos para la fecha
FECHA_unique_df= pd.DataFrame(FECHA_unique)
FECHA_unique_df.columns=["fecha"]
FECHA_unique_df['fecha']= pd.to_datetime(FECHA_unique_df['fecha'])
FECHA_unique_df.sort_values(by='fecha', inplace=True)
FECHA_unique_df.head(10)
FECHA_unique_df.tail(10)
# Guardamos el archivo
np.savetxt("/home/luisa/Escritorio/Semestre_Actual/FACOM/fechas.csv", 
           FECHA_unique_df,fmt='%s')

#------------------------------------------------------------------------------
#INFORMACIÓN DE VARIABLES 

#1. CÓDIGO ESTACIÓN
CDE=pd.read_csv(m,usecols=[0])
CDE_memoria = CDE.memory_usage().sum()
print('La memoria total actual de la variable',"CodigoEstacion",'es-', CDE_memoria,'Bytes.')
CDE.columns=["CodigoEstacion"]
CDE_unique=list(CDE['CodigoEstacion'].unique())
CDE_unique= sorted(CDE_unique)
np.savetxt("/home/luisa/Escritorio/Semestre_Actual/FACOM/CodigoEstacion.csv", 
           CDE_unique,fmt='%s')

#2. CÓDIGO SENSOR
CDS=pd.read_csv(m,usecols=[1])
CDS_memoria = CDS.memory_usage().sum()
print('La memoria total actual de la variable',"Codigo de Sensor",'es-', 
      CDS_memoria,'Bytes.')
CDS.columns=["CodigoSensor"]
CDS_unique=list(CDS['CodigoSensor'].unique())
CDS_unique= sorted(CDS_unique)
np.savetxt("/home/luisa/Escritorio/Semestre_Actual/FACOM/CodigoSensor.csv", 
           CDS_unique,fmt='%s')

#3. NOMBRE ESTACIÓN
NE=pd.read_csv(m,usecols=[4])
NE_memoria = NE.memory_usage().sum()
print('La memoria total actual de la variable',"Nombre de Estaciones",'es-', NE_memoria,'Bytes.')
NE.columns=["NombreEstacion"]
NE_unique=list(NE['NombreEstacion'].unique())
NE_unique= sorted(NE_unique)
np.savetxt("/home/luisa/Escritorio/Semestre_Actual/FACOM/NombresEstaciones.csv", 
           NE_unique,fmt='%s')

#4. DEPARTAMENTOS
Departamentos=pd.read_csv(m,usecols=[5])
Departamentos_memoria = Departamentos.memory_usage().sum()
print('La memoria total actual de la variable',"Departamentos",'es-', 
      Departamentos_memoria,'Bytes.')
Departamentos.columns=["Departamentos"]
Departamentos_unique=list(Departamentos['Departamentos'].unique())
Departamentos_unique= sorted(Departamentos_unique)
np.savetxt("/home/luisa/Escritorio/Semestre_Actual/FACOM/Departamentos.csv", 
           Departamentos_unique,fmt='%s')

#5. MUNICIPIOS
Municipios=pd.read_csv(m,usecols=[6])
Municipios_memoria = Municipios.memory_usage().sum()
print('La memoria total actual de la variable',"Municipios",'es-', 
      Municipios_memoria,'Bytes.')
Municipios.columns=["Municipios"]
Municipios_unique=list(Municipios['Municipios'].unique())
Municipios_unique= sorted(Municipios_unique)
np.savetxt("/home/luisa/Escritorio/Semestre_Actual/FACOM/Municipios.csv", 
           Municipios_unique,fmt='%s')

#------------------------------------------------------------------------------
#PRECIPITACIÓN



#------------------------------------------------------------------------------

#PRIMERA Y ULTIMA FECHA, ADEMÁS INTERVALO
FECHA=pd.read_csv(n,usecols=[2])
FECHA.tail(20)
#Se cambia el nombre de la columna por "fecha"
FECHA.columns=["fecha"]

# Obtengamos una lista de las fechas que contiene
FECHA_unique = list(FECHA['fecha'].unique())
np.savetxt("/home/luisa/Escritorio/Semestre_Actual/FACOM/fechas_P_sinordenar.csv", 
           FECHA_unique,fmt='%s')
# Ordenemos, como s un str no lo organizo 
#FECHA_unique = sorted(FECHA_unique, reverse=True)
# Guardamos el archivo
#np.savetxt("/home/luisa/Escritorio/Semestre_Actual/FACOM/fechas.csv", rate_keys,fmt='%s')
#Visualizar los primeros y ultimos datos para la fecha
FECHA_unique_df= pd.DataFrame(FECHA_unique)
FECHA_unique_df.columns=["fecha"]
FECHA_unique_df['fecha']= pd.to_datetime(FECHA_unique_df['fecha'])
FECHA_unique_df.sort_values(by='fecha', inplace=True)
FECHA_unique_df.head(10)
FECHA_unique_df.tail(10)
# Guardamos el archivo
np.savetxt("/home/luisa/Escritorio/Semestre_Actual/FACOM/fechas.csv", 
           FECHA_unique_df,fmt='%s')

