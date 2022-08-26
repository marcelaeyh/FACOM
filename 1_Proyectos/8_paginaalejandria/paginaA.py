
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
####################### 2. DATOS #######################
##  Base de datos de Postgresql
eng = "postgresql://lucy:usuario@localhost:5432/alejandria"
#eng = "postgresql://luisa:000000@localhost:5432/alejandria" #Motor.
engine = create_engine(eng)                                 #Máquina.
conn=engine.connect()                                       #Conexión.
####################### 3. TITULO Y NOTAS INICIALES #######################
st.title("Base de datos Alejandría") # Titulo       
st.sidebar.header("**IMPORTANTE**")
#Nota 1
st.sidebar.write("""
               *NOTA 1:Este sitio es producido con fines netamente acádemicos, los datos han sido tomados 
              de la pagina web <a href='https://www.datos.gov.co/'> Datos Abiertos</a> .
              Por lo tanto no nos hacemos responsables del uso que usted le dé a la información.
              para mayor información ingrese a las páginas compartidas.*
              """, unsafe_allow_html=True)
st.sidebar.markdown("---")
#Nota 2
st.sidebar.write(""" *NOTA 2: Se solicita a cualquier persona que haga uso de los datos aquí
                 contenidos, otorgar el debido reconocimiento a las estudiantes de la Universidad
                 de Antioquia Luisa Fernanda Buriticá Ruiz y Marcela Echeverri Gallego 
                 por su trabajo en la creación y automatización de la base de datos Alejandría.* """)
st.sidebar.markdown("---")
#Nota 3
st.sidebar.write(""" *NOTA 3: Si realiza una búsqueda que contenga una gran cantidad de datos, en el 
                 conjunto solo podrá ver una vista previa de 100 filas, sin embargo, al descargar el 
                 archivo csv tendrá la información completa.*""")
st.sidebar.markdown("---")
####################### 4. SELECCION DE COLUMNAS #######################
nav = st.sidebar.radio("",["Conjunto de Datos","Gráficos por estación"]) #Para seleccionar otras busquedas


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

ver=0 # Verificación de codigo estacion (sirve para hacer los gráficos)

