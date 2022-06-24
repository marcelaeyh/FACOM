# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.

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

"""
from sqlalchemy import create_engine
import pandas as pd
from tqdm import tqdm  
import numpy as np
import re
from unicodedata import normalize

#-------------------------#
def SQL_PD(table_or_sql,conn):
       generator_object = pd.read_sql(table_or_sql,con=conn)
       return generator_object 
   
def lower(df):
    df_s=df.str.lower().str.replace('á','a').str.replace('é','e').str.replace('í','i').str.replace('ó','o').str.replace('ú','u').str.replace('ñ','n')
    return(df_s)

def llaveforanea(df,colum_cod_KF,tabla_KF,colum_name_KF,colum_name_dfKF,conn,
                 column_name_dfPK,colum_name_PF):
    #paso1: encontrar el valor con el que se relaciona
    #en la tabla de la llave foranea
    V=[]
    for i in tqdm(range(len(df))):
        my_query='''
        SELECT {} FROM {} WHERE {} = '{}'
        '''.format(colum_cod_KF,tabla_KF,colum_name_KF,df[colum_name_dfKF][i])
        
        #d_f=SQL_PD(my_query,conn)
        d_f=pd.read_sql(my_query,con=conn)
        
        v=[df[column_name_dfPK][i] ,int(d_f[colum_cod_KF][0])]
        V.append(v)
    V=pd.DataFrame(V)
    V.columns=[colum_name_PF,colum_cod_KF]
    return(V)



#------------------------#------
#-------------------------#

#VARIABLES DE ENTRADA
t_luisa=r"/media/luisa/Datos/FACOM/Datos_Hidrometeorol_gicos_Crudos_-_Red_de_Estaciones_IDEAM___Temperatura.csv"
p_luisa=r"/media/luisa/Datos/FACOM/P.csv"

VariableEntrada=p_luisa

#MOTOR DE BUSQUEDA
luisa="postgresql://luisa:000000@localhost:5432/BDPrueba"

#DIRECCION DE SALIDA DE ARCHIVOS
D1="/media/luisa/Datos/FACOM/gits/FACOM/otros_documentos" #guardar infomacióm
D2="/media/luisa/Datos/FACOM/gits/FACOM/otros_documentos/Cat_logo_Nacional_de_Estaciones_del_IDEAM.csv" #Catalogo nacional
#ABRIR CONEXIÓN CON LA BASE DE DATOS
engine = create_engine(luisa)
conn = engine.connect()

Motor=luisa
#-------------------------#
a="ValorObservado"
b="FechaObservacion"
c="CodigoEstacion"
d="Calidad"
e="Departamento"
f="Municipio"
g="Zona Hidrografica"
h="Tecnologia"
n="Categoria"
l="Estado"
#-------------------------#
#creación del motor
engine = create_engine(Motor)
#archivos de entrada
prueba=pd.read_csv(VariableEntrada,nrows=20, usecols=[0,2,3,10])
datos=pd.read_csv(D2)
#convertir a minuscula y eliminar caracteres especieales
datos[f] = pd.DataFrame(lower(datos[f]))
datos[g] = pd.DataFrame(lower(datos[g]))
datos[h] = pd.DataFrame(lower(datos[h]))
datos[l] = pd.DataFrame(lower(datos[l]))
datos[n] = pd.DataFrame(lower(datos[n]))


####################################################################################
#TABLAS CON NINGUNA LLAVE FORANEA
#############################
ac="nombre_categoria"
at="nombre_tecnologia"
ae="nombre_estado"
ad="nombre_departamento"
azh="nombre_zonahidrografica"
am="nombre_municipio"

cat_unicos=pd.DataFrame(list(datos[n].unique())) #Dataframe de los datos individuales
tec_unicos=pd.DataFrame(list(datos[h].unique())) #Dataframe de los datos individuales
est_unicos=pd.DataFrame(list(datos[l].unique())) #Dataframe de los datos individuales
dep_unicos=pd.DataFrame(list(datos[e].unique())) #Dataframe de los datos individuales
zoh_unicos=pd.DataFrame(list(datos[g].unique())) #Dataframe de los datos individuales

cat_unicos.columns=[ac]   #se cambia el nombre de la columna  
tec_unicos.columns=[at]   #se cambia el nombre de la columna 
est_unicos.columns=[ae]   #se cambia el nombre de la columna
dep_unicos.columns=[ad]   #se cambia el nombre de la columna 
zoh_unicos.columns=[azh]   #se cambia el nombre de la columna 


cat_unicos[ac] = lower(cat_unicos[ac]) #remover mayúsculas, vocales y ñ
tec_unicos[at] = lower(tec_unicos[at]) #remover mayúsculas, vocales y ñ
est_unicos[ae] = lower(est_unicos[ae]) #remover mayúsculas, vocales y ñ
dep_unicos[ad] = lower(dep_unicos[ad]) #remover mayúsculas, vocales y ñ
zoh_unicos[azh] = lower(zoh_unicos[azh]) #remover mayúsculas, vocales y ñ

#momentoobservacion
mo=[]
mo=pd.DataFrame(mo)
mo["fecha"]=pd.date_range(start="2000-01-01 00:00:00", end="2031-01-01 00:00:00", freq='min')
mo.columns=["fecha_observacion"]

#Se agrega a la base d datos
cat_unicos.to_sql("categoria", engine, if_exists= "append",index=False)
tec_unicos.to_sql("tecnologia", engine, if_exists= "append",index=False)
est_unicos.to_sql("estado", engine, if_exists= "append",index=False)
dep_unicos.to_sql("departamento", engine, if_exists= "append",index=False)
zoh_unicos.to_sql("zonahidrografica", engine, if_exists= "append",index=False)
mo.to_sql('momento_observacion', con=engine, index=False, if_exists='append', 
                  chunksize=10000)
###############################################################################
#TABLAS CON LLAVES FORANEAS
##############################
#Tabla municipio

mun_dep = pd.concat([datos[e],datos[f]],axis=1) # Relacionar municipios y departamentos en un dataframe
mun_dep = mun_dep.drop_duplicates (keep = 'first') # Conbinaciones individuales
mun_dep[e]=lower(mun_dep[e])
mun_dep[f]=lower(mun_dep[f])
mun_dep=mun_dep.reset_index(drop=True) #resetear el indice

municipio = llaveforanea(mun_dep,"cod_departamento","departamento","nombre_departamento",
                 e,luisa,f,"nombre_municipio")
##############################
#Tabla estación
n1=len(datos)
datos=pd.read_csv(D2)
nombre_estacion=datos.Nombre.str.split('-',expand=True).drop([1,2], axis=1)
nombre_estacion=pd.DataFrame(nombre_estacion[0].str.split('[',expand=True).drop([1], axis=1))

ubicacion=pd.DataFrame(datos['Ubicación'].str.replace('(','').str.replace(')','').str.split(',',expand=True))
ubicacion.columns=["latitud","longitud"]
datos.Altitud=pd.DataFrame(datos.Altitud.str.replace(',','.'))


#Cod_municipio
fkmunicipio_pkestacion = llaveforanea(datos,"cod_municipio","municipio","nombre_municipio",
                 f,conn,"Codigo","codigo_estacion")
#zona_hidrografica
fkzh_pkestacion = llaveforanea(datos,"cod_zonahidrografica","zonahidrografica",
                                      "nombre_zonahidrografica",g,conn,"Codigo","codigo_estacion")
#categoria
fkcategoria_pkestacion = llaveforanea(datos,"cod_categoria","categoria","nombre_categoria",
                 n,conn,"Codigo","codigo_estacion")
#tecnologia
fktecnologia_pkestacion = llaveforanea(datos,"cod_tecnologia","tecnologia","nombre_tecnologia",
                 h,conn,"Codigo","codigo_estacion")
#estado
fkestado_pkestacion = llaveforanea(datos,"cod_estado","estado","nombre_estado",
                 l,conn,"Codigo","codigo_estacion")

V=[]
for i in tqdm(range(n1)):
    cod=datos["Codigo"][i]
    
    v = [cod,nombre_estacion[0][i],ubicacion["latitud"][i],ubicacion["longitud"][i],datos["Altitud"][i],
         fkmunicipio_pkestacion.cod_municipio[i],fkzh_pkestacion.cod_zonahidrografica[i],
         fkcategoria_pkestacion.cod_categoria[i],fktecnologia_pkestacion.cod_tecnologia[i],
         fkestado_pkestacion.cod_estado[i]]
    V.append(v)
V=pd.DataFrame(V)

V.columns=["codigo_estacion","nombre_estacion","latitud","longitud","altitud",
           "cod_municipio","cod_zonahidrografica","cod_tecnologia","cod_estado","cod_categoria"]
    
#####################################


my_query1='''
SELECT {} FROM {} WHERE {} = '{}'
'''.format("cod_momentoobservacion","momento_observacion","fecha_observacion",prueba[b][0])

d_f=SQL_PD(my_query1,conn)
d_f=pd.read_sql(my_query1,con=conn)

rs = conn.execute(my_query1)

for row in rs:
    print(row)

###################################

#tabla observación
luisaSQLite= 'sqlite:////media/luisa/Datos/FACOM/gits/FACOM/db/precipitacion_2.db'
engine = create_engine(luisaSQLite)
conn = engine.connect()

query='''
SELECT CodigoEstacion,FechaObservacion,ValorObservado
FROM precipitacion
WHERE Departamento = 'antioquia'
'''

df= pd.read_sql(query,con=conn)
df=df.sort_values(by="FechaObservacion").reset_index(drop=True,inplace=False)
df[b]=pd.to_datetime(df[b],format='%m/%d/%Y %I:%M:%S %p')
df["calidad"]= np.zeros(len(df))

for index, row in tqdm(df.iterrows()):
    if row["ValorObservado"] < 0.0:
        df["calidad"][index] = 1.0
    if ((row["ValorObservado"] > 1.5) and (row["ValorObservado"] <= 2.0 )) :
         df["calidad"][index] = 1.0
    if row["ValorObservado"] > 2.0:
        df["calidad"][index] = 2.0






query1='''
SELECT *
FROM momento_observacion
''' 
df_mo= pd.read_sql(query1,con=conn)
df_mo

df_mo.to_csv(r"/media/luisa/Datos/FACOM/gits/FACOM/proyectos/posgrest/archivos/tabla_mo.csv",sep=";")
df.to_csv(r"/media/luisa/Datos/FACOM/gits/FACOM/proyectos/posgrest/archivos/antioquia.csv",sep=";")
for index, row in tqdm(df.iterrows()):
    print(1)       
 
fkmomentoobservacion_pkobservacion = llaveforanea(df,"cod_momentoobservacion",
                                   "momento_observacion","fecha_observacion",
                                   b,conn,b,"cod_observacion")    
        
        
    v = [prueba.ValorObservado[i],fkmomentoobservacion_pkobservacion.fkmomentoobservacion_pkobservacion[i],
         prueba[b][i],prueba["calidad"][i],fkvariable_pkobservacion.cod_variable[i]]


df


fkvariable_pkobservacion = llaveforanea(prueba,"cod_variable",
                                   "variable","descripcion_variable",
                                   "DescripcionSensor",conn,b,"cod_observacion")

fkmomentoobservacion_pkobservacion
fkvariable_pkobservacion
prueba
26135502 2016-07-02 12:15:00  ...      Temp Aire 2 m     0.0
prueba[b]=pd.to_datetime(prueba[b],format='%m/%d/%Y %I:%M:%S %p')
prueba["calidad"]= np.zeros(len(prueba))

m=prueba.groupby(prueba.ValorObservado > 0.0).count()
m
for index, row in tqdm(prueba.iterrows()):
    if ((row["ValorObservado"] >= 0.0) and (row["ValorObservado"] < 1.5 )) :
        #print(1)
        prueba["calidad"][index] = int(2.0)
    if row["ValorObservado"] < 0.0:
        #print(2)
        prueba["calidad"][index] = 1.0

for i in range(len(prueba)):
    
    v = [prueba.ValorObservado[i],fkmomentoobservacion_pkobservacion.fkmomentoobservacion_pkobservacion[i],
         prueba[b][i],prueba["calidad"][i],fkvariable_pkobservacion.cod_variable[i]]
    V.append(v)

V=pd.Dataframe(V)
V.column=["valor_observado", "cod_momentoobservacion","cod_estacion","calidad_dato","cod_variable"]

#se agrega a la base de datos
municipio.to_sql('municipio', con=engine, index=False, if_exists='append')
V.to_sql('estacion', con=engine, index=False, if_exists='append')




