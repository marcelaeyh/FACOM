#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado el 24 de agosto de 2022

Autores: Marcela

Descripción: Acumulados/promedios horarios, diarios y mensuales para las diferentes
variables de la base de datos Alejandría. 

"""
################################ 1. LIBRERIAS ################################

import pandas as pd                  # Análisis de los datos  
from tqdm import tqdm                # Tiempo de ejecución
from sqlalchemy import create_engine # Conexión con la base de datos
import matplotlib.pyplot as plt      # Gráficar
import numpy as np                   # Matemáticas
import datetime                      # Manipulación de datos "fecha"
import scipy     
from scipy import stats
from datetime import datetime
################################ 2. FUNCIONES ################################ 

# 2.1 INTERVALO
'''Nota 1: PARA ENCONTRAR EL INTERVALO SE ASUME QUE: 
el intervalo de mayor frecuencia es el intervalo de la serie de datos.'''
def intervalo(datos,nombrecolumnafecha):
    vector=[]                                             # Vector para almacenar la diferencia en minutos. 
    for x in (range(len(datos)-1)):
        fi=datos[nombrecolumnafecha][x]                   # Fecha i
        fi1=datos[nombrecolumnafecha][x+1]                # Fecha i+1
        diferencia=fi1-fi                                 # Diferencia entre ambas. 
        minutos=diferencia.total_seconds()/60             # Se convierte la diferencia a minutos.
        vector.append(minutos)                            # Se agrega al vector. 
    vector=pd.DataFrame(vector,columns=["intervalo"])
    agrupacion= vector.groupby(['intervalo']).size().reset_index(name='cantidad')
    maxi=agrupacion.cantidad.max()
    minutomax=list(agrupacion["intervalo"][agrupacion.cantidad==maxi])
    frecuencia=(str(int(minutomax[0]))+"min")
    return(frecuencia,minutomax[0])
def SThorario(variable,tipo,nombrecolumnafecha,nombrecolumnavariable):
    print("Inicia el proceso para acumular/promediar los datos a resolución temporal horaria")
    #Primera parte hacer los scumulados horarios
    frecu,inter=intervalo(variable,nombrecolumnafecha)
    print("Intervalo = ", frecu)
    v=[]
    RT= (60/inter)
    for i in (y):
        for ii in (month):
            for iii in d:
                for iv in h:
                    acumulado=variable[variable.year==i][variable.month==ii][variable.day==iii][variable.hour==iv]
                    N=len(acumulado)
                    if N== 0.0:# Para evitar un error en el código más adelante.
                        continue
                    #Categorias del Umbral de datos perdidos
                    if N > 0.0 and N < ( RT*0.5): #CATEGORIA 0
                        acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                        if tipo ==1:
                            dia = acumulado[nombrecolumnavariable].sum()
                        elif tipo ==2:
                            dia = acumulado[nombrecolumnavariable].mean()
                        fecha = acumulado[nombrecolumnafecha].min()
                        v.append([fecha,dia,0])
                    if N >= ( RT*0.5) and N < ( RT*0.6): #CATEGORIA 1
                        acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                        if tipo ==1:
                            dia = acumulado[nombrecolumnavariable].sum()
                        elif tipo ==2:
                            dia = acumulado[nombrecolumnavariable].mean()
                        fecha = acumulado[nombrecolumnafecha].min()
                        v.append([fecha,dia,1])
                    if N >= ( RT*0.6) and N < ( RT*0.7): #CATEGORIA 2
                        acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                        if tipo ==1:
                            dia = acumulado[nombrecolumnavariable].sum()
                        elif tipo ==2:
                            dia = acumulado[nombrecolumnavariable].mean()
                        fecha = acumulado[nombrecolumnafecha].min()
                        v.append([fecha,dia,2])
                    if N >= ( RT*0.7) and N < ( RT*0.8): #CATEGORIA 3
                        acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                        if tipo ==1:
                            dia = acumulado[nombrecolumnavariable].sum()
                        elif tipo ==2:
                            dia = acumulado[nombrecolumnavariable].mean()
                        fecha = acumulado[nombrecolumnafecha].min()
                        v.append([fecha,dia,3])
                    if N >= ( RT*0.8) and N < ( RT*0.9): #CATEGORIA 4
                        acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                        if tipo ==1:
                            dia = acumulado[nombrecolumnavariable].sum()
                        elif tipo ==2:
                            dia = acumulado[nombrecolumnavariable].mean()
                        fecha = acumulado[nombrecolumnafecha].min()
                        v.append([fecha,dia,4])
                    if N >= ( RT*0.9): #CATEGORIA 5
                        acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                        if tipo ==1:
                            dia = acumulado[nombrecolumnavariable].sum()
                        elif tipo ==2:
                            dia = acumulado[nombrecolumnavariable].mean()
                        fecha = acumulado[nombrecolumnafecha].min()
                        v.append([fecha,dia,5])
                    
    v = pd.DataFrame(v,columns=["fecha","valor","categoria"])  # Se convierte el resultado en un dataframe.
    v["fecha"] = pd.to_datetime(v["fecha"])                    # Convertir fecha en Datatime.
    v["year"]=pd.to_datetime(v["fecha"]).dt.year
    v["month"]=pd.to_datetime(v["fecha"]).dt.month
    v["day"]=pd.to_datetime(v["fecha"]).dt.day
    v["hour"]=pd.to_datetime(v["fecha"]).dt.hour 
    v["fecha"]=v["fecha"].dt.floor('H')
    return(v)
def STdiario(variable,tipo,nombrecolumnafecha,nombrecolumnavariable):
    print("Inicia el proceso para acumular/promediar los datos a resolución temporal diaria")
    #Primera parte hacer los scumulados horarios
    frecu,inter=intervalo(variable,nombrecolumnafecha)
    v=[]
    RT= (60/inter)*24
    for i in (y):
        for ii in (month):
            for iii in d:
                acumulado=variable[variable.year==i][variable.month==ii][variable.day==iii]
                N=len(acumulado)
                if N== 0.0:# Para evitar un error en el código más adelante.
                    continue
                #Categorias del Umbral de datos perdidos
                if N > 0.0 and N < ( RT*0.5): #CATEGORIA 0
                    acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                    if tipo ==1:
                        dia = acumulado[nombrecolumnavariable].sum()
                    elif tipo ==2:
                        dia = acumulado[nombrecolumnavariable].mean()
                    fecha = acumulado[nombrecolumnafecha].min()
                    v.append([fecha,dia,0])
                if N >= ( RT*0.5) and N < ( RT*0.6): #CATEGORIA 1
                    acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                    if tipo ==1:
                        dia = acumulado[nombrecolumnavariable].sum()
                    elif tipo ==2:
                        dia = acumulado[nombrecolumnavariable].mean()
                    fecha = acumulado[nombrecolumnafecha].min()
                    v.append([fecha,dia,1])
                if N >= ( RT*0.6) and N < ( RT*0.7): #CATEGORIA 2
                    acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                    if tipo ==1:
                        dia = acumulado[nombrecolumnavariable].sum()
                    elif tipo ==2:
                        dia = acumulado[nombrecolumnavariable].mean()
                    fecha = acumulado[nombrecolumnafecha].min()
                    v.append([fecha,dia,2])
                if N >= ( RT*0.7) and N < ( RT*0.8): #CATEGORIA 3
                    acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                    if tipo ==1:
                        dia = acumulado[nombrecolumnavariable].sum()
                    elif tipo ==2:
                        dia = acumulado[nombrecolumnavariable].mean()
                    fecha = acumulado[nombrecolumnafecha].min()
                    v.append([fecha,dia,3])
                if N >= ( RT*0.8) and N < ( RT*0.9): #CATEGORIA 4
                    acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                    if tipo ==1:
                        dia = acumulado[nombrecolumnavariable].sum()
                    elif tipo ==2:
                        dia = acumulado[nombrecolumnavariable].mean()
                    fecha = acumulado[nombrecolumnafecha].min()
                    v.append([fecha,dia,4])
                if N >= ( RT*0.9): #CATEGORIA 5
                    acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                    if tipo ==1:
                        dia = acumulado[nombrecolumnavariable].sum()
                    elif tipo ==2:
                        dia = acumulado[nombrecolumnavariable].mean()
                    fecha = acumulado[nombrecolumnafecha].min()
                    v.append([fecha,dia,5])
                    
    v = pd.DataFrame(v,columns=["fecha","valor","categoria"])  # Se convierte el resultado en un dataframe.
    v["fecha"] = pd.to_datetime(v["fecha"])                    # Convertir fecha en Datatime.
    v["year"]=pd.to_datetime(v["fecha"]).dt.year
    v["month"]=pd.to_datetime(v["fecha"]).dt.month
    v["day"]=pd.to_datetime(v["fecha"]).dt.day
    v["fecha"]=v["fecha"].dt.floor('D')
    return(v)
def STmensual(variable,tipo,nombrecolumnafecha,nombrecolumnavariable):
    #No se tiene en cuenta los años bisiestos
    print("Inicia el proceso para acumular/promediar los datos a resolución temporal mensual")
    #Primera parte hacer los scumulados horarios
    frecu,inter=intervalo(variable,nombrecolumnafecha)
    v=[]
    diameses=[31,28,31,30,31,30,31,31,30,31,30,31]
    for i in (y):
        for ii in (month):
            acumulado=variable[variable.year==i][variable.month==ii]
            RT= (60/inter)*24*diameses[ii-1] # se tiene en cuenta la cantidad de días por mes.
            N=len(acumulado)
            if N== 0.0:# Para evitar un error en el código más adelante.
                continue
            #Categorias del Umbral de datos perdidos
            if N > 0.0 and N < ( RT*0.5): #CATEGORIA 0
                acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                if tipo ==1:
                    dia = acumulado[nombrecolumnavariable].sum()
                elif tipo ==2:
                    dia = acumulado[nombrecolumnavariable].mean()
                fecha = datetime(acumulado.year.min(), acumulado.month.min(),1)
                v.append([fecha,dia,0])
            if N >= ( RT*0.5) and N < ( RT*0.6): #CATEGORIA 1
                acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                if tipo ==1:
                    dia = acumulado[nombrecolumnavariable].sum()
                elif tipo ==2:
                    dia = acumulado[nombrecolumnavariable].mean()
                fecha = datetime(acumulado.year.min(), acumulado.month.min(),1)
                v.append([fecha,dia,1])
            if N >= ( RT*0.6) and N < ( RT*0.7): #CATEGORIA 2
                acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                if tipo ==1:
                    dia = acumulado[nombrecolumnavariable].sum()
                elif tipo ==2:
                    dia = acumulado[nombrecolumnavariable].mean()
                fecha =datetime(acumulado.year.min(), acumulado.month.min(),1)
                v.append([fecha,dia,2])
            if N >= ( RT*0.7) and N < ( RT*0.8): #CATEGORIA 3
                acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                if tipo ==1:
                    dia = acumulado[nombrecolumnavariable].sum()
                elif tipo ==2:
                    dia = acumulado[nombrecolumnavariable].mean()
                fecha = datetime(acumulado.year.min(), acumulado.month.min(),1)
                v.append([fecha,dia,3])
            if N >= ( RT*0.8) and N < ( RT*0.9): #CATEGORIA 4
                acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                if tipo ==1:
                    dia = acumulado[nombrecolumnavariable].sum()
                elif tipo ==2:
                    dia = acumulado[nombrecolumnavariable].mean()
                fecha = datetime(acumulado.year.min(), acumulado.month.min(),1)
                v.append([fecha,dia,4])
            if N >= ( RT*0.9): #CATEGORIA 5
                acumulado.reset_index(drop = True,inplace = True) # Se resetea el indice del nuevo vector de salida.
                if tipo ==1:
                    dia = acumulado[nombrecolumnavariable].sum()
                elif tipo ==2:
                    dia = acumulado[nombrecolumnavariable].mean()
                fecha = datetime(acumulado.year.min(), acumulado.month.min(),1)
                v.append([fecha,dia,5])
                    
    v = pd.DataFrame(v,columns=["fecha","valor","categoria"])  # Se convierte el resultado en un dataframe.
    v["fecha"] = pd.to_datetime(v["fecha"])                    # Convertir fecha en Datatime.
    v["year"]=pd.to_datetime(v["fecha"]).dt.year
    v["month"]=pd.to_datetime(v["fecha"]).dt.month
    v["day"]=pd.to_datetime(v["fecha"]).dt.day
    return(v)
################################ 3. INFORMACION DE ENTRADA ################################
## 3.1 Base de datos de Postgresql ALEJANDRÍA
eng = "postgresql://facom:usuario@localhost:5432/alejandria" #Motor.
engine = create_engine(eng)                                 #Máquina.
conn=engine.connect() 
## 3.2 Base de datos de Postgresql A2
eng1 = "postgresql://facom:usuario@localhost:5432/a2" #Motor.
engine1 = create_engine(eng1)                                 #Máquina.
conn1=engine1.connect()   
################################ 4. PROCESOS ################################ 

#4.1 Variables
#4.1.1 Encontrar todas las estaciones que tengan información de alguna variable
query1=''' 
SELECT estacion.cod_estacion 
FROM estacion INNER JOIN observacion ON observacion.cod_estacion=estacion.cod_estacion
WHERE cod_variable=1 or cod_variable=2 or cod_variable=3 or cod_variable=4 or cod_variable=5
GROUP BY estacion.cod_estacion 
'''
estaciones= pd.read_sql(query1,con=eng) # Estaciones IDEAM con información

bd=["fecha_observacion","valor_observado","cod_estacion","categoria_dato",
    "cod_variable","intervalo"] # Nombresde columnas en la base de datos

tablas=["observacion_horaria","observacion_diaria","observacion_mensual","intervalo"]
month=[1,2,3,4,5,6,7,8,9,10,11,12]
d=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
h=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
month.sort()
d.sort()
h.sort()
p=2+137+15
for j in tqdm(range(p,len(estaciones))):
    print("PASO 1")
    #Encontrar la información de la estación
    cod=estaciones.cod_estacion[j]
    query2='''
    SELECT valor_observado,fecha_observacion,cod_estacion,cod_variable
    FROM observacion
    WHERE cod_estacion={} and categoria_dato=0
    '''.format(cod)

    datos=pd.read_sql(query2,con=eng) # Busqueda en la base de datos de alejandria.
    
    print("PASO2")
    #Procesos con fechas
    datos["year"]=pd.to_datetime(datos[bd[0]]).dt.year   # crea una columna con los años.
    datos["month"]=pd.to_datetime(datos[bd[0]]).dt.month # crea una columna con los meses.
    datos["day"]=pd.to_datetime(datos[bd[0]]).dt.day     # crea una columna con los dias.
    datos["hour"]=pd.to_datetime(datos[bd[0]]).dt.hour   # crea una columna con los hora.
    
    #Separando dataframes por variables
    print("PASO3")
    temperatura=datos[datos.cod_variable==1]
    precipitacion= datos[datos.cod_variable==2]
    presión=datos[datos.cod_variable==3]
    direcionviento=datos[datos.cod_variable==4]
    velocidadviento=datos[datos.cod_variable==5]
    
    temperatura=temperatura.reset_index()
    precipitacion=precipitacion.reset_index()
    presión=presión.reset_index()
    direcionviento=direcionviento.reset_index()
    velocidadviento=velocidadviento.reset_index()

    #Temperatura
    print("PASO 4")
    if len(temperatura) >1:
        y=list(temperatura["year"].unique()) 
        y.sort()
        print("Cantidad de años a evaluar en temperatura= ",len(y))
        H,D,M,FRE,INT=0,0,0,0,0
        FRE,INT=intervalo(temperatura,bd[0])
        H=SThorario(temperatura,2,bd[0],bd[1])
        D=STdiario(temperatura,2,bd[0],bd[1])
        M=STmensual(temperatura,2,bd[0],bd[1])
        tH,tD,tM,tInt=[],[],[],[]
        
        #Tabla observacion horaria
        v=0
        for i in (range(len(H))):
            v=[H.valor[i],H.fecha[i],cod,H.categoria[i],1]
            tH.append(v)
        tH = pd.DataFrame(tH,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla observacion diaria
        v=0
        for i in (range(len(D))):
            v=[D.valor[i],D.fecha[i],cod,D.categoria[i],1]
            tD.append(v)
        tD = pd.DataFrame(tD,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla observacion mensual
        v=0
        for i in (range(len(M))):
            v=[M.valor[i],M.fecha[i],cod,M.categoria[i],1]
            tM.append(v)
        tM = pd.DataFrame(tM,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla de intervalo
        tInt.append([cod,1,INT])
        tInt=pd.DataFrame(tInt,columns=[bd[2],bd[4],bd[5]])
        
        tH.to_sql(tablas[0], con=engine1, index=False, if_exists='append',chunksize=100000)
        tD.to_sql(tablas[1], con=engine1, index=False, if_exists='append',chunksize=100000)
        tM.to_sql(tablas[2], con=engine1, index=False, if_exists='append',chunksize=100000)
        tInt.to_sql(tablas[3], con=engine1, index=False, if_exists='append',chunksize=100000) 
    #Precipitacion
    print("PASO 5")
    if len(precipitacion) >1:
        y=list(precipitacion["year"].unique()) 
        y.sort()
        print("Cantidad de años a evaluar en precipitación= ",len(y))
        H,D,M,FRE,INT=0,0,0,0,0
        FRE,INT=intervalo(precipitacion,bd[0])
        H=SThorario(precipitacion,1,bd[0],bd[1])
        D=STdiario(precipitacion,1,bd[0],bd[1])
        M=STmensual(precipitacion,1,bd[0],bd[1])
        tH,tD,tM,tInt=[],[],[],[]
        
        #Tabla observacion horaria
        v=0
        for i in (range(len(H))):
            v=[H.valor[i],H.fecha[i],cod,H.categoria[i],2]
            tH.append(v)
        tH = pd.DataFrame(tH,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla observacion diaria
        v=0
        for i in (range(len(D))):
            v=[D.valor[i],D.fecha[i],cod,D.categoria[i],2]
            tD.append(v)
        tD = pd.DataFrame(tD,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla observacion mensual
        v=0
        for i in (range(len(M))):
            v=[M.valor[i],M.fecha[i],cod,M.categoria[i],2]
            tM.append(v)
        tM = pd.DataFrame(tM,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla de intervalo
        tInt.append([cod,2,INT])
        tInt=pd.DataFrame(tInt,columns=[bd[2],bd[4],bd[5]])
        
        tH.to_sql(tablas[0], con=engine1, index=False, if_exists='append',chunksize=100000)
        tD.to_sql(tablas[1], con=engine1, index=False, if_exists='append',chunksize=100000)
        tM.to_sql(tablas[2], con=engine1, index=False, if_exists='append',chunksize=100000)
        tInt.to_sql(tablas[3], con=engine1, index=False, if_exists='append',chunksize=100000) 
    #Presión
    print("PASO 6")
    if len(presión) >1:
        y=list(presión["year"].unique()) 
        y.sort()
        print("Cantidad de años a evaluar en presión= ",len(y))
        H,D,M,FRE,INT=0,0,0,0,0
        FRE,INT=intervalo(presión,bd[0])
        H=SThorario(presión,2,bd[0],bd[1])
        D=STdiario(presión,2,bd[0],bd[1])
        M=STmensual(presión,2,bd[0],bd[1])
        tH,tD,tM,tInt=[],[],[],[]
        
        #Tabla observacion horaria
        v=0
        for i in (range(len(H))):
            v=[H.valor[i],H.fecha[i],cod,H.categoria[i],3]
            tH.append(v)
        tH = pd.DataFrame(tH,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla observacion diaria
        v=0
        for i in (range(len(D))):
            v=[D.valor[i],D.fecha[i],cod,D.categoria[i],3]
            tD.append(v)
        tD = pd.DataFrame(tD,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla observacion mensual
        v=0
        for i in (range(len(M))):
            v=[M.valor[i],M.fecha[i],cod,M.categoria[i],3]
            tM.append(v)
        tM = pd.DataFrame(tM,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla de intervalo
        tInt.append([cod,3,INT])
        tInt=pd.DataFrame(tInt,columns=[bd[2],bd[4],bd[5]])
        
        tH.to_sql(tablas[0], con=engine1, index=False, if_exists='append',chunksize=100000)
        tD.to_sql(tablas[1], con=engine1, index=False, if_exists='append',chunksize=100000)
        tM.to_sql(tablas[2], con=engine1, index=False, if_exists='append',chunksize=100000)
        tInt.to_sql(tablas[3], con=engine1, index=False, if_exists='append',chunksize=100000)
    #Direción viento
    print("PASO 7")
    if len(direcionviento) >1:
        y=list(direcionviento["year"].unique()) 
        y.sort()
        print("Cantidad de años a evaluar en direccion del viento= ",len(y))
        H,D,M,FRE,INT=0,0,0,0,0
        FRE,INT=intervalo(direcionviento,bd[0])
        H=SThorario(direcionviento,2,bd[0],bd[1])
        D=STdiario(direcionviento,2,bd[0],bd[1])
        M=STmensual(direcionviento,2,bd[0],bd[1])
        tH,tD,tM,tInt=[],[],[],[]
        
        #Tabla observacion horaria
        v=0
        for i in (range(len(H))):
            v=[H.valor[i],H.fecha[i],cod,H.categoria[i],4]
            tH.append(v)
        tH = pd.DataFrame(tH,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla observacion diaria
        v=0
        for i in (range(len(D))):
            v=[D.valor[i],D.fecha[i],cod,D.categoria[i],4]
            tD.append(v)
        tD = pd.DataFrame(tD,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla observacion mensual
        v=0
        for i in (range(len(M))):
            v=[M.valor[i],M.fecha[i],cod,M.categoria[i],4]
            tM.append(v)
        tM = pd.DataFrame(tM,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla de intervalo
        tInt.append([cod,4,INT])
        tInt=pd.DataFrame(tInt,columns=[bd[2],bd[4],bd[5]])
        
        tH.to_sql(tablas[0], con=engine1, index=False, if_exists='append',chunksize=100000)
        tD.to_sql(tablas[1], con=engine1, index=False, if_exists='append',chunksize=100000)
        tM.to_sql(tablas[2], con=engine1, index=False, if_exists='append',chunksize=100000)
        tInt.to_sql(tablas[3], con=engine1, index=False, if_exists='append',chunksize=100000)
    #Velocidad viento
    print("PASO 8")
    if len(velocidadviento) >1:
        y=list(velocidadviento["year"].unique()) 
        y.sort()
        print("Cantidad de años a evaluar en velocidad del viento= ",len(y))
        H,D,M,FRE,INT=0,0,0,0,0
        FRE,INT=intervalo(velocidadviento,bd[0])
        H=SThorario(velocidadviento,2,bd[0],bd[1])
        D=STdiario(velocidadviento,2,bd[0],bd[1])
        M=STmensual(velocidadviento,2,bd[0],bd[1])
        tH,tD,tM,tInt=[],[],[],[]
        
        #Tabla observacion horaria
        v=0
        for i in (range(len(H))):
            v=[H.valor[i],H.fecha[i],cod,H.categoria[i],5]
            tH.append(v)
        tH = pd.DataFrame(tH,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla observacion diaria
        v=0
        for i in (range(len(D))):
            v=[D.valor[i],D.fecha[i],cod,D.categoria[i],5]
            tD.append(v)
        tD = pd.DataFrame(tD,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla observacion mensual
        v=0
        for i in (range(len(M))):
            v=[M.valor[i],M.fecha[i],cod,M.categoria[i],5]
            tM.append(v)
        tM = pd.DataFrame(tM,columns=[bd[1],bd[0],bd[2],bd[3],bd[4]])
        #Tabla de intervalo
        tInt.append([cod,5,INT])
        tInt=pd.DataFrame(tInt,columns=[bd[2],bd[4],bd[5]])
        
        tH.to_sql(tablas[0], con=engine1, index=False, if_exists='append',chunksize=100000)
        tD.to_sql(tablas[1], con=engine1, index=False, if_exists='append',chunksize=100000)
        tM.to_sql(tablas[2], con=engine1, index=False, if_exists='append',chunksize=100000)
        tInt.to_sql(tablas[3], con=engine1, index=False, if_exists='append',chunksize=100000)

#Fin del codigo
        




