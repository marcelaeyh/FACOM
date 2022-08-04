#----------------------------------------------------------------#
#1. LIBRERIAS
import pandas as pd
import numpy as np
from tqdm import tqdm # libreria para saber el tiempo de ejecuci´on
from sqlalchemy import create_engine
import time
import math
#----------------------------------------------------------------#
#2. CREACION DE VARIABLES DE NORMALIZACION, MOTOR DE POSTGRES, DIRECCIONES, CONJUNTO DE DATOS
#2.1 Base de datos
#2.1.1 postgresql
eng = "postgresql://facom:usuario@localhost:5432/alejandria" #Motor
engine = create_engine(eng) #Maquina
conn=engine.connect()

#2.3 Variables normalizadoras
vnC=['Codigo','Nombre','Categoria','Tecnologia','Estado','Departamento','Municipio', 
      'Ubicación','Altitud','Fecha_instalacion','Fecha_suspension','Area Operativa','Corriente',
      'Area Hidrografica','Zona Hidrografica','Subzona hidrografica','Entidad','Latitud','Longitud',
      'calidad','fecha_llaveforanea']

vnCSV=["CodigoEstacion","CodigoSensor","FechaObservacion","ValorObservado", "NombreEstacion",
        "Departamento","Municipio","ZonaHidrografica","Latitud","Longitud","DescripcionSensor",
        "UnidadMedida"]

vnBD=["nombre_categoria","nombre_tecnologia","nombre_estado", "nombre_departamento",
       "nombre_zonahidrografica","nombre_municipio","cod_departamento","cod_municipio",
       "cod_zonahidrografica","cod_categoria","cod_tecnologia","cod_estado","descripcion_variable",
       "unidad_medida","codigo_sensor","cod_estacion","nombre_estacion","latitud","longitud",
       "altitud","fecha_observacion","valor_observado","cod_estacion",
       "categoria_dato","cod_variable"]

tablas=["departamento","municipio","zonahidrografica","categoria","tecnologia","estado",
        "estacion","observacion","variable"]

#2.4 Direcciones
#2.4.1 
d1   = r"direccion del csv del catalogo nacional de estaciones IDEAM"
temp = r"direccion del csv de los datos de temperatura"
pre  = r"direccion del csv de los datos de precipitación"
pres = r"direccion del csv de los datos de presión"
direV= r"direccion del csv de los datos de direccion del viento"
veloV= r"direccion del csv de los datos de velocidad del viento"
coor = r"direccion del archivo coordenadas_estaciones.csv"

#conjunto de datos
datos = pd.read_csv(d1)

#----------------------------------------------------------------#
# 3. FUNCIONES
def lower(df):
    df_s = df.str.lower().str.replace('á','a').str.replace('é','e').str.replace('í','i')
    df_s = df_s.str.replace('ó','o').str.replace('ú','u').str.replace('ñ','n')
    return(df_s)

def llave(eng,tabla_FK,cod_FK,data,data_FK,nombredb_FK):
    q = '''
    SELECT * FROM {};
    '''.format(tabla_FK)
    b = pd.read_sql(q,con=eng)
    #b = SQL_PD(q,eng)
    b.set_index(cod_FK,inplace = True)
    
    cod = []
    
    for i in data[data_FK]:
        for j in b[nombredb_FK]:
            if i == j:
                cod.append(b.index[b[nombredb_FK] == j][0])
                break 
    return cod
#----------------------------------------------------------------#
# 4. CORRECIONES

#4.1 MAYUSCULAS, MINUSCULAS Y TILDES

datos[vnC[1]] = lower(datos[vnC[1]] ) #remover mayusculas, vocales y ñ
datos[vnC[2]] = lower(datos[vnC[2]] ) #remover mayusculas, vocales y ñ
datos[vnC[3]] = lower(datos[vnC[3]] ) #remover mayusculas, vocales y ñ
datos[vnC[4]] = lower(datos[vnC[4]] ) #remover mayusculas, vocales y ñ
datos[vnC[5]] = lower(datos[vnC[5]] ) #remover mayusculas, vocales y ñ
datos[vnC[6]] = lower(datos[vnC[6]] ) #remover mayusculas, vocales y ñ
datos[vnC[14]] = lower(datos[vnC[14]]) #remover mayusculas, vocales y ñ

#4.2 COLUMNA NOMBRE ESTACION
def nombres_cat(df):
    df=df.str.split('-',expand=True).drop([1,2], axis=1)
    df=pd.DataFrame(df[0].str.split('[',expand=True).drop([1], axis=1))
    return df

datos[vnC[1]] = nombres_cat(datos[vnC[1]])

