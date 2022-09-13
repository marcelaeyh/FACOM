#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 17:29:39 2022

@author: marcelae
"""
###############################################################################

#1. LIBRERIAS
import pandas as pd
import  numpy as np
from tqdm import tqdm              # librería para saber el tiempo de ejecución.
from sqlalchemy import create_engine
import matplotlib.pyplot as plt    #Para graficar.

# 4. PROCESOS 
# 4.1 Convertir la fecha en datatime y crear las columnas  de año, mes, día y hora.
def conv_fecha(datos,nombrecolumnafecha):
    datos[nombrecolumnafecha]=pd.to_datetime(datos[nombrecolumnafecha]) #conversión a datatime.
    datos["year"]=pd.to_datetime(datos[nombrecolumnafecha]).dt.year  # crea una columna con los años.
    datos["month"]=pd.to_datetime(datos[nombrecolumnafecha]).dt.month # crea una columna con los meses.
    datos["day"]=pd.to_datetime(datos[nombrecolumnafecha]).dt.day  # crea una columna con los días.
    datos["hour"]=pd.to_datetime(datos[nombrecolumnafecha]).dt.hour # crea una columna con los hora.
    return datos

# 3. FUNCIONES
#Lista de funciones disponibles.
#3.1 Serie de tiempo de promedios/acumulados horarios


#3.1 Serie de tiempo de promedios/acumulados horarios.
#Descripción: Permite generar una serie de tiempo horario, entrega un dataframe con el valor generado y
# fecha(mes-día).
#Variable: son los datos que se ingresan como dataframe, tipo: según el tipo promedio/acumulado
# se pone 2 o 1 respectivamente, nombrecolumnafecha: es el nombre de la columna dentro del 
# dataframe para la fecha, nombrecolumnavariable: es el nombre de la columna dentro del 
# dataframe para la el valor observado de la variable.
#Esta función requiere un dataframe con fecha en datatime, además 3 columnas una para el 
# año, otra para el mes, dia que se puede generar con: pd.datatime(datos.fecha).df.year/month/day/hour. 
#IMPORTANTE: Los acumulados quedan en unidades de mm/día
def SThorarios(variable,tipo,nombrecolumnafecha,nombrecolumnavariable,y,month,d,h):
    v=[]
    for i in tqdm(y):
        for j in (month):
            for k in d:
                for l in h:
                    acumulado=variable[variable.year==i][variable.month==j][variable.day==k][variable.hour==l]
                    if len(acumulado) == 0.0: # vector para evitar un error en el código más adelante
                        continue
                    acumulado.reset_index(drop = True,inplace = True) #se resetea el indice del nuevo vector de salida
                    if tipo ==1:
                        dia = acumulado[nombrecolumnavariable].sum()
                    elif tipo ==2:
                        dia = acumulado[nombrecolumnavariable].mean()
                    fecha = acumulado[nombrecolumnafecha].min()
                    v.append([fecha,dia])
                    
    v = pd.DataFrame(v,columns=["fecha","valor"]) # Se convierte el resultado en un dataframe
    v["fecha"] = pd.to_datetime(v["fecha"]) # convertir fecha en Datatime
    v=v.set_index(["fecha"]) # se pone la fecha como indice
    return v

#3.2 Serie de tiempo de promedios/acumulados diarios.
#Descripción: Permite generar una serie de tiempo diaria, entrega un dataframe con 
# el valor, fecha(mes-día) y 3 columnas con el año, mes y día.
#Variable: son los datos que se ingresan como dataframe, tipo: según el tipo promedio/acumulado
# se pone 2 o 1 respectivamente, nombrecolumnafecha: es el nombre de la columna dentro del 
# dataframe para la fecha, nombrecolumnavariable: es el nombre de la columna dentro del 
# dataframe para la el valor observado de la variable.
#Esta función requiere un dataframe con fecha en datatime, además 3 columnas, una para el año, 
# otra para el mes, día que se puede generar con: pd.datatime(datos.fecha).df.year/month/day/hour. 
#IMPORTANTE: Los acumulados quedan en unidades de mm/día
def STdiarios(variable,tipo,nombrecolumnafecha,nombrecolumnavariable,y,month,d):
    v=[]
    for i in tqdm(y):
        for j in month:
            for k in d:
                acumulado=variable[variable.year==i][variable.month==j][variable.day==k]
                if len(acumulado) == 0.0: # vector para evitar un error en el código más adelante
                    continue
                acumulado.reset_index(drop = True,inplace = True) #se resetea el indice del nuevo vector de salida
                if tipo ==1:
                    dia = acumulado[nombrecolumnavariable].sum()
                elif tipo ==2:
                    dia = acumulado[nombrecolumnavariable].mean()
                fecha = acumulado[nombrecolumnafecha].min()
                fecha= fecha.strftime('%Y-%m-%d')
                v.append([fecha,dia])
    v = pd.DataFrame(v,columns=["fecha","valor"]) # Se convierte el resultado en un dataframe
    v["fecha"] = pd.to_datetime(v["fecha"]) # convertir fecha en Datatime
    v["year"]=pd.to_datetime(v.fecha).dt.year
    v["month"]=pd.to_datetime(v.fecha).dt.month
    v["day"]=pd.to_datetime(v.fecha).dt.day
    v=v.set_index(["fecha"]) # se pone la fecha como indice
    return v

# 3.3 Serie de tiempo de promedios mensuales para datos diarios.
#Descripción: Esta función permite  generar una serie de tiempo de promedios mensuales 
# con la serie de tiempo de promedios/acumulados diarios, entraga un dataframe con 6 columnas
# valor, fecha, año, mes, día y hora.
#datos: son los datos que se ingresan como dataframe, tipoPD: según el tipo promedio/acumulado
# se pone 2 o 1 respectivamente para los promedios/acumulados diarios, 
# nombrecolumnafecha: es el nombre de la columna dentro del dataframe para la fecha, 
# nombrecolumnavariable: es el nombre de la columna dentro del dataframe para la el valor observado 
# de la variable.
#Esta función requiere un dataframe con fecha en datatime, además 3 columnas, una para el año, 
# otra para el mes, día que se puede generar con: pd.datatime(datos.fecha).df.year/month/day/hour. 
# además requiere de la función de promedios diarios.
#IMPORTANTE: Los acumulados quedan en unidades de mm/día
def STmensual(datos,tipoPD,nombrecolumnafecha,nombrecolumnavariable,y,month,d):
    df1=STdiarios(datos,tipoPD,nombrecolumnafecha,nombrecolumnavariable,y,month,d) #promedios diarios 
    df2=df1.valor.resample('M').mean() #serie de tiempo mensual
    df2=df2.reset_index()
    df2["year"]=pd.to_datetime(df2["fecha"]).dt.year  # crea una columna con los años
    df2["month"]=pd.to_datetime(df2["fecha"]).dt.month # crea una columna con los meses
    df2["day"]=pd.to_datetime(df2["fecha"]).dt.day  # crea una columna con los dias
    df2["hour"]=pd.to_datetime(df2["fecha"]).dt.hour # crea una columna con los hora
    return df2

# 3.4 Ciclo medio diurno para un día particular (acumulado/promediado).
#Descripción: es un gráfico donde se acumulan/promedian todos los minutos contenidos en una hora 
# de un mes, dia y año particulares, que luego va a ser promediados con el resto de sumas/promedios de esa hora 
# en diferentes años del conjunto de datos.
#dia= día que se quiere analizar, mes= mes que se quiere analizar,
# nombrecolumnavariable= nombre de la columna donde se encuentran los valores observados para
# la variable, nombrecolumnafecha= nombre de la columna donde se ubica la fecha y tipo es para 
# elegir si se hacen acumulados horarios o promedios.
#Los datos de fecha se deben ingresar como DATATIME y se deben crear
# cuatro columnas una para los años, otra para los meses, dias y horas
#IMPORTANTE: Los acumulados quedan en unidades de mm/hora
def CMD_dia(dia,mes,y,variable,nombrecolumnavariable,nombrecolumnafecha,tipo):
    # Sumar cada hora en cada año del día que se quiere analizar
    v = [] # vector donde se acumulan los resultados del ciclo for
    for i in tqdm(y):
        for j in h:
            acumulado = variable[variable.month == mes][variable.day == dia][variable.year == i][variable.hour == j] # acumula un vector con ese día.
            if len(acumulado) == 0.0: # vector para evitar un error en el código más adelante
                continue
            acumulado.reset_index(drop = True,inplace = True) #se resetea el indice del nuevo vector de salida
            # Segun la variable se añade la variable que se va a sumar y se almacena la fecha
            if tipo ==1:
                suma = acumulado[nombrecolumnavariable].sum()
            elif tipo ==2:
                suma = acumulado[nombrecolumnavariable].mean()
            fecha = acumulado[nombrecolumnafecha].min()
            v.append([fecha,suma])
    v = pd.DataFrame(v,columns=["fecha","valor"]) # Se convierte el resultado en un dataframe
    v["fecha"] = pd.to_datetime(v["fecha"]) # convertir fecha en Datatime
    v=v.set_index(["fecha"]) # se pone la fecha como indice
    v1=v["valor"].groupby(v.index.hour).mean()
    v1=v1.reset_index()
    return(v1)
# 3.5  Ciclo medio diurno de un mes particular (acumulada/promediado).
# Es un grafico donde se acumulan/promedian todos los minutos contenidos en una hora particular
# de un mes, dia y año, que luego va a ser promediado con el resto de acumulados/promedios
# de esa hora en diferentes años del conjunto de datos.
#Variables pedidas: dia= día que se quiere analizar, mes= mes que se quiere analizar,
# nombrecolumnavariable= nombre de la columna donde se encuentran los valores observados para
# la variable, nombrecolumnafecha= nombre de la columna donde se ubica la fecha y tipo es para 
# elegir si se hacen acumulados horarios o promedios.
#Los datos de fecha se deben ingresar como DATATIME y se deben crear
# cuatro columnas una para los años, otra para los meses, dias y horas
#IMPORTANTE: Los acumulados quedan en unidades de mm/hr
def CMD_mes(y,variable,mes,nombrecolumnavariable,nombrecolumnafecha,tipo):
    v = [] # vector donde se acumulan los resultados del ciclo for
    for i in tqdm(y):
        for k in d :
            for j in h:
                acumulado = variable[variable.month == mes][variable.day == k][variable.year == i][variable.hour == j] # acumula un vector con ese día.
                if len(acumulado) == 0.0: # vector para evitar un error en el código más adelante
                    continue
                acumulado.reset_index(drop = True,inplace = True) #se resetea el indice del nuevo vector de salida
                # Segun la variable se añade la variable que se va a sumar y se almacena la fecha
                if tipo ==1:
                    suma = acumulado[nombrecolumnavariable].sum()
                elif tipo ==2:
                    suma = acumulado[nombrecolumnavariable].mean()
                fecha = acumulado[nombrecolumnafecha].min()
                v.append([fecha,suma])

    v = pd.DataFrame(v,columns=["fecha","valor"]) # Se convierte el resultado en un dataframe
    v["fecha"] = pd.to_datetime(v["fecha"]) # convertir fecha en Datatime
    v=v.set_index(["fecha"]) # se pone la fecha como indice
    v1=v["valor"].groupby(v.index.hour).mean()
    return(v1)
# 3.6 Ciclo medio anual (diario, 366 días).
#Descripción: Esta función genera un ciclo medio anual para los 366 días del año, entrega
# 4 columnas, fecha, valor promedio del día, el mes y el día respectivo.
#Variable: son los datos que se ingresan como dataframe, tipo: según el tipo promedio/acumulado
# se pone 2 o 1 respectivamente, nombrecolumnafecha: es el nombre de la columna dentro del 
# dataframe para la fecha, nombrecolumnavariable: es el nombre de la columna dentro del 
# dataframe para la el valor observado de la variable.
#Esta función requiere un dataframe con fecha en datatime, además 3 columnas una para el 
#año, otra para el mes, dia que se puede generar con:
# pd.datatime(datos.fecha).df.year/month/day/hour. 
#IMPORTANTE: La unidades que se obtienen de los acumulados es de [mm/día]
def CMA_dias(variable,tipo,nombrecolumnafecha,nombrecolumnavariable):
    variable1=STdiarios(variable,tipo,nombrecolumnafecha,nombrecolumnavariable) #promedios/acumulados diarios
    variable1.reset_index(drop = False,inplace = True) #se resetea el indice del nuevo vector de salida
    variable1["year"]=pd.to_datetime(variable1["fecha"]).dt.year  # crea una columna con los años
    variable1["month"]=pd.to_datetime(variable1["fecha"]).dt.month # crea una columna con los meses
    variable1["day"]=pd.to_datetime(variable1["fecha"]).dt.day  # crea una columna con los dias
    variable1["hour"]=pd.to_datetime(variable1["fecha"]).dt.hour # crea una columna con los hora
    v=[]
    for i in month:
        for j in d:
            acumulado=variable1[variable1.day==j][variable1.month==i]
            if len(acumulado) == 0.0: # vector para evitar un error en el código más adelante
                continue
            acumulado.reset_index(drop = False,inplace = True) #se resetea el indice del nuevo vector de salida
            mean=acumulado["valor"].mean()
            fecha =acumulado["fecha"].min()
            fmes=pd.to_datetime(acumulado.fecha).dt.month
            fdia=pd.to_datetime(acumulado.fecha).dt.day
            fecha= fecha.strftime('%m-%d')
            v.append([fecha,mean,fmes[0],fdia[0]])
    v=pd.DataFrame(v,columns=["fecha","valor","month",'day'])
    return v
# 3.7 Ciclo medio anual (mensual, 12 meses).
#Descripción: Esta función genera un ciclo medio anual para los 12 meses del año, entrega
# 2 columnas, el mes y valor promedio del mes respectivo.
#datos: son los datos que se ingresan como dataframe, tipoPD: según el tipo promedio/acumulado
# se pone 2 o 1 respectivamente para los promedios/acumulados diarios, 
# nombrecolumnafecha: es el nombre de la columna dentro del dataframe para la fecha, 
# nombrecolumnavariable: es el nombre de la columna dentro del dataframe para la el 
# valor observado de la variable.
#Esta función requiere un dataframe con fecha en datatime, además 3 columnas una para el 
#año, otra para el mes, dia que se puede generar con:
# pd.datatime(datos.fecha).df.year/month/day/hour. 
# además requiere de la función de promedios diarios.
#IMPORTANTE: La unidades que se obtienen de los acumulados es de [mm/día]
def CMA_mes(datos,tipoPD,nombrecolumnafecha,nombrecolumnavariable):
    df1=STdiarios(datos,tipoPD,nombrecolumnafecha,nombrecolumnavariable) #promedios diarios
    df2=df1["valor"].groupby(df1.index.month).mean() #cma_mensual
    df2=df2.reset_index()
    df2.columns=["month","valor"]
    return df2
# 3.8 Anomalías de la serie de tiempo de promedios/acumulados diarios.
#Descripción: Permite generar las anomalias de una serie de tiempo diaria, entrega
# un dataframe con el valor de la anomalía, fecha(mes-día).
#datos= dataframe, tipoPD ( ingresar 1 para acumulados(sumas) o 2 para promedios), 
# nombrecolumnafecha y nombrecolumnavalor son los nombres de la columna para la fecha y el valor.
#Esta función requiere un dataframe con fecha en datatime, además 3 columnas, una para el 
# año, otra para el mes, día que se puede generar con pd.datatime(datos.fecha).df.year/month/day/hour, y
# requiere la función para el ciclo medio anual de promedios/acumulados diarios y 
# la de promedios/acumulados diarios.
def anomalias_dia(datos,tipoPD,nombrecolumnafecha,nombrecolumnavalor):
    #Recordar que el tipoPD y el tipoCMAPD es para seleccionar si son acumulados o promedios.
    print("")
    print("")
    print("1.Promedios/acumulados diarios")
    print("")
    df1=STdiarios(datos,tipoPD,nombrecolumnafecha,nombrecolumnavalor) #promedios diarios
    print("")
    print("2. CMA diarios")
    print("")
    df2=CMA_dias(datos,tipoPD,nombrecolumnafecha,nombrecolumnavalor) #ciclo medio anual promedios diarios
    
    v=[] #Vector para ingresar los resultados 
    for i in tqdm(y): # año # Ejecuta las restas para encontrar las anomalías
        for j in month: # mes
            for k in d: #día
                acumulado1=df1[df1.year==i][df1.month==j][df1.day==k] #valor dia particular.
                acumulado2=df2[df2.month==j][df2.day==k] # valor del dia promedio.
                if len(acumulado1) == 0.0: # vector para evitar un error en el código más adelante
                    continue
                # reseteo del indice en ambos vectores
                acumulado1.reset_index(drop = False,inplace = True)
                acumulado2.reset_index(drop = False,inplace = True)
                
                resta=acumulado1.valor[0]-acumulado2.valor[0] # se ejecuta la resta
                
                fecha=acumulado1.fecha[0] #fecha analizada
                v.append([resta,fecha]) # se agrega al vector resultante
    v=pd.DataFrame(v,columns=["valor","fecha"])
    return(v)
#3.9 Anomalías de la serie de tiempo mensual.
#Descripción: Permite generar las anomalías de una serie de tiempo mensual, entrega
# un dataframe con el valor de la anomalía y la fecha.
#datos= dataframe, tipo (ingresar 1 para acumulados(sumas) o 2 para), 
#nombrecolumnafecha y nombrecolumnavalor son los nombres de la columna para la fecha y el valor
#Esta función requiere un dataframe con fecha en datatime, además 3 columnas, una para el 
#año, otra para el mes, día que se puede generar con pd.datatime(datos.fecha).df.year/month/day/hour. 
# además requiere la función para el ciclo medio anual mensual y la de promedios/acumulados mensuales.
def anomalias_mes(datos,tipo,nombrecolumnafecha,nombrecolumnavariable):
    #serie de tiempo de promedios mensuales de acumulados/promedios diarios
    df1=STmensual(datos,tipo,nombrecolumnafecha,nombrecolumnavariable) 
    #cma mensual de acumulados/promedios diarios
    df2=CMA_mes(datos,tipo,nombrecolumnafecha,nombrecolumnavariable)

    v=[] #Vector para ingresar los resultados 
    for i in tqdm(y): # año # Ejecuta las restas para encontrar las anomalías
        for j in month: # mes
            acumulado1=df1[df1.year==i][df1.month==j] #valor dia particular.
            acumulado2=df2[df2.month==j]# valor del dia promedio. 
            if len(acumulado1) == 0.0: # vector para evitar un error en el código más adelante
                continue
            # reseteo del indice en ambos vectores
            acumulado1.reset_index(drop = False,inplace = True)
            acumulado2.reset_index(drop = False,inplace = True)
            resta=acumulado1.valor[0]-acumulado2.valor[0] # se ejecuta la resta
            
            fecha=acumulado1.fecha[0] #fecha analizada
            v.append([resta,fecha]) # se agrega al vector resultante
    v=pd.DataFrame(v,columns=["valor","fecha"])
    return(v)