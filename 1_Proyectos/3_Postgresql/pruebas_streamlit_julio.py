#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 11:10:05 2022

@author: marcelae
"""

import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static
from sodapy import Socrata
from datetime import date, timedelta, datetime

def func_datetime(x):
    try:
        return datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f')
    except:
        return pd.NaT
    
def corr_format(y):
    dk = y
    dk['fecha'] = dk['fechaobservacion'].apply(func_datetime)
    dk['fecha'] = pd.to_datetime(dk['fecha'])
    dk['codigoestacion'] = dk['codigoestacion'].astype(float)
    dk['valorobservado'] = dk['valorobservado'].astype(float)
    dk['latitud'] = dk['latitud'].astype(float)
    dk['longitud'] = dk['longitud'].astype(float)
    dk = dk[['fecha','nombreestacion','latitud','longitud','valorobservado','descripcionsensor','unidadmedida','codigoestacion','departamento','municipio']]
    dk.sort_values(by='fecha', inplace=True)

    #dk = dk[dk['codigoestacion']==15075501]
    return dk

#client = Socrata("www.datos.gov.co", None)
client = Socrata("www.datos.gov.co", 
                "ymgH2QpK9Z5cSKBNlKgtuzWZP", 
                username="esteban.silvav@udea.edu.co", 
                password="Nomeacuerdodatosabiertos_1")

st.set_page_config(layout ="wide")
json1 = f"Colombia.geo.json"

choice = ['CodigoEstacion','CodigoSensor','FechaObservacion','ValorObservado',
          'NombreEstacion','Departamento','Municipio','ZonaHidrografica','Latitud',
          'Longitud','DescripcionSensor','UnidadMedida']

catal = ['sbwg-7ju4','s54a-sgyg','62tk-nxj5']

choice_selected = st.selectbox("Seleccionar variable", choice,index=0)

ind = choice.index(choice_selected)

limite_datos = 500

results = client.get(catal[ind], limit=limite_datos,where = "fechaobservacion > '2022-06-09T23:59:00.000'" )
df1 = pd.DataFrame.from_records(results)
df1.head()


df1 = corr_format(df1)
#st.write(df1.head())