#4.3 UBICACION
def ubicacion(datos):
    ubicacion = datos[vnC[7]].str.replace('(','').str.replace(')','').str.split(',',expand=True)
    
    '''
    Para reemplazar las coordenadas de los csv del IDEAM, por favor descomente el siguiente bloque de codigo.
    (recuerde que esto solo tendra un resultado positivo si previamente descargo y definio la ruta del
    archivo coordenadas_estaciones.csv que se encuentra en el repositorio de GitHub)
    '''
    
    '''
    c = pd.read_csv(coor,sep=";")
    # Reemplaza las coordenadas de las estaciones que estan en los csv del IDEAM
    for i in tqdm(range(len(datos))):
    for j in range(len(c)):
    if datos[vnC[0]][i] == c.Codigo[j]:
    ubicacion[0][i] = c.Latitud[j]
    ubicacion[1][i] = c.Longitud[j]
    '''
    return ubicacion[0].astype(float),ubicacion[1].astype(float)

lat, lon = ubicacion(datos)
datos.insert(17,"Latitud",lat)
datos.insert(18,"Longitud",lon)
datos =  datos.drop(columns=["Ubicación"])

#4.4 ALTITUD                
def Altitud(datos):                
    datos[vnC[8]]=pd.DataFrame(datos[vnC[8]].str.replace(',','')).astype(float)

Altitud(datos)

#----------------------------------------------------------------#
# 5.PROCESOS POR TABLA

#5.1 TABLA CATEGORIA
def categoria(datos):
    ca = pd.DataFrame(datos[vnC[2]].unique(),columns = [vnBD[0]])
    ca = ca.sort_values(vnBD[0])
    ca.to_sql(tablas[3], engine, if_exists= "append",index=False)
    
#5.2 TABLA DEPARTAMENTO
def departamento(datos):
    dep = pd.DataFrame(datos[vnC[5]].unique(),columns = [vnBD[3]])
    dep = dep.sort_values(vnBD[3])
    dep.to_sql(tablas[0], engine, if_exists= "append",index=False)
    
#5.3 TABLA ESTADO

def estado(datos):
    es = pd.DataFrame(datos[vnC[4]].unique(),columns = [vnBD[2]])
    es = es.sort_values(vnBD[2])
    es.to_sql(tablas[5], engine, if_exists= "append",index=False)


#5.4 TABLA TECNOLOGIA
def tecnologia(datos):
    tec = pd.DataFrame(datos[vnC[3]].unique(),columns = [vnBD[1]])
    tec = tec.sort_values(vnBD[1])
    tec.to_sql(tablas[4], engine, if_exists= "append",index=False)
    
#5.5 TABLA VARIABLE
def variable():
    temperatura = pd.read_csv(temp,nrows=1)
    precipitacion = pd.read_csv(pre,nrows=1)

    variable = pd.DataFrame(columns = [vnBD[12],vnBD[13],vnBD[14]])
    variable.descripcion_variable = [temperatura.DescripcionSensor[0],precipitacion.DescripcionSensor[0]]
    variable.unidad_medida = [temperatura.UnidadMedida[0],precipitacion.UnidadMedida[0]]
    variable.codigo_sensor = [temperatura.CodigoSensor[0],precipitacion.CodigoSensor[0]]
    
    # Se añade el df a la tabla variable
    variable.to_sql(tablas[8], engine, if_exists= "append",index=False)
    
#5.6 TABLA ZONA HIDROGRAFICA
def zonahidrografica(datos):
    zh = pd.DataFrame(datos[vnC[14]].unique(),columns = [vnBD[4]])
    zh = zh.sort_values(vnBD[4])
    zh.to_sql(tablas[2], engine, if_exists= "append",index=False)
    
#5.7 TABLA MUNICIPIO
def municipio(datos,eng):
    
    mun_cat = datos[[vnC[5],vnC[6]]]
    mun_cat = mun_cat.drop_duplicates(subset = vnC[6])
    mun_cat = mun_cat.sort_values(vnC[6])
    
    cod_mun = llave(eng,tablas[0],vnBD[6],mun_cat,vnC[5],vnBD[3])
    
    mun = pd.DataFrame(columns = [vnBD[6],vnBD[5]])
    mun.nombre_municipio = mun_cat[vnC[6]]
    mun.cod_departamento = cod_mun
    
    mun.to_sql(tablas[1], engine, if_exists= "append",index=False)
    