for i in range(len(a)):     #Agregar todas las columnas que se quiera agregar
    if a[i] == True:
        if df[0][i] == 'Valor Observado':
            col +='valor_observado,'
        if df[0][i] == 'Fecha de Observación':
            col +='fecha_observacion,'
        if df[0][i] == 'Codigo de Estación':
            col +='cod_estacion,'
            ver = 1
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
col = col[:-1]    #PREGUNTAR A MARCELA SOBRE ESTO, PARA QUÉ SIRVE - Quita la ultima coma :)
# El Query a continuación permite la busqueda en todas las tablas
query='''
SELECT cod_variable, {}
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
data = pd.DataFrame()
#Caja de selección para activar la opción de agregar varias variables

v = st.sidebar.checkbox("Búsquedas por variables meteorológicas")
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
        variable1="Temperatura [°C]"
    if "Precipitación" in variable:
        query += 'cod_variable = 2 OR '
        variable1="Precipitación [mm]"
    if "Presión" in variable:
        query += 'cod_variable = 3 OR '
        variable1="Presión [hpa]"
    if  "Dirección del viento" in variable:
        query += 'cod_variable = 4 OR' 
        variable1="Dirección del viento [grados]"
    if  "Velocidad del viento" in variable:
        query += 'cod_variable = 5 OR '
        variable1="Velocidad del viento [m/s]"

    if len(variable) >=1:
        query = query[:-3]

# filtros por fecha
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
    
# Seleccionar una estación en particular
es = st.sidebar.checkbox("Búsquedas por estación")

if es == True:
    qq='''
    SELECT DISTINCT cod_estacion FROM estacion
    '''
    estac = pd.read_sql(qq,con=eng)
    estacion = st.sidebar.selectbox('Seleccione el código de la estación deseada',estac['cod_estacion'])
    
    if query.find('WHERE') == -1:
        query+='WHERE '
    else:
        query+= 'AND '
        
    query += 'cod_estacion = {}'.format(estacion)

# Buscar por departamento
dep = st.sidebar.checkbox("Búsquedas por Departamento")

if dep == True:
    qq='''
    SELECT DISTINCT nombre_departamento FROM departamento 
    ORDER BY nombre_departamento
    '''
    depa = pd.read_sql(qq,con=eng)
    departamento = st.sidebar.selectbox('Seleccione el Departamento deseado',depa['nombre_departamento'])
    
    if query.find('WHERE') == -1:
        query+='WHERE '
    else:
        query+= 'AND '
        
    query += " nombre_departamento = '{}' ".format(departamento)

# Buscar por municipio
mun = st.sidebar.checkbox("Búsquedas por Municipio")

if mun == True:
    if dep == True:
        qq='''
        SELECT DISTINCT nombre_municipio FROM municipio 
        INNER JOIN departamento USING(cod_departamento)
        WHERE nombre_departamento = '{}'
        ORDER BY nombre_municipio
        '''.format(departamento)
    else:
        qq='''
        SELECT DISTINCT nombre_municipio FROM municipio 
        ORDER BY nombre_municipio
        '''
        
    muni = pd.read_sql(qq,con=eng)
    municipio = st.sidebar.selectbox('Seleccione el Municipio deseado',muni['nombre_municipio'])
    
    if query.find('WHERE') == -1:
        query+='WHERE '
    else:
        query+= 'AND '
        
    query += " nombre_municipio = '{}'".format(municipio)

# Buscar por Categoria
cat = st.sidebar.checkbox("Búsquedas por Categoría")

if cat == True:
    qq='''
    SELECT DISTINCT nombre_categoria FROM categoria 
    ORDER BY nombre_categoria
    '''
    cate = pd.read_sql(qq,con=eng)
    categoria = st.sidebar.selectbox('Seleccione la Categoría deseada ',cate['nombre_categoria'])
    
    if query.find('WHERE') == -1:
        query+='WHERE '
    else:
        query+= 'AND '
        
    query += " nombre_categoria = '{}' ".format(categoria)
    
# Buscar por Estado
est = st.sidebar.checkbox("Búsquedas por Estado")

if est == True:
    qq='''
    SELECT DISTINCT nombre_estado FROM estado 
    ORDER BY nombre_estado
    '''
    esta = pd.read_sql(qq,con=eng)
    estado = st.sidebar.selectbox('Seleccione el Estado deseado ',esta['nombre_estado'])
    
    if query.find('WHERE') == -1:
        query+='WHERE '
    else:
        query+= 'AND '
        
    query += " nombre_estado = '{}' ".format(estado)
    
if st.sidebar.button('Buscar'):
    query += ' LIMIT 200'
    data= pd.read_sql(query,con=eng)
    
    #Guarda toda información para tenerla disponible para hacer graficos
    data.to_csv(r'/home/marcelae/Desktop/FACOM/1_Proyectos/8_paginaalejandria/data.csv')
    
st.sidebar.markdown('---')     
# Opciones de visualización de los datos

if nav == "Conjunto de Datos":
    
    st.header("Conjunto de datos seleccionado")
    
    csv = data.to_csv().encode('utf-8')
    if len(data) >= 100:
        st.dataframe(data[:100])
    else:
        st.dataframe(data)
    st.write('Cantidad de datos',len(data))
    st.download_button(
     label="Descargar",
     data=csv,
     file_name='Datos.csv',
     mime='text/csv',
)
    if len(col) >=1:
        st.success(query)
    

    
if nav == "Gráficos por estación":
    if ver == 1 or es == True:
        st.header("Conjunto de gráficos de la estación seleccionada")

        variable=st.selectbox("Seleccione las variables que desea gráficar de su conjunto de datos filtrado",
                          variable)
        
        datas = pd.read_csv('/home/marcelae/Desktop/FACOM/1_Proyectos/8_paginaalejandria/data.csv')
        # Seleccionar una estación en particular (si no la seleccionó antes)
        if es != True:
            estac = datas['cod_estacion'].unique()
            estacion1 = st.selectbox('Seleccione el código de la estación deseada',estac)

            g = datas[datas['cod_estacion'] == estacion1]
            
        else:
            st.write("La estación seleccionada es:")
            st.write(estacion)
            g = datas
        
        st.write("Tipos de gráficos")
        seriet = st.checkbox("Series de tiempo")
        
        if "Temperatura" in variable:
            grafico = g[g['cod_variable'] == 1]
        if "Precipitación" in variable:
            grafico = g[g['cod_variable'] == 2]
        if "Presión" in variable:
            grafico = g[g['cod_variable'] == 3]
        if  "Dirección del viento" in variable:
            grafico = g[g['cod_variable'] == 4]
        if  "Velocidad del viento" in variable:
            grafico = g[g['cod_variable'] == 5]
            
        if(len(grafico)==0):
            st.write("Error, la estación no tiene datos de esa variable en su conjunto de datos", fontzise=30)
        
        if (len(grafico)!=0):  
            if seriet == True:
                grafico= grafico.sort_values(by="fecha_observacion")
                grafico=grafico.rename(columns={"fecha_observacion":'Hora Local', "valor_observado":str(variable1)})
            
                fig = px.line(grafico, x = "Hora Local", y = str(variable1), title = "Serie de tiempo")
                st.plotly_chart(fig)
    
    else:
        st.write("Debe seleccionar la columna 'Código de Estación' o Filtrar los datos por estación para usar este recurso")