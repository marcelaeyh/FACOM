#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creado el 21 de junio de 2022 a las 16:21 , Autor: Luisa Fernanda Buriticá Ruíz
Objetivo: Definir unos gráficos básicos usando la base de datos alejandria. 
"""
###############################################################################

#1. LIBRERIAS
import pandas as pd
import  numpy as np
from tqdm import tqdm              # librería para saber el tiempo de ejecución.
from sqlalchemy import create_engine
import matplotlib.pyplot as plt    #Para graficar.
##############################################################################

# 2 . INFORMACIÓN DE ENTRADA
print("############# 2. Información de entrada ############################")
print("")
print("Nota Importante 1: ")
print("*Se sugiere crear una carpeta llamada 'graficos' y poner la ruta a la carpeta en 'Ingresar ruta de almacenamiento de graficos'.")
print("")
print("Nota Importante 2: ")
print("*Se sugiere crear una carpeta llamada 'csv' y poner la ruta a la carpeta en 'Ingresar ruta de almacenamiento de información en csv'.")
print("")
print("Nota Importante 3: ")
print("* Ingresar la información sin comillas y sin espacio al inicio.")
print("")
print("#########################################")
print("")

# 2.1 Motor y máquina de postgresql en alejandria.
print("No olvide ingresar el motor de su base de datos, abajo está un ejemplo ")
eng = "postgresql://luisa:000000@localhost:5432/alejandria" #Motor.
engine = create_engine(eng) #Creación de máquina.
conn=engine.connect() #Conección con de la máquina.

#2.2 Ingreso del conjunto de datos.
r2_2_1=input("¿La información de entrada está en alejandria? si/no :") 
print("#########################################")
print("")

# 2.3 Cuando el conjunto de datos NO pertenece a la base de datos alejandria.
if r2_2_1 == "no":
    print("")
    print("Nota Importante 4: ")
    print("* Este script solo le permite leer archivos csv.")
    print("")
    print("#########################################")

    print("")    
    d1=input("Ingrese la ruta del conjunto de datos:")
    print("")
    separador=input("¿Qué tipo de separador tiene el csv de entrada?")
    datos=pd.read_csv(str(d1),sep=str(separador))
    print("")
    nombrecolumnafecha=str(input("Escriba el nombre de la columna de la fecha: "))
    print("")
    nombrecolumnavariable=str(input("Escriba el nombre de la columna de la variable: "))
    print("")
    unidades=str(input("Ingrese las unidades de la variable: "))
    print("")
    print("#########################################")

# 2.4 Cuando el conjunto de datos SÍ pertenece a la base de datos alejandria.   
elif r2_2_1 == "si":
    print("")
    estacion=input("Código de estación:")
    print("")
    print("#########################################")
    print("")
    variable=str(input("Elija la variable \n Ingrese 'precipitacion' o 'temperatura': "))
    print("")
    print("############ ESPERE... #############################")
    if variable == "precipitacion":
        var=2
    elif variable == "temperatura":
        var=1
    #QUERY 1
    query='''
    select valor_observado,observacion.cod_estacion, fecha_observacion
    from observacion where cod_variable={} and cod_estacion ={} and categoria_dato <> 1
    '''.format(var,estacion)
    print("")
    print("Espere un momento mientras buscamos la información de la estación en la base de datos alejandria")
    print("")
    datos=pd.read_sql(query,con=eng)
    nombrecolumnafecha="fecha_observacion"
    nombrecolumnavariable="valor_observado"
    #QUERY 2
    query2='''
    select unidad_medida from variable
    where cod_variable={}
    '''.format(var)
    unidadesbusqueda=pd.read_sql(query2,con=eng)
    unidades=unidadesbusqueda["unidad_medida"][0]
    
print("#########################################")
print("RESULTADO = ")
print("")
print("Primero datos \n \n",datos.head())
print("")
print("Últimos datos \n \n",datos.tail())
print("#########################################")

# 2.5 Otros vectores de entrada.
meses=["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"] #meses para gráficos
meses1=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre",
        "Octubre","Noviembre","Diciembre"] # meses para gráficos

# 2.6 Otras preguntas
print("Ingrese la siguiente infomación como en el ejemplo acontinuación.")
print("* EJEMPLO= "+r"/media/luisa/Datos/FACOM/gits/FACOM/3_csv/")

dgra=str(input('Ingresar ruta de almacenamiento de graficos: '))
dcsv=str(input('Ingresar ruta de almacenamiento de información en csv: '))
print("#########################################")

##############################################################################
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
def SThorarios(variable,tipo,nombrecolumnafecha,nombrecolumnavariable):
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
def STdiarios(variable,tipo,nombrecolumnafecha,nombrecolumnavariable):
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
def STmensual(datos,tipoPD,nombrecolumnafecha,nombrecolumnavariable):
    df1=STdiarios(datos,tipoPD,nombrecolumnafecha,nombrecolumnavariable) #promedios diarios 
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
##############################################################################

# 4. PROCESOS 
# 4.1 Convertir la fecha en datatime y crear las columnas  de año, mes, día y hora.
datos[nombrecolumnafecha]=pd.to_datetime(datos[nombrecolumnafecha]) #conversión a datatime.
datos["year"]=pd.to_datetime(datos[nombrecolumnafecha]).dt.year  # crea una columna con los años.
datos["month"]=pd.to_datetime(datos[nombrecolumnafecha]).dt.month # crea una columna con los meses.
datos["day"]=pd.to_datetime(datos[nombrecolumnafecha]).dt.day  # crea una columna con los días.
datos["hour"]=pd.to_datetime(datos[nombrecolumnafecha]).dt.hour # crea una columna con los hora.
y=list(datos["year"].unique()) # se obtiene una lista de los años.
month=list(datos["month"].unique()) # se obtiene una lista de los meses.
d=list(datos["day"].unique()) # se obtiene una lista de los días.
h=list(datos["hour"].unique()) # se obtiene una lista de las horas.
h.sort()
d.sort()
month.sort()
y.sort()
##############################################################################
# 5. GRÁFICOS
print("################ 5. GRÁFICOS #########################")
print("")
print("Nota Importante 5: ")
print("* Los gráficos acumulados se permiten hacer en variables que se puedan acumular, por ejemplo la precipitación")
print("")
print("############### MENÚ ##########################")
print("SERIES DE TIEMPO \n")
print("1. Serie de tiempo de promedios horarios.")
print("2. Serie de tiempo de acumulados horarios.")
print("3. Serie de tiempo de Promedios diarios.")
print("4. Serie de tiempo de acumulados diarios.")
print("5. Serie de tiempo mensual con promedios diarios.")
print("6. Serie de tiempo mensual con acumulados diarios. \n")
print("CICLOS MEDIOS \n")
print("7. Ciclo medio diurno para un día particular (promedio).")
print("8. Ciclo medio diurno para un día particular (acumulado).")
print("9. Ciclo medio diurno de un mes particular (promedio).")
print("10. Ciclo medio diurno de un mes particular (acumulado).")
print("11. Ciclo medio anual - a intervalo diarios (promedio).")
print("12. Ciclo medio anual - a intervalo diarios (acumulado).")
print("13. Ciclo medio anual - a intervalo mensual (promedio).")
print("14. Ciclo medio anual - a intervalo mensual (acumulado). \n ")
print(" ANOMALÍAS \n")
print("15. Anomalías de la ST diaria (promedios)")
print("16. Anomalías de la ST diaria (acumulados)")
print("17. Anomalías de la ST mensual (promedios)")
print("18. Anomalías de la ST mensual (acumulados)")

continuar1="si"
while (continuar1 =="si"):
    r4_1=int(input("Ingrese el número del gráfico que desea obtener:"))
    if r4_1==1: #Serie de tiempo de promedios horarios.
        g1=SThorarios(datos,2,nombrecolumnafecha,nombrecolumnavariable) # Función 3.1
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g1,color="blue",label=(str(estacion)+"- g1"))
        plt.title(" Serie de tiempo de promedios horarios de "+ str(variable),fontsize=15)
        plt.ylabel( str(variable)+ " ["+str(unidades)+"]", fontsize=12)
        plt.xlabel("Tiempo (horas)",fontsize=12)
        plt.minorticks_on()
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:"))
        if guardarplt=="si":
            plt.savefig(dgra+"STPH_promedios_g1"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g1.to_csv(dcsv+"STPH_promedios_g1"+str(variable)+".csv",sep=";")
        del g1
    if r4_1==2: #Serie de tiempo de acumulados horarios
        g2=SThorarios(datos,1,nombrecolumnafecha,nombrecolumnavariable) #Función 3.1
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g2,color="blue",label=(str(estacion)+"- g2"))
        plt.title(" Serie de tiempo de acumulados horarios de "+ str(variable),fontsize=15)
        plt.ylabel( str(variable)+ "["+str(unidades)+"/horas]", fontsize=12)
        plt.xlabel("Tiempo (horas)",fontsize=12)
        plt.minorticks_on()
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
        if guardarplt=="si":
            plt.savefig(dgra+"STAH_acumulados_g2"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g2.to_csv(dcsv+"STAH_acumulados_g2"+str(variable)+".csv",sep=";")
        del g2
    if r4_1==3: #Serie de tiempo de promedios diarios.
        g3=STdiarios(datos,2,nombrecolumnafecha,nombrecolumnavariable) #Función 3.2
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g3.valor,color="purple",label=(str(estacion)+"- g3"))
        plt.title(" Serie de tiempo de promedios diarios de "+ str(variable),fontsize=15)
        plt.ylabel( str(variable)+ " ["+str(unidades)+"]", fontsize=12)
        plt.xlabel("Tiempo (días)",fontsize=12)
        plt.minorticks_on()
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
        if guardarplt=="si":
            plt.savefig(dgra+"STPD_promedios_g3"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g3.to_csv(dcsv+"STPD_promedios_g3"+str(variable)+".csv",sep=";")
        del g3
    if r4_1==4: #Serie de tiempo de acumulados diarios.
        g4=STdiarios(datos,1,nombrecolumnafecha,nombrecolumnavariable) #Función 3.2
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g4.valor,color="purple",label=(str(estacion)+"- g4"))
        plt.title(" Serie de tiempo de acumulados diarios de "+ str(variable),fontsize=15)
        plt.ylabel( str(variable)+ " ["+str(unidades)+"/días]", fontsize=12)
        plt.xlabel("Tiempo (días)",fontsize=12)
        plt.minorticks_on()
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
        if guardarplt=="si":
            plt.savefig(dgra+"STAD_acumulados_g4"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g4.to_csv(dcsv+"STAD_acumulados_g4"+str(variable)+".csv",sep=";")
        del g4
    if r4_1==5: #Serie de tiempo mensual con promedios diarios.
        g5=STmensual(datos,2,"fecha_observacion","valor_observado")# serie de tiempo mensual
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g5.fecha,g5.valor,color="palevioletred",label=(str(estacion)+"- g5"))
        plt.title(" Serie de tiempo mensual con promedios diarios de "+ str(variable),fontsize=15)
        plt.ylabel( str(variable)+ " ["+str(unidades)+"]", fontsize=12)
        plt.xlabel("Tiempo (meses)",fontsize=12)
        plt.minorticks_on()
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
        
        if guardarplt=="si":
            plt.savefig(dgra+"STPM_promedios_g5"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g5.to_csv(dcsv+"STPM_promedios_g5"+str(variable)+".csv",sep=";")   
    if r4_1==6: #Serie de tiempo mensual con acumulados diarios.
        g6=STmensual(datos,1,"fecha_observacion","valor_observado")# serie de tiempo mensual
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g6.fecha,g6.valor,color="palevioletred",label=(str(estacion)+"- g6"))
        plt.title(" Serie de tiempo mensual con acumulados diarios de "+ str(variable),fontsize=15)
        plt.ylabel( str(variable)+ " ["+str(unidades)+"/días]", fontsize=12)
        plt.xlabel("Tiempo (meses)",fontsize=12)
        plt.minorticks_on()
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
        if guardarplt=="si":
            plt.savefig(dgra+"STAM_acumulados_g6"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g6.to_csv(dcsv+"STAM_acumulados_g6"+str(variable)+".csv",sep=";")
    if r4_1==7: # Ciclo medio diurno para un día particular (promedio).
        continuar="si"
        while(continuar=="si"): 
            print(" Ingrese los valores acontinuación sin puntos y en números.")
            dia=int(input("¿Qué día quiere analizar?: "))
            mes=int(input("¿Qué mes quiere analizar?: "))
            g7=CMD_dia(dia,mes,y,datos,nombrecolumnavariable,nombrecolumnafecha,2)
            #gráfico
            fechatitulo=str(dia)+" de "+str(meses1[mes-1])
            plt.figure(figsize=(10,5))  
            plt.plot(g7.valor,color="teal",label=str(estacion)+" - g7")
            plt.title(" Ciclo Medio Diurno (promedios horarios) \n "+ str(variable)+" - "+ str(fechatitulo),fontsize=15)
            plt.ylabel( str(variable)+ " ["+str(unidades)+"]", fontsize=12)
            plt.xlabel("Tiempo (horas)",fontsize=12)
            plt.xticks(np.arange(0, 24, step=1))
            plt.minorticks_on()
            plt.legend()
            plt.grid()
            #pregunta para almacenamiento
            guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
            guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
            
            if guardarplt=="si":
                plt.savefig(dgra+"CMDparaundia_promedios_g7"+str(variable)+str(dia)+str(mes)+".png",dpi = 400)
            if guardarcsv=="si":
                g7.to_csv(dcsv+"CMDparaundia_promedios_g7"+str(variable)+str(dia)+str(mes)+".csv",sep=";")
            continuar=str(input("¿Desea realizar el gráfico en otra fecha? si/no: "))
    if r4_1==8: # Ciclo medio diurno para un día particular (acumulado).
        continuar="si"
        while(continuar=="si"):
            print(" Ingrese los valores acontinuación sin puntos y en números.")
            dia=int(input("¿Qué día quiere analizar?: "))
            mes=int(input("¿Qué mes quiere analizar?: "))
            g8=CMD_dia(dia,mes,y,datos,nombrecolumnavariable,nombrecolumnafecha,1)
            #gráfico
            fechatitulo=str(dia)+" de "+str(meses1[mes-1])
            plt.figure(figsize=(10,5))  
            plt.plot(g8.valor,color="teal",label=str(estacion)+" - g8")
            plt.title(" Ciclo Medio Diurno (acumulados horarios) \n "+ str(variable)+" - "+ str(fechatitulo),fontsize=15)
            plt.ylabel( str(variable)+ " ["+str(unidades)+"/horas]", fontsize=12)
            plt.xlabel("Tiempo (horas)",fontsize=12)
            plt.xticks(np.arange(0, 24, step=1))
            plt.minorticks_on()
            plt.legend()
            plt.grid()
            #pregunta para almacenamiento
            guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
            guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
            
            if guardarplt=="si":
                plt.savefig(dgra+"CMDparaundia_acumulados_g8"+str(variable)+str(dia)+str(mes)+".png",dpi = 400)
            if guardarcsv=="si":
                g8.to_csv(dcsv+"CMDparaundia_acumulados_g8"+str(variable)+str(dia)+str(mes)+".csv",sep=";")
            continuar=str(input("¿Desea realizar el gráfico en otra fecha? si/no: "))
    if r4_1==9: #Ciclo medio diurno de un mes particular (promedio).
        continuar="si"
        while(continuar=="si"):
            print(" Ingrese los valores acontinuación sin puntos y en números.")
            mes=int(input("¿Qué mes quiere analizar?: "))
            g9=CMD_mes(y,datos,mes,nombrecolumnavariable,nombrecolumnafecha,2)
            #gráfico
            fechatitulo=str(meses1[mes-1])
            plt.figure(figsize=(10,5))  
            plt.plot(g9,color="forestgreen",label=str(estacion)+ "-g9")
            plt.title(" Ciclo Medio Diurno (promedios horarios \n "+ str(variable)+" - "+ str(fechatitulo),fontsize=15)
            plt.ylabel( str(variable)+ "["+str(unidades)+"]", fontsize=12)
            plt.xlabel("Tiempo (horas)",fontsize=12)
            plt.xticks(np.arange(0, 24, step=1))
            plt.minorticks_on()
            plt.legend()
            plt.grid()
            #pregunta para almacenamiento
            guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
            guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
            if guardarplt=="si":
                plt.savefig(dgra+"CMDparaunmes_promedios_g9"+str(variable)+str(mes)+".png",dpi = 400)
            if guardarcsv=="si":
                g9.to_csv(dcsv+"CMDparaunmes_promedios_g9"+str(variable)+str(mes)+".csv",sep=";")
                del g9
            continuar=str(input("¿Desea realizar el gráfico en otra fecha? si/no: "))
    if r4_1==10: #Ciclo medio diurno de un mes particular (acumulado).
        continuar="si"
        while(continuar=="si"):
            print(" Ingrese los valores acontinuación sin puntos y en números.")
            mes=int(input("¿Qué mes quiere analizar?: "))
            g10=CMD_mes(y,datos,mes,nombrecolumnavariable,nombrecolumnafecha,1)
            #gráfico
            fechatitulo=str(meses1[mes-1])
            plt.figure(figsize=(10,5))  
            plt.plot(g10,color="forestgreen",label=str(estacion)+ "-g10")
            plt.title(" Ciclo Medio Diurno (acumulados horarios \n "+ str(variable)+" - "+ str(fechatitulo),fontsize=15)
            plt.ylabel( str(variable)+ " ["+str(unidades)+"/hora]", fontsize=12)
            plt.xlabel("Tiempo (horas)",fontsize=12)
            plt.xticks(np.arange(0, 24, step=1))
            plt.minorticks_on()
            plt.legend()
            plt.grid()
            #pregunta para almacenamiento
            guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
            guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
            if guardarplt=="si":
                plt.savefig(dgra+"CMDparaunmes_acumulados_g10"+str(variable)+str(mes)+".png",dpi = 400)
            if guardarcsv=="si":
                g10.to_csv(dcsv+"CMDparaunmes_acumulados_g10"+str(variable)+str(mes)+".csv",sep=";")
            del g10
            continuar=str(input("¿Desea realizar el gráfico en otra fecha? si/no: "))
    if r4_1==11: #Ciclo medio anual - a intervalo diarios (promedio)
        g11=CMA_dias(datos,2,nombrecolumnafecha,nombrecolumnavariable)
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g11.fecha,g11.valor,color="olive",label=(str(estacion)+"- g11"))
        plt.title(" Cliclo medio anual (promedios diarios) \n "+ str(variable),fontsize=15)
        plt.minorticks_on()
        plt.ylabel( str(variable)+ " ["+str(unidades)+"]", fontsize=12)
        plt.xlabel("Tiempo (días)",fontsize=12)
        #plt.xticks(np.arange(15, 365-15, step=30),labels=meses)
        plt.xticks(np.arange(15, 365-15, step=30))
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
        if guardarplt=="si":
            plt.savefig(dgra+"CMDdiarios_promedios_g11"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g11.to_csv(dcsv+"CMDdiarios_promedios_g11"+str(variable)+".csv",sep=";")
        del g11
    if r4_1==12: #Ciclo medio anual - a intervalo diarios (acumulado)
        g12=CMA_dias(datos,1,nombrecolumnafecha,nombrecolumnavariable)
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g12.fecha,g12.valor,color="olive",label=(str(estacion)+"- g12"))
        plt.title(" Cliclo medio anual (acumulados diarios) \n "+ str(variable),fontsize=15)
        plt.minorticks_on()
        plt.ylabel( str(variable)+ " ["+str(unidades)+"/días]", fontsize=12)
        plt.xlabel("Tiempo (días)",fontsize=12)
        #plt.xticks(np.arange(15, 365-15, step=30),labels=meses)
        plt.xticks(np.arange(15, 365-15, step=30))
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
        if guardarplt=="si":
            plt.savefig(dgra+"CMAdiarios_acumulados_g12"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g12.to_csv(dcsv+"CMAdiarios_acumulados_g12"+str(variable)+".csv",sep=";")
        del g12
    if r4_1==13: #Ciclo medio anual - a intervalo mensual (promedio).
        g13=CMA_mes(datos,2,nombrecolumnafecha,nombrecolumnavariable)
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g13.valor,color="mediumvioletred",label=(str(estacion)+"- g13"))
        plt.title(" Cliclo medio anual (mensual-promedios) \n "+ str(variable),fontsize=15)
        plt.ylabel( str(variable)+ " ["+str(unidades)+"]", fontsize=12)
        plt.xlabel("Tiempo (meses)",fontsize=12)
        plt.xticks(np.arange(0, 12, step=1),labels=meses)
        plt.minorticks_on()
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
        if guardarplt=="si":
            plt.savefig(dgra+"CMAmensual_promedios_g13"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g13.to_csv(dcsv+"CMAmensual_promedios_g13"+str(variable)+".csv",sep=";")
        del g13
    if r4_1==14: #Ciclo medio anual - a intervalo mensual (acumulado).
        g14=CMA_mes(datos,1,nombrecolumnafecha,nombrecolumnavariable)
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g14.valor,color="mediumvioletred",label=(str(estacion)+"- g14"))
        plt.title(" Cliclo medio anual (mensual-acumulado) \n "+ str(variable),fontsize=15)
        plt.ylabel( str(variable)+ " ["+str(unidades)+"/días]", fontsize=12)
        plt.xlabel("Tiempo (meses)",fontsize=12)
        plt.xticks(np.arange(1, 13, step=1),labels=meses)
        plt.minorticks_on()
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
        if guardarplt=="si":
            plt.savefig(dgra+"CMAmensual_acumulados_g14"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g14.to_csv(dcsv+"CMAmensual_acumulados_g14"+str(variable)+".csv",sep=";")
        del g14   
    if r4_1==15: #Anomalías ST diaria (promedios).
        g15=anomalias_dia(datos,2,"fecha_observacion","valor_observado")  #anomalias diarias
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g15.fecha,g15.valor,color="crimson",label=(str(estacion)+"- g15"))
        plt.title(" Anomalías ST diaria (promedios) \n "+ str(variable),fontsize=15)
        plt.axhline(y=0,color="k",linewidth=1.0,linestyle="--")
        plt.ylabel( str(variable)+ " ["+str(unidades)+"]", fontsize=12)
        plt.xlabel("Tiempo (días)",fontsize=12)
        plt.minorticks_on()
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
        if guardarplt=="si":
            plt.savefig(dgra+"AnomaliasD_promedios_g15"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g15.to_csv(dcsv+"AnomaliasD_promedios_g15"+str(variable)+".csv",sep=";")
        del g15
    if r4_1==16: #Anomalías ST diaria (acumulados).
        g16=anomalias_dia(datos,1,"fecha_observacion","valor_observado")  #anomalias diarias
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g16.fecha,g16.valor,color="crimson",label=(str(estacion)+"- g16"))
        plt.title(" Anomalías ST diaria (acumulados) \n "+ str(variable),fontsize=15)
        plt.axhline(y=0,color="k",linewidth=1.0,linestyle="--")
        plt.ylabel( str(variable)+ " ["+str(unidades)+"/dias]", fontsize=12)
        plt.xlabel("Tiempo (días)",fontsize=12)
        plt.minorticks_on()
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
        if guardarplt=="si":
            plt.savefig(dgra+"AnomaliasD_acumulados_g16"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g16.to_csv(dcsv+"AnomaliasD_acumulados_g16"+str(variable)+".csv",sep=";")
    if r4_1==17: #Anomalías ST mensual (promedios).
        g17=anomalias_mes(datos,2,"fecha_observacion","valor_observado") #anomalias mensuales
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g17.fecha,g17.valor,color="darkslategray",label=(str(estacion)+"- g17"))
        plt.title(" Anomalías ST mensual (promedios) \n "+ str(variable),fontsize=15)
        plt.axhline(y=0,color="k",linewidth=1.0,linestyle="--")
        plt.ylabel( str(variable)+ " ["+str(unidades)+"]", fontsize=12)
        plt.xlabel("Tiempo (meses)",fontsize=12)
        plt.minorticks_on()
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
        if guardarplt=="si":
            plt.savefig(dgra+"AnomaliasM_promedios_g17"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g17.to_csv(dcsv+"AnomaliasM_promedios_g17"+str(variable)+".csv",sep=";")
    if r4_1==18: #Anomalías ST mensual (acumulados).
        g18=anomalias_mes(datos,1,"fecha_observacion","valor_observado") #anomalias mensuales
        #gráfico
        plt.figure(figsize=(10,5))  
        plt.plot(g18.fecha,g18.valor,color="darkslategray",label=(str(estacion)+"- g18"))
        plt.title(" Anomalías ST mensual (acumulados) de "+ str(variable),fontsize=15)
        plt.axhline(y=0,color="k",linewidth=1.0,linestyle="--")
        plt.ylabel( str(variable)+ " ["+str(unidades)+"/días]", fontsize=12)
        plt.xlabel("Tiempo (meses)",fontsize=12)
        plt.minorticks_on()
        plt.legend()
        plt.grid()
        #pregunta para almacenamiento
        guardarplt=str(input("¿Desea Guardar el gráfico? si/no:"))
        guardarcsv=str(input("¿Desea Guardar la informacion de salida? si/no:")) 
        if guardarplt=="si":
            plt.savefig(dgra+"AnomaliasM_acumulados_g18"+str(variable)+".png",dpi = 400)
        if guardarcsv=="si":
            g18.to_csv(dcsv+"AnomaliasM_acumulados_g18"+str(variable)+".csv",sep=";")
    continuar1=str(input("¿Desea realizar otros graficos? si/no: "))
    