#5.8 TABLA ESTACION
def estacion(datos,eng):
    # Busqueda de Codigos
    
    cod_mun = llave(eng,tablas[1],vnBD[7],datos,vnC[6],vnBD[5])
    cod_zh = llave(eng,tablas[2],vnBD[8],datos,vnC[14],vnBD[4])
    cod_tec = llave(eng,tablas[4],vnBD[10],datos,vnC[3],vnBD[1])
    cod_est = llave(eng,tablas[5],vnBD[11],datos,vnC[4],vnBD[2])
    cod_cat = llave(eng,tablas[3],vnBD[9],datos,vnC[2],vnBD[0])
    
    estacion = pd.DataFrame(columns = [vnBD[15],vnBD[16],vnBD[17],vnBD[18],vnBD[7],
                                       vnBD[8],vnBD[9],vnBD[10],vnBD[11],vnBD[19]])
    
    estacion.cod_estacion = datos[vnC[0]]
    estacion.nombre_estacion = datos[vnC[1]]
    estacion.latitud = datos[vnC[17]]
    estacion.longitud = datos[vnC[18]]
    estacion.cod_municipio = cod_mun
    estacion.cod_zonahidrografica = cod_zh
    estacion.cod_categoria = cod_cat
    estacion.cod_tecnologia = cod_tec
    estacion.cod_estado = cod_est
    estacion.altitud = datos[vnC[8]]
    # Se añade el df a la tabla estacion
    estacion.to_sql(tablas[6], engine, if_exists= "append",index=False)

#----------------------------------------------------------------#
# EJECUCION DE LAS FUNCIONES PARA AGREGAR TABLAS
def añadirdb(catalogo,eng):
    departamento(catalogo)
    print("Se añadieron los datos a la tabla departamento")
    municipio(catalogo,eng)
    print("Se añadieron los datos a la tabla municipio")
    zonahidrografica(catalogo)
    print("Se añadieron los datos a la tabla zonahidrografica")
    categoria(catalogo)
    print("Se añadieron los datos a la tabla categoria")
    tecnologia(catalogo)
    print("Se añadieron los datos a la tabla tecnologia")
    estado(catalogo)
    print("Se añadieron los datos a la tabla estado")
    estacion(catalogo,eng)
    print("Se añadieron los datos a la tabla estacion")
    variable()
    print("Se añadieron los datos a la tabla variable")


añadirdb(datos,eng)

#----------------------------------------------------------------#
#5.9.1 PRECIPITACION

#logitud del archivo de entrada
lp=pd.read_csv(pre,usecols=[0])
n_p=len(lp)
del lp

step=math.ceil(n_p*0.05)  #el numero es el porcentaje que se va a tomar "dx"
cont=0 # el contador inicia desde 0, pero si es necesario se pue asignar uno diferente
dx=0
print("Longitud del archivo de entrada= ",n_p)
print("Los pasos de tiempo son de= ",step)
print("Inicia desde= ",cont)

while tqdm(cont <= (n_p-1)):
    start= time.time()
    #Las siguientes lineas de codigo toman una porcion de los datos y solo se ingresa
    #el porcentaje que se desea cargar, esto se asigno anteriormente en el paso.
    df=pd.read_csv(pre,nrows=int(step),skiprows=range(1,int(cont)),usecols=[0,2,3])
    print("#------#-------#")
    print("contador ",cont,"paso=",dx)
    print("#------#-------#")
    dx=dx+1
    
    df[vnCSV[2]]=pd.to_datetime(df[vnCSV[2]],format='%m/%d/%Y %I:%M:%S %p')
    df[vnCSV[2]] = df[vnCSV[2]].dt.floor('Min')
    df=df.sort_values(by=vnCSV[2]).reset_index(drop=True,inplace=False)
    df[vnC[19]]= np.zeros(len(df))
    df[vnC[20]]=np.zeros(len(df))
    n_df=len(df)
    
    # Categoria del dato
    for index, row in tqdm(df.iterrows()):
        
        if row[vnCSV[3]] < 0.0 or row[vnCSV[3]] >0.8:
            df[vnC[19]][index] = 1.0
       
    V=[]
    p=0
    
    for i in tqdm(range(p,n_df)):
        ab=df["CodigoEstacion"][i]
        if (ab==88112901 or ab==35237040 or ab==21202270 
            or ab==35217080 or ab==35227020 or ab==23157050 or ab==52017020):
            continue 
        
        if ab ==14015020:
            df[vnCSV[0]][i] = 14015080
        if ab==48015010:
            df[vnCSV[0]][i] = 48015050
            
        v =[df[vnCSV[3]][i],df[vnCSV[2]][i],df[vnCSV[0]][i],df[vnC[19]][i],2]
        V.append(v)

    V=pd.DataFrame(V)
    V.columns=[vnBD[21], vnBD[20],vnBD[22],vnBD[23],vnBD[24]]
    V.to_sql(tablas[7], con=engine, index=False, if_exists='append',chunksize=100000)
    cont=cont+step
    final= time.time()
    print("Tiempo de ejecucion",final-start)
    
