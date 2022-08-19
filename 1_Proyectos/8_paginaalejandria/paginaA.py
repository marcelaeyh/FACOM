
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
              Por lo tanto no nos hacemos responsables del uso que usted le dé a la información.
              para mayor información ingrese a las páginas compartidas.
              """,
              unsafe_allow_html=True)
  

st.sidebar.markdown("---")
st.sidebar.write(" \n NOTA 2: \n Se solicita a cualquier persona que haga uso de los datos aquí contenidos, otorgar el debido reconocimiento a las estudiantes de la Universidad de Antioquia Luisa Fernanda Buriticá Ruiz y Marcela Echeverri Gallego por su trabajo en la creación y automatización de la base de datos Alejandría.")
st.sidebar.markdown("---")

st.sidebar.header("Seleccione el formato en que desea ver los datos")
nav = st.sidebar.radio("",["Conjunto de Datos","Gráficos por estación"])

st.sidebar.header("Filtros")
st.sidebar.markdown("---")
df = pd.DataFrame(['Valor Observado','Fecha de Observación',
 'Codigo de Estación','Nombre de Estación','Departamento',
 'Municipio','Categoria','Tecnología','Estado','Altitud',
 'Latitud','Longitud','Zona Hidrográfica','Unidad de Medida'])

# Búsquedas
columns = st.sidebar.multiselect("Seleccione las columnas de información que desea obtener",
                                 ['Valor Observado','Fecha de Observación',
                                  'Codigo de Estación','Nombre de Estación','Departamento',
                                  'Municipio','Categoria','Tecnología','Estado','Altitud',
                                  'Latitud','Longitud','Zona Hidrográfica','Unidad de Medida'])
col = ''
a = df[0].isin(columns)

for i in range(len(a)):
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

col = col[:-1]

v = st.sidebar.checkbox("Búsquedas por variables meteorológicas")

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


if v==True:
    variable=st.sidebar.multiselect("seleccione la variable ",
                      ["Temperatura","Precipitación","Presión","Dirección del viento","Velocidad del viento"])
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

