#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 19:14:21 2022

@author: luisa
"""
####################### 1. LIBRERIAS #######################
import streamlit as st
import pandas as pd                  # Análisis de los datos  
from sqlalchemy import create_engine # Conexión con la base de datos
import plotly.express as px
import matplotlib.pyplot as plt    #Para graficar.
from tqdm import tqdm              # librería para saber el tiempo de ejecución.
import  numpy as np
####################### 2. DATOS #######################
##  Base de datos de Postgresql
#eng = "postgresql://lucy:usuario@localhost:5432/alejandria"
eng = "postgresql://luisa:000000@localhost:5432/alejandria" #Motor.
engine = create_engine(eng)                                 #Máquina.
conn=engine.connect()                                       #Conexión.
datos=[]
####################### 3. TITULO Y NOTAS INICIALES #######################
st.title("Base de datos Alejandría") # Titulo       
st.sidebar.header("**IMPORTANTE**")
#Nota 1
st.sidebar.write("""
               *Nota 1:Este sitio es producido con fines netamente acádemicos, los datos han sido tomados 
              de la pagina web <a href='https://www.datos.gov.co/'> Datos Abiertos</a> .
              Por lo tanto no nos hacemos responsables del uso que usted le dé a la información.
              para mayor información ingrese a las páginas compartidas.*
              """, unsafe_allow_html=True)
#Nota 2
st.sidebar.write(""" *NOTA 2: Se solicita a cualquier persona que haga uso de los datos aquí
                 contenidos, otorgar el debido reconocimiento a las estudiantes de la Universidad
                 de Antioquia Luisa Fernanda Buriticá Ruiz y Marcela Echeverri Gallego 
                 por su trabajo en la creación y automatización de la base de datos Alejandría.* """)
st.sidebar.markdown("---")
####################### 4. SELECCION DE COLUMNAS #######################
nav = st.sidebar.radio("",["Conjunto de Datos","Gráficos por estación"]) #Para seleccionar otras busquedas

if nav== "Conjunto de Datos":
    st.sidebar.header(" Filtros") # Titulo de filtros
    #Nombre de columnas
    df = pd.DataFrame(['Valor Observado','Fecha de Observación','Codigo de Estación','Nombre de Estación'
                       ,'Departamento','Municipio','Categoria','Tecnología','Estado','Altitud','Latitud'
                       ,'Longitud','Zona Hidrográfica','Unidad de Medida'])
    # Búsquedas
    columns = st.sidebar.multiselect("Seleccione las columnas de información que desea obtener",
                                     ['Valor Observado','Fecha de Observación','Codigo de Estación'
                                      ,'Nombre de Estación','Departamento','Municipio','Categoria',
                                      'Tecnología','Estado','Altitud','Latitud','Longitud','Zona Hidrográfica',
                                      'Unidad de Medida'])
    col = ''                    #Se inicia la variable
    a = df[0].isin(columns)     #Selección de columnas para busqueda.
    
    for i in range(len(a)):     #Agregar todas las columnas que se quiera agregar
        if a[i] == True:
            if df[0][i] == 'Valor Observado':
                col +='valor_observado,'
            if df[0][i] == 'Fecha de Observación':
                col +='fecha_observacion,'
            if df[0][i] == 'Codigo de Estación':
                col +='cod_estacion'
            if df[0][i] == 'Nombre de Estación':
                col +='nombre_estacion,'
            if df[0][i] == 'Departamento':
                col +='nombre_departamento,'
            if df[0][i] == 'Municipio':
                col +='nombre_municipio,'
            if df[0][i] == 'Categoria':
                col +='nombre_categoria,'
            if df[0][i] == 'Tecnología':
                col +='nombre_tecnologia,'
            if df[0][i] == 'Altitud':
                col +='altitud,'
            if df[0][i] == 'Estado':
                col +='nombre_estado,'
            if df[0][i] == 'Latitud':
                col +='latitud,'
            if df[0][i] == 'Longitud':
                col +='longitud,'
            if df[0][i] == 'Zona Hidrográfica':
                col +='nombre_zonahidrografica,'
            if df[0][i] == 'Unidad de Medida':
                col +='unidad_medida,'
    col = col[:-1]    #PREGUNTAR A MARCELA SOBRE ESTO, PARA QUÉ SIRVE
    # El Query a continuación permite la busqueda en todas las tablas
    query='''
    SELECT {}
    FROM observacion 
    INNER JOIN estacion USING(cod_estacion)
    INNER JOIN municipio USING(cod_municipio)
    INNER JOIN departamento USING(cod_departamento)
    INNER JOIN categoria USING(cod_categoria)
    INNER JOIN tecnologia USING(cod_tecnologia)
    INNER JOIN estado USING(cod_estado)
    INNER JOIN zonahidrografica USING(cod_zonahidrografica)
    INNER JOIN variable USING(cod_variable)
    '''.format(col)
    
    ####################### 5. SELECCIÓN DE VARIABLES #######################
    
    #Caja de selección para activar la opción de agregar varias variables
    v = st.sidebar.checkbox("Búsquedas por variables meteorológicas")
    variable=0
    if v==True:
        variable=st.sidebar.multiselect("seleccione la variable ",
                          ["Temperatura","Precipitación","Presión","Dirección del viento",
                           "Velocidad del viento"])
        if len(variable) >=1:
            if query.find('WHERE') == -1:
                query+='WHERE '
            else:
                query+= 'AND '
        
        if "Temperatura" in variable:
            query += 'cod_variable = 1 OR '
        if "Precipitación" in variable:
            query += 'cod_variable = 2 OR '
        if "Presión" in variable:
            query += 'cod_variable = 3 OR '
        if  "Dirección del viento" in variable:
            query += 'cod_variable = 4 OR' 
        if  "Velocidad del viento" in variable:
            query += 'cod_variable = 5 OR '
    
        if len(variable) >=1:
            query = query[:-3]
    
    f = st.sidebar.checkbox("Búsquedas por fecha")
    
    if f == True:
        
        if query.find('WHERE') == -1:
            query+='WHERE '
        else:
            query+= 'AND '
            
        fi=st.sidebar.date_input("Ingrese la fecha inicial:")
        ff=st.sidebar.date_input("Ingrese la fecha final:")
        
        query += ''' fecha_observacion < '{}' AND fecha_observacion >= '{}'
        '''.format(ff,fi)    
          
    if nav == "Conjunto de Datos":
        st.header("Conjunto de datos seleccionado")
        
        if st.sidebar.button('Buscar'):
    
            data= pd.read_sql(query,con=eng)
        
            csv = data.to_csv().encode('utf-8')
            st.dataframe(data)
            st.download_button(
             label="Descargar",
             data=csv,
             file_name='Datos.csv',
             mime='text/csv',
        )
        
            if len(col) >=1:
                st.success(query)
                
        st.sidebar.markdown('---')
if nav== "Gráficos por estación":
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
    
    # Vectores de entrada.
    meses=["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"] #meses para gráficos
    meses1=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre",
            "Octubre","Noviembre","Diciembre"] # meses para gráficos
    nombrecolumnafecha="fecha_observacion"
    nombrecolumnavariable="valor_observado"
    
    #ESTACIÓN
    #QUERY 1
    query1='''
    select cod_estacion from estacion
    '''
    df1=pd.read_sql(query1,con=eng)
    est=st.sidebar.selectbox("Seleccione una estación",df1)
    #VARIABLE
    variable = st.sidebar.selectbox("Selección de variable",["1. Dirección del viento","2. Precipitación",
                                                          "3. Presión", "4. Temperatura"
                                                          ,"5. Velocidad del viento"])
    if variable == "1. Dirección del viento":
        var=4
        variable1="Dirección del viento"
    if variable == "2. Precipitación":
        var=2
        variable1="Precipitación"
    if variable == "3. Presión":
        var=3
        variable1="Presión"
    if variable == "4. Temperatura":
        var=1
        variable1="Temperatura"
    if variable == "5. Velocidad del viento":
        var=5
        variable1="Velocidad del viento"
    st.session_state['variable'] = variable1 # Variable de estado 1 
    
    #QUERY 2
    query2='''
    select valor_observado,observacion.cod_estacion, fecha_observacion
    from observacion where cod_variable={} and cod_estacion ={}
    '''.format(var,est)
    #QUERY 3
    query3='''
    select unidad_medida from variable
    where cod_variable={}
    '''.format(var)
    
    if st.sidebar.button('Buscar'):

        datos=pd.read_sql(query2,con=eng)
        unidadesbusqueda=pd.read_sql(query3,con=eng)
        unidades=unidadesbusqueda["unidad_medida"][0]
        #Convertir la fecha en datatime y crear las columnas  de año, mes, día y hora.
        datos[nombrecolumnafecha]=pd.to_datetime(datos[nombrecolumnafecha]) #conversión a datatime.
        datos["year"]=pd.to_datetime(datos[nombrecolumnafecha]).dt.year  # crea una columna con los años.
        datos["month"]=pd.to_datetime(datos[nombrecolumnafecha]).dt.month # crea una columna con los meses.
        datos["day"]=pd.to_datetime(datos[nombrecolumnafecha]).dt.day  # crea una columna con los días.
        datos["hour"]=pd.to_datetime(datos[nombrecolumnafecha]).dt.hour # crea una columna con los hora.
        st.session_state['vectordatos'] = datos # Variable de estado 2
        st.session_state['unidades'] = unidades # Varible de estado 3
        
        st.write ("Datos de la estación"+str(est),datos.head())
        csv = datos.to_csv().encode('utf-8')
        st.download_button(
         label="Descargar",
         data=csv,
         file_name='Datos.csv',
         mime='text/csv')
        
        #A continuación se crea una variable de estado que sirve para conservar un valor cuando la 
        # página se refresca (carga de nuevo) > postback
        
    ##############################################################################
    # 5. GRÁFICOS
    
    #En el siguiente if se comprueba si existe datos y sí existe entonces comprueba si el 
    # valor es 1.
    if 'vectordatos' in st.session_state and len(st.session_state['vectordatos']) != 0:  
        
        menugraficos=["1. Serie de tiempo de promedios horarios.",
                      "2. Serie de tiempo de acumulados horarios.",
                      "3. Serie de tiempo de Promedios diarios."
                      ,"4. Serie de tiempo de acumulados diarios."
                      ,"5. Serie de tiempo mensual con promedios diarios."
                      ,"6. Serie de tiempo mensual con acumulados diarios."
                      ,"7. Ciclo medio diurno para un día particular (promedio)."
                      ,"8. Ciclo medio diurno para un día particular (acumulado)."
                      ,"9. Ciclo medio diurno de un mes particular (promedio)."
                      ,"10. Ciclo medio diurno de un mes particular (acumulado)."
                      ,"11. Ciclo medio anual - a intervalo diarios (promedio)."
                      ,"12. Ciclo medio anual - a intervalo diarios (acumulado)."
                      ,"13. Ciclo medio anual - a intervalo mensual (promedio)."
                      ,"14. Ciclo medio anual - a intervalo mensual (acumulado)."
                      ,"15. Anomalías de la ST diaria (promedios)."
                      ,"16. Anomalías de la ST diaria (acumulados)."
                      ,"17. Anomalías de la ST mensual (promedios)."
                      ,"18. Anomalías de la ST mensual (acumulados)."
                      ]
        r4_1=st.selectbox("Seleccione un gráfico: ",menugraficos)
        datos=st.session_state['vectordatos']
        unidades=st.session_state['unidades']
        variable1=st.session_state['variable']
        
        y=list(datos["year"].unique()) # se obtiene una lista de los años.
        month=list(datos["month"].unique()) # se obtiene una lista de los meses.
        d=list(datos["day"].unique()) # se obtiene una lista de los días.
        h=list(datos["hour"].unique()) # se obtiene una lista de las horas.
        h.sort()
        d.sort()
        month.sort()
        y.sort()
        st.write("Cantidad de datos disponibles: ", len(datos))
        st.write("Unidades: ", unidades)
        st.write("Nombre de la variable: ",variable1 )
        if st.button('Generar'):
            
            if r4_1=="1. Serie de tiempo de promedios horarios.": #Serie de tiempo de promedios horarios.
                g1=SThorarios(datos,2,nombrecolumnafecha,nombrecolumnavariable) # Función 3.1
                #gráfico
                fig =plt.figure(figsize=(10,5))  
                plt.plot(g1,color="blue",label=(str(est)+"- g1"))
                plt.title(" Serie de tiempo de promedios horarios de "+ str(variable1),fontsize=15)
                plt.ylabel( str(variable1)+ " ["+str(unidades)+"]", fontsize=12)
                plt.xlabel("Tiempo (horas)",fontsize=12)
                plt.minorticks_on()
                plt.legend()
                plt.grid()
                st.pyplot(fig)
            if r4_1=="2. Serie de tiempo de acumulados horarios.": #Serie de tiempo de acumulados horarios
                g2=SThorarios(datos,1,nombrecolumnafecha,nombrecolumnavariable) #Función 3.1
                #gráfico
                fig=plt.figure(figsize=(10,5))  
                plt.plot(g2,color="blue",label=(str(est)+"- g2"))
                plt.title(" Serie de tiempo de acumulados horarios de "+ str(variable1),fontsize=15)
                plt.ylabel( str(variable1)+ "["+str(unidades)+"/horas]", fontsize=12)
                plt.xlabel("Tiempo (horas)",fontsize=12)
                plt.minorticks_on()
                plt.legend()
                plt.grid()
                st.pyplot(fig)
            if r4_1=="3. Serie de tiempo de Promedios diarios.": #Serie de tiempo de promedios diarios.
                g3=STdiarios(datos,2,nombrecolumnafecha,nombrecolumnavariable) #Función 3.2
                #gráfico
                fig=plt.figure(figsize=(10,5))  
                plt.plot(g3.valor,color="purple",label=(str(est)+"- g3"))
                plt.title(" Serie de tiempo de promedios diarios de "+ str(variable1),fontsize=15)
                plt.ylabel( str(variable1)+ " ["+str(unidades)+"]", fontsize=12)
                plt.xlabel("Tiempo (días)",fontsize=12)
                plt.minorticks_on()
                plt.legend()
                plt.grid()
                st.pyplot(fig)
                
            if r4_1=="4. Serie de tiempo de acumulados diarios.": #Serie de tiempo de acumulados diarios.
                g4=STdiarios(datos,1,nombrecolumnafecha,nombrecolumnavariable) #Función 3.2
                #gráfico
                fig=plt.figure(figsize=(10,5))  
                plt.plot(g4.valor,color="purple",label=(str(est)+"- g4"))
                plt.title(" Serie de tiempo de acumulados diarios de "+ str(variable1),fontsize=15)
                plt.ylabel( str(variable1)+ " ["+str(unidades)+"/días]", fontsize=12)
                plt.xlabel("Tiempo (días)",fontsize=12)
                plt.minorticks_on()
                plt.legend()
                plt.grid()
                st.pyplot(fig)
            if r4_1=="5. Serie de tiempo mensual con promedios diarios.": #Serie de tiempo mensual con promedios diarios.
                g5=STmensual(datos,2,"fecha_observacion","valor_observado")# serie de tiempo mensual
                #gráfico
                fig=plt.figure(figsize=(10,5))  
                plt.plot(g5.fecha,g5.valor,color="palevioletred",label=(str(est)+"- g5"))
                plt.title(" Serie de tiempo mensual con promedios diarios de "+ str(variable1),fontsize=15)
                plt.ylabel( str(variable1)+ " ["+str(unidades)+"]", fontsize=12)
                plt.xlabel("Tiempo (meses)",fontsize=12)
                plt.minorticks_on()
                plt.legend()
                plt.grid()
                st.pyplot(fig)   
            if r4_1=="6. Serie de tiempo mensual con acumulados diarios.": #Serie de tiempo mensual con acumulados diarios.
                g6=STmensual(datos,1,"fecha_observacion","valor_observado")# serie de tiempo mensual
                #gráfico
                fig=plt.figure(figsize=(10,5))  
                plt.plot(g6.fecha,g6.valor,color="palevioletred",label=(str(est)+"- g6"))
                plt.title(" Serie de tiempo mensual con acumulados diarios de "+ str(variable1),fontsize=15)
                plt.ylabel( str(variable1)+ " ["+str(unidades)+"/días]", fontsize=12)
                plt.xlabel("Tiempo (meses)",fontsize=12)
                plt.minorticks_on()
                plt.legend()
                plt.grid()
                st.pyplot(fig)
                
            
        
            
    
    
            
                
                
                
   
    

                                                      