#----------------------------------------------------------------#
#5.9.2 TEMPERATURA

#logitud del archivo de entrada
lt =pd.read_csv(temp,usecols=[0])
n_t=len(lt)
del lt

step=math.ceil(n_t*0.05)  #el numero es el porcentaje que se va a tomar "dx"
cont=0 # el contador inicia desde 0, pero si es necesario se pue asignar uno diferente
dx=0
print("Longitud del archivo de entrada= ",n_t)
print("Los pasos de tiempo son de= ",step)
print("Inicia desde= ",cont)
while tqdm(cont <= (n_t-1)):
    start= time.time()
    #Las siguientes lineas de codigo toman una porcion de los datos y solo se ingresa
    #el porcentaje que se desea cargar, esto se asigno anteriormente en el paso. 
    df=pd.read_csv(temp,nrows=int(step),skiprows=range(1,int(cont)),usecols=[0,2,3])
    print("######################")
    print("#------#-------#")
    print("contador",cont,"paso=",dx)
    print("#------#-------#")
    df[vnCSV[2]]=pd.to_datetime(df[vnCSV[2]],format='%m/%d/%Y %I:%M:%S %p')
    df[vnCSV[2]] = df[vnCSV[2]].dt.floor('Min')
    df=df.sort_values(by=vnCSV[2]).reset_index(drop=True,inplace=False)
    df[vnC[19]]= np.zeros(len(df))
    df[vnC[20]]=np.zeros(len(df))
    n_df=len(df)
    print("Ingresa la categoria-",dx)
    print("#------#-------#")
    # Categoria del dato
    for index, row in tqdm(df.iterrows()):
        
        if row[vnCSV[3]] < 1.3 or row[vnCSV[3]] > 32.90:
            df[vnC[19]][index] = 1 
       

    print("Ingresa a ingresar informacion-",dx)
    print("#------#-------#")       
    #Ingreso de la informacion
    V=[]
    p=0
    for i in tqdm(range(p,n_df)):
        ab=df["CodigoEstacion"][i]
        if (ab==88112901 or ab==35237040 or ab==21202270 
            or ab==35217080 or ab==35227020 or ab==23157050 or ab==52017020):
            continue 
        
        if ab ==14015020:
            df[vnCSV[0]][i] = 14015080
        if ab==48015010:
            df[vnCSV[0]][i] = 48015050
            
        v =[df[vnCSV[3]][i],df[vnCSV[2]][i],df[vnCSV[0]][i],df[vnC[19]][i],1]
        V.append(v)

    V=pd.DataFrame(V)
    V.columns=[vnBD[21], vnBD[20],vnBD[22],vnBD[23],vnBD[24]]
    V.to_sql(tablas[7], con=engine, index=False, if_exists='append',chunksize=100000)
    cont=cont+step
    final= time.time()
    print("Termina-",dx)
    print("#------#-------#")

    dx=dx+1
    print("Tiempo de ejecucion",final-start)
    print("#------#-------#")
    print("######################")
    
#----------------------------------------------------------------#
#5.9.3 DIRECCIÓN VIENTO

#logitud del archivo de entrada
ldv =pd.read_csv(direV,usecols=[0])
n_dv=len(ldv)
del ldv

