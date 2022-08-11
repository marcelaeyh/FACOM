
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 19:14:21 2022

@author: luisa
"""
import streamlit as st
import pandas as pd                  # Análisis de los datos  
from sqlalchemy import create_engine # Conexión con la base de datos
import plotly.express as px

## 2.1 Base de datos de Postgresql

eng = "postgresql://lucy:usuario@localhost:5432/alejandria"

#eng = "postgresql://luisa:000000@localhost:5432/alejandria" #Motor.
engine = create_engine(eng)                                 #Máquina.
conn=engine.connect()                                       #Conexión.

st.title("Base de datos Alejandría")


st.sidebar.header("IMPORTANTE")
                  
st.sidebar.write("""
               Nota 1: Este sitio es producido con fines netamente acádemicos, los datos han sido tomados 
              de la pagina web <a href='https://www.datos.gov.co/'> Datos Abiertos</a> .
              Por lo tanto no nos hacemos responsables del uso que ustede le dé a la información.
              para mayor información ingrese a las páginas compartidas.
              """,
              unsafe_allow_html=True)
  

st.sidebar.markdown("---")
st.sidebar.write(" \n NOTA 2: \n Se solicita a cualquier persona que haga uso de los datos aquí contenidos, otorgar el debido reconocimiento a las estudiantes de la Universidad de Antioquia Luisa Fernanda Buriticá Ruiz y Marcela Echeverri Gallego por su trabajo en la creación y automatización de la base de datos alejandría.")
st.sidebar.markdown("---")

st.sidebar.header("Seleccione el formato en que desea ver los datos")
nav = st.sidebar.radio("",["Conjunto de Datos","Gráficos por estación"])

st.sidebar.header("Filtros")
st.sidebar.markdown("---")

if nav == "Conjunto de Datos":
    st.header("Conjunto de datos seleccionado")
    variable=st.sidebar.selectbox("seleccione la variable ",
                  ["Temperatura","Precipitación","Presión","Dirección del viento","Velocidad del viento"])
    
    if variable == "Temperatura":
        var=1
        variable1="Temperatura [°C]"
    if variable == "Precipitación":
        var=2
        variable1="Precipitación [mm]"
    if variable == "Presión":
        var=3
        variable1="Presión [hpa]"
    if variable == "Dirección del viento":
        var=4
        variable1="Dirección del viento [grados]"
    if variable == "Velocidad del viento":
        var=5
        variable1="Velocidad del viento [m/s]"
    
    fi=st.sidebar.date_input("Ingrese la fecha inicial:")
    ff=st.sidebar.date_input("Ingrese la fecha final:")
    
    query='''
    select valor_observado,fecha_observacion,cod_estacion
    from observacion where cod_variable={} and 
    fecha_observacion < '{}' and fecha_observacion >= '{}'
    '''.format(var,ff,fi)
    data= pd.read_sql(query,con=eng)
    
    csv = data.to_csv().encode('utf-8')
    st.dataframe(data)
    st.download_button(
     label="Descargar",
     data=csv,
     file_name='Datos.csv',
     mime='text/csv',
 )
    
if nav == "Gráficos por estación":
    st.header("Conjunto de gráficos de la estación seleccionada")

    seriet = st.checkbox("Serie de tiempo para una variable")
    
    variable=st.sidebar.selectbox("seleccione la variable ",
                      ["Temperatura","Precipitación","Presión","Dirección del viento","Velocidad del viento"])
    estacion =int(st.sidebar.number_input("Ingrese la estación: "))
    st.sidebar.write("Su estación es: ",estacion)
    print(str(estacion))
    
    
    if variable == "Temperatura":
        var=1
        variable1="Temperatura [°C]"
    if variable == "Precipitación":
        var=2
        variable1="Precipitación [mm]"
    if variable == "Presión":
        var=3
        variable1="Presión [hpa]"
    if variable == "Dirección del viento":
        var=4
        variable1="Dirección del viento [grados]"
    if variable == "Velocidad del viento":
        var=5
        variable1="Velocidad del viento [m/s]"
    
    fi=st.sidebar.date_input("Ingrese la fecha inicial:")
    ff=st.sidebar.date_input("Ingrese la fecha final:")
    
    query='''
    select valor_observado,fecha_observacion
    from observacion where cod_variable={} and cod_estacion ={} and 
    fecha_observacion < '{}' and fecha_observacion >= '{}'
    '''.format(var,estacion,ff,fi)
    data= pd.read_sql(query,con=eng)
    
    if(len(data)==0):
        st.write("Error, la estación no tiene datos de esa variable", fontzise=30)
    
    if (len(data)!=0):  
        if seriet == True:
            data= data.sort_values(by="fecha_observacion")
            data=data.rename(columns={"fecha_observacion":'Hora Local', "valor_observado":str(variable1)})
        
            fig = px.line(data, x = "Hora Local", y = str(variable1), title = "Serie de tiempo")
            st.plotly_chart(fig)