step=math.ceil(n_dv*0.05)  #el numero es el porcentaje que se va a tomar "dx"
cont=0 # el contador inicia desde 0, pero si es necesario se pue asignar uno diferente
dx=0
print("Longitud del archivo de entrada= ",n_dv)
print("Los pasos de tiempo son de= ",step)
print("Inicia desde= ",cont)
while tqdm(cont <= (n_dv-1)):
    start= time.time()
    #Las siguientes lineas de codigo toman una porcion de los datos y solo se ingresa
    #el porcentaje que se desea cargar, esto se asigno anteriormente en el paso. 
    df=pd.read_csv(direV,nrows=int(step),skiprows=range(1,int(cont)),usecols=[0,2,3])
    print("######################")
    print("#------#-------#")
    print("contador",cont,"paso=",dx)
    print("#------#-------#")
    df[vnCSV[2]]=pd.to_datetime(df[vnCSV[2]],format='%m/%d/%Y %I:%M:%S %p')
    df[vnCSV[2]] = df[vnCSV[2]].dt.floor('Min')
    df=df.sort_values(by=vnCSV[2]).reset_index(drop=True,inplace=False)
    df[vnC[19]]= np.zeros(len(df))
    df[vnC[20]]=np.zeros(len(df))
    n_df=len(df)
    print("Ingresa la categoria-",dx)
    print("#------#-------#")
    # Categoria del dato
    for index, row in tqdm(df.iterrows()):
        
        if row[vnCSV[3]] < 0 or row[vnCSV[3]] > 360:
            df[vnC[19]][index] = 1 
       

    print("Ingresa a ingresar informacion-",dx)
    print("#------#-------#")       
    #Ingreso de la informacion
    V=[]
    p=0
    for i in tqdm(range(p,n_df)):
        ab=df["CodigoEstacion"][i]
        if (ab==88112901 or ab==35237040 or ab==21202270 
            or ab==35217080 or ab==35227020 or ab==23157050 or ab==52017020):
            continue 
        
        if ab ==14015020:
            df[vnCSV[0]][i] = 14015080
        if ab==48015010:
            df[vnCSV[0]][i] = 48015050
            
        v =[df[vnCSV[3]][i],df[vnCSV[2]][i],df[vnCSV[0]][i],df[vnC[19]][i],4]
        V.append(v)

    V=pd.DataFrame(V)
    V.columns=[vnBD[21], vnBD[20],vnBD[22],vnBD[23],vnBD[24]]
    V.to_sql(tablas[7], con=engine, index=False, if_exists='append',chunksize=100000)
    cont=cont+step
    final= time.time()
    print("Termina-",dx)
    print("#------#-------#")

    dx=dx+1
    print("Tiempo de ejecucion",final-start)
    print("#------#-------#")
    print("######################")

#----------------------------------------------------------------#
#5.9.4 VELOCIDAD DEL VIENTO

#logitud del archivo de entrada
lvev =pd.read_csv(veloV,usecols=[0])
n_vev=len(lvev)
del lvev

step=math.ceil(n_vev*0.05)  #el numero es el porcentaje que se va a tomar "dx"
cont=0 # el contador inicia desde 0, pero si es necesario se pue asignar uno diferente
dx=0
print("Longitud del archivo de entrada= ",n_vev)
print("Los pasos de tiempo son de= ",step)
print("Inicia desde= ",cont)
while tqdm(cont <= (n_vev-1)):
    start= time.time()
    #Las siguientes lineas de codigo toman una porcion de los datos y solo se ingresa
    #el porcentaje que se desea cargar, esto se asigno anteriormente en el paso. 
    df=pd.read_csv(veloV,nrows=int(step),skiprows=range(1,int(cont)),usecols=[0,2,3])
    print("######################")
    print("#------#-------#")
    print("contador",cont,"paso=",dx)
    print("#------#-------#")
    df[vnCSV[2]]=pd.to_datetime(df[vnCSV[2]],format='%m/%d/%Y %I:%M:%S %p')
    df[vnCSV[2]] = df[vnCSV[2]].dt.floor('Min')
    df=df.sort_values(by=vnCSV[2]).reset_index(drop=True,inplace=False)
    df[vnC[19]]= np.zeros(len(df))
    df[vnC[20]]=np.zeros(len(df))
    n_df=len(df)
    print("Ingresa la categoria-",dx)
    print("#------#-------#")
    # Categoria del dato
    for index, row in tqdm(df.iterrows()):
        
        if row[vnCSV[3]] < 0 or row[vnCSV[3]] > 50:
            df[vnC[19]][index] = 1 
       

    print("Ingresa a ingresar informacion-",dx)
    print("#------#-------#")       
    #Ingreso de la informacion
    V=[]
    p=0
    for i in tqdm(range(p,n_df)):
        ab=df["CodigoEstacion"][i]
        if (ab==88112901 or ab==35237040 or ab==21202270 
            or ab==35217080 or ab==35227020 or ab==23157050 or ab==52017020):
            continue 
        
        if ab ==14015020:
            df[vnCSV[0]][i] = 14015080
        if ab==48015010:
            df[vnCSV[0]][i] = 48015050
            
        v =[df[vnCSV[3]][i],df[vnCSV[2]][i],df[vnCSV[0]][i],df[vnC[19]][i],5]
        V.append(v)

    V=pd.DataFrame(V)
    V.columns=[vnBD[21], vnBD[20],vnBD[22],vnBD[23],vnBD[24]]
    V.to_sql(tablas[7], con=engine, index=False, if_exists='append',chunksize=100000)
    cont=cont+step
    final= time.time()
    print("Termina-",dx)
    print("#------#-------#")
    dx=dx+1
    print("Tiempo de ejecucion",final-start)
    print("#------#-------#")
    print("######################")