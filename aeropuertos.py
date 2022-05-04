#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:11:05 2022

@author: luisa
"""


import pandas as pd
import  numpy as np
from datetime import datetime
from tqdm import tqdm              # libreria para saber el tiempo de ejecución
from sqlalchemy import create_engine
import os
import math
import re
import matplotlib.pyplot as plt #Para graficar

def SQL_PD(table_or_sql,eng):
       engine = create_engine(eng)
       conn = engine.connect()
       generator_object = pd.read_sql(table_or_sql,con=conn)
       return generator_object 
#Esta función permite analizar un data frame con tres columnas (FechaObservación, 
# CodigoEstacion y ValorObservado) para la variable de precipitación
#direccion1 = dirección donde se va a guardar los png de los CMA
#direccion2 = Dirección donde se va a guardar los png de los CMD
#direccion3 = Dirección donde se va a guardar el archivo de salida final


def col3_analisis_p(df_v,direccion1,direccion2,direccion3):
    df_v["fecha"]=pd.to_datetime(df_v["FechaObservacion"])
    cod=df_v.CodigoEstacion.unique()
    n_1=len(cod)
    titulos=["CodigoEstacion","FechaInicial","FechaFinal","dxI","dxF","tamaño","Maximo"
             ,"Minimo","Promedio"]
    vector=[titulos]
    exep=["CodigoEstacion"]
    for i in tqdm(range(n_1)):
        cod_q=cod[i]
        df=df_v[df_v.CodigoEstacion==cod_q]
        #df=pd.DataFrame(df)
        df = df.reset_index()
        print("Se guarda la estacion", cod_q)
    
        try:
            
            #longitud de filas
            n=len(df)
            #longitud de columnas
            shape = df.shape
            #Obtener el nombre de las columnas
            #columns_names = variables_df.columns.values
            #Paso de tiempo
            if n <=1 :
                print("SOLO TIENE UNA FECHA REGISTRADA")
                dxi=None
                dxf=None
                
            if n > 1:
                if df["fecha"][0] != df["fecha"][1]:
                    dxi=(df["fecha"][1]-df["fecha"][0]).seconds/60    
                else:
                    dxi=None
                    
                if df["fecha"][n-1] != df["fecha"][n-2]:
                    dxf=(df["fecha"][n-1]-df["fecha"][n-2]).seconds/60    
                else:
                    dxf=None
                
            print("")
            print("#---------------------------#")
            print("Estación",cod_q)
            print("")
            print("INFORMACIÓN INICIAL")
            print("")
            print("1. La fecha inicial =",df["fecha"][0] )
            print("2. La fecha final =",df["fecha"][n-1] )
            print("3. Muestreo valores iniciales =",dxi, "min")
            print("4. Muestreo valores finales =",dxf, "min")
            print("5. La cantidad de filas y columnas =",shape )
            #print("6. El nombre de las columnas es=",columns_names)
            print("7. Las primeras filas son= ")
            print(df.head())
            print("8. Las últimas filas= ")
            print(df.tail())
            print("")
            #CALCULOS
            #max, min, promedio
            #Valor máximo
            maxi=df.ValorObservado.max()
            mini=df.ValorObservado.min()
            media=df.ValorObservado.mean()
            desviacion=np.std(df.ValorObservado)
            mediana=np.median(df.ValorObservado)
    
            print("")
            print("ESTADISTICOS")
            print("")
            print("17. Valor máximo= ", maxi)
            print("18. Valor mínimo= ", mini)
            print("19. Valor medio= ", media)
            print("20. Desviación estandar", desviacion)
            print("21. Mediana= ", mediana)
            
            df["year"]=pd.to_datetime(df['fecha']).dt.year 
            df["month"]=pd.to_datetime(df['fecha']).dt.month
            df["day"]=pd.to_datetime(df['fecha']).dt.day  
            df["hour"]=pd.to_datetime(df['fecha']).dt.hour
            month=list(df["month"].unique())
            month.sort() 
            hour=list(df["hour"].unique())
            hour.sort()
            
            print("")
            print("GRAFICOS")
            print("")
            
            #ciclo diurno
            H=[]
            for j in tqdm(hour):
                hora=df[df.hour==j]
                mean_h=hora.ValorObservado.mean(skipna=True)
                H.append(mean_h)
                #print("Ingresa")
            #grafico
            plt.figure(figsize=(10,5))
            plt.title("Ciclo medio diurno \n Estación " +str(cod_q) 
                      , size=20, loc='center', pad=8)
            plt.plot(hour,H,color="slateblue",label=("precipitacion -",str(cod_q)))
            plt.xlabel("Tiempo (horas)")
            plt.ylabel("Precipitacion [mm]")
            plt.grid()
            plt.legend()
            plt.minorticks_on()
            plt.savefig(direccion2+'CMD'  + '_IDEAM-' + str(cod_q) + '_' + str(i) + '.png') 
            
            
            #ciclo medio anual
            
            if len(month) != 12:
                lista=[1,2,3,4,5,6,7,8,9,10,11,12]
                dif_1=set(lista).difference(set(month))
                dif_2=set(month).difference(set(lista))
                dif=list(dif_1.union(dif_2))
                len_dif=len(dif)
                for k in range(len(dif)):
                    month.append(dif[k])
                month.sort()
                
            Ma_mes=[]
            for j in tqdm(month):
                mes=df[df.month==j]
                mean_m=mes.ValorObservado.mean(skipna=True)
                Ma_mes.append(mean_m)
                #print("Ingresa el promed|io del mes",j)
            meses=np.array(["Ene","Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", 
                            "Sep","Oct", "Nov", "Dic"])
            
            plt.figure(figsize=(10,5))
            plt.title("Ciclo Medio Anual \n Estación= " +str(cod_q) 
                      , size=20, loc='center', pad=8)
            #plt.title("Ciclo medio anual \n Estación" )
            plt.plot(meses,Ma_mes,color="indigo",label=("precipitacion -",str(cod_q)))
            plt.legend()
            plt.xlabel("Tiempo (meses)")
            plt.ylabel("Precipitación [mm]")
            plt.grid()
            plt.minorticks_on()
            plt.savefig(direccion1+'CMA'  + '_IDEAM-' + str(cod_q) + '_' + str(i) + '.png')  
            
            #se guarda el archivo
            titulos=["CodigoEstacion","FechaInicial","FechaFinal","dxI","dxF","tamaño","Maximo"
                     ,"Minimo","Promedio"]
    
            c=[cod_q,df["fecha"][0],df["fecha"][n-1],dxi,dxf,shape,maxi,mini,media,
               desviacion,mediana]
            vector.append(c)
            #print(vector)
            print("termina" ,i, "-",cod_q)
            print("#---------------------------#")
        except:
            print("La estación", cod_q, "No pudo ser ingresada")
            exep.append(cod_q)
            
    print("se termina de analizar la base de datos")
    df_final=pd.DataFrame(vector)
    df_final.to_csv(direccion3,sep=";")
    return(df_final,exep)    

def col3_analisis_t(df_v,direccion1,direccion2,direccion3):
    df_v["fecha"]=pd.to_datetime(df_v["FechaObservacion"])
    cod=df_v.CodigoEstacion.unique()
    n_1=len(cod)
    titulos=["CodigoEstacion","FechaInicial","FechaFinal","dxI","dxF","tamaño","Maximo"
             ,"Minimo","Promedio"]
    vector=[titulos]
    exep=["CodigoEstacion"]
    for i in tqdm(range(n_1)):
        cod_q=cod[i]
        df=df_v[df_v.CodigoEstacion==cod_q]
        #df=pd.DataFrame(df)
        df = df.reset_index()
        print("Se guarda la estacion", cod_q)
    
        try:
            
            #longitud de filas
            n=len(df)
            #longitud de columnas
            shape = df.shape
            #Obtener el nombre de las columnas
            #columns_names = variables_df.columns.values
            #Paso de tiempo
            if n <=1 :
                print("SOLO TIENE UNA FECHA REGISTRADA")
                dxi=None
                dxf=None
                
            if n > 1:
                if df["fecha"][0] != df["fecha"][1]:
                    dxi=(df["fecha"][1]-df["fecha"][0]).seconds/60    
                else:
                    dxi=None
                    
                if df["fecha"][n-1] != df["fecha"][n-2]:
                    dxf=(df["fecha"][n-1]-df["fecha"][n-2]).seconds/60    
                else:
                    dxf=None
                
            print("")
            print("#---------------------------#")
            print("Estación",cod_q)
            print("")
            print("INFORMACIÓN INICIAL")
            print("")
            print("1. La fecha inicial =",df["fecha"][0] )
            print("2. La fecha final =",df["fecha"][n-1] )
            print("3. Muestreo valores iniciales =",dxi, "min")
            print("4. Muestreo valores finales =",dxf, "min")
            print("5. La cantidad de filas y columnas =",shape )
            #print("6. El nombre de las columnas es=",columns_names)
            print("7. Las primeras filas son= ")
            print(df.head())
            print("8. Las últimas filas= ")
            print(df.tail())
            print("")
            #CALCULOS
            #max, min, promedio
            #Valor máximo
            maxi=df.ValorObservado.max()
            mini=df.ValorObservado.min()
            media=df.ValorObservado.mean()
            desviacion=np.std(df.ValorObservado)
            mediana=np.median(df.ValorObservado)
    
            print("")
            print("ESTADISTICOS")
            print("")
            print("17. Valor máximo= ", maxi)
            print("18. Valor mínimo= ", mini)
            print("19. Valor medio= ", media)
            print("20. Desviación estandar", desviacion)
            print("21. Mediana= ", mediana)
            
            df["year"]=pd.to_datetime(df['fecha']).dt.year 
            df["month"]=pd.to_datetime(df['fecha']).dt.month
            df["day"]=pd.to_datetime(df['fecha']).dt.day  
            df["hour"]=pd.to_datetime(df['fecha']).dt.hour
            month=list(df["month"].unique())
            month.sort() 
            hour=list(df["hour"].unique())
            hour.sort()
            
            print("")
            print("GRAFICOS")
            print("")
            
            #ciclo diurno
            H=[]
            for j in tqdm(hour):
                hora=df[df.hour==j]
                mean_h=hora.ValorObservado.mean(skipna=True)
                H.append(mean_h)
                #print("Ingresa")
            #grafico
            plt.figure(figsize=(10,5))
            plt.title("Ciclo medio diurno \n Estación " +str(cod_q) 
                      , size=20, loc='center', pad=8)
            plt.plot(hour,H,color="palevioletred",label=("precipitacion -",str(cod_q)))
            plt.xlabel("Tiempo (horas)")
            plt.ylabel("Temperatura [°C]")
            plt.grid()
            plt.legend()
            plt.minorticks_on()
            plt.savefig(direccion2+'CMD'  + '_IDEAM-' + str(cod_q) + '_' + str(i) + '.png') 
            
            
            #ciclo medio anual
            
            if len(month) != 12:
                lista=[1,2,3,4,5,6,7,8,9,10,11,12]
                dif_1=set(lista).difference(set(month))
                dif_2=set(month).difference(set(lista))
                dif=list(dif_1.union(dif_2))
                len_dif=len(dif)
                for k in range(len(dif)):
                    month.append(dif[k])
                month.sort()
                
            Ma_mes=[]
            for j in tqdm(month):
                mes=df[df.month==j]
                mean_m=mes.ValorObservado.mean(skipna=True)
                Ma_mes.append(mean_m)
                #print("Ingresa el promed|io del mes",j)
            meses=np.array(["Ene","Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", 
                            "Sep","Oct", "Nov", "Dic"])
            
            plt.figure(figsize=(10,5))
            plt.title("Ciclo Medio Anual \n Estación= " +str(cod_q) 
                      , size=20, loc='center', pad=8)
            #plt.title("Ciclo medio anual \n Estación" )
            plt.plot(meses,Ma_mes,color="crimson",label=("precipitacion -",str(cod_q)))
            plt.legend()
            plt.xlabel("Tiempo (meses)")
            plt.ylabel("Temperatura [°C]")
            plt.grid()
            plt.minorticks_on()
            plt.savefig(direccion1+'CMA'  + '_IDEAM-' + str(cod_q) + '_' + str(i) + '.png')  
            
            #se guarda el archivo
            titulos=["CodigoEstacion","FechaInicial","FechaFinal","dxI","dxF","tamaño","Maximo"
                     ,"Minimo","Promedio"]
    
            c=[cod_q,df["fecha"][0],df["fecha"][n-1],dxi,dxf,shape,maxi,mini,media,
               desviacion,mediana]
            vector.append(c)
            #print(vector)
            print("termina" ,i, "-",cod_q)
            print("#---------------------------#")
        except:
            print("La estación", cod_q, "No pudo ser ingresada")
            exep.append(cod_q)
            
    print("se termina de analizar la base de datos")
    df_final=pd.DataFrame(vector)
    df_final.to_csv(direccion3,sep=";")
    return(df_final,exep)

#precipitacion
#lucy
dfp=pd.read_csv(r"/home/marcelae/Desktop/FACOM/aeropuertos/entrega/precipitacion_2018_AeropuertosPD.csv")
#luisa
#dfp=pd.read_csv(r"/media/luisa/Datos/FACOM/gits/FACOM/aeropuertos/entrega/precipitacion_2018_AeropuertosPD.csv")
dfp.columns=["FechaObservacion", "CodigoEstacion", "ValorObservado"]
direccion1p="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/png/anual_p/"
direccion2p="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/png/diurno_p/"
direccion3p="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/aeropuertos_p_2018.csv"
p,exep_p=col3_analisis_p(dfp,direccion1p,direccion2p,direccion3p)

#temperatura
dft=pd.read_csv(r"/home/marcelae/Desktop/FACOM/aeropuertos/entrega/temperatura_2018_AeropuertosPD.csv",sep=";")
dft.columns=["FechaObservacion", "CodigoEstacion", "ValorObservado"]

direccion1t="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/png/anual_t/"
direccion2t="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/png/diurno_t/"
direccion3t="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/aeropuertos_t_2018.csv"
t,exep_t=col3_analisis_t(dft,direccion1t,direccion2t,direccion3t)

#################################################3


#d_A_entrada= dirección del archivo de entrada para comparar,
#usecols_AE= columnas de referencia del archivo de entrada (lon y lat en ese orden)

#hallar las coordenadas cercanas a unas de referencia, en una base de datos, en un área cuadrada
def rangocuadrado_coordenadas(d_A_entrada,usecols_AE,variacion_lat,variacion_lon
                              ,direccion1,direccion2,direccion3,eng,tabla):
    #se ingresa la información de entrada
    datos = pd.read_csv( d_A_entrada, usecols=usecols_AE)
    #se realiza el cambio en los nombres de las columnas para realizar un append
    datos.columns = ["lon","lat"]
    
    #Se crean los vectores para guardar
    
    #archivo con estaciones no encontradas
    titulos1 = ["lat","lon"]
    vector1 = [titulos1]
    #archivo con estaciones encontradas
    titulos = ["i","CodigoEstacion","NombreEstacion","Departamento","Municipio",
             "ZonaHidrografica","Latitud","Longitud"]
    vector = [titulos]
    #cuando encuentra más de 1 estación
    titulos2 = ["i","CodigoEstacion","NombreEstacion","Departamento","Municipio",
              "ZonaHidrografica","Latitud","Longitud"]
    vector2 = [titulos2]
    
    for i in  tqdm(range(len(datos))):
        my_query3='''
        SELECT DISTINCT CodigoEstacion,NombreEstacion,Departamento,Municipio,ZonaHidrografica,Latitud,Longitud
        FROM {}
        WHERE (Latitud <= {} AND Latitud >= {}) AND (Longitud <= {} AND Longitud >= {})
        '''.format(tabla,datos["lat"][i]+variacion_lat , datos["lat"][i]-variacion_lat ,datos["lon"][i]+variacion_lon,datos["lon"][i]-variacion_lon)
        df_est = SQL_PD(my_query3,eng)
        
        n=len(df_est)
        if n== 0 :
            print("el paso de tiempo ",i, "no tiene información disponible en las coordenadas"
                  ,"(",datos["lon"][i],",",datos["lat"][i],")")
            c1=(datos["lon"][i],datos["lat"][i])
            vector1.append(c1)
        if n != 0 :
            if n == 1:
                
                #print("el paso de tiempo ", i, " tiene información disponible")
                c=(i,df_est["CodigoEstacion"][0],df_est["NombreEstacion"][0],df_est["Departamento"][0],
                          df_est["Municipio"][0],df_est["ZonaHidrografica"][0],df_est["Latitud"][0],
                          df_est["Longitud"][0])
                print(i, "- El codigo de estación es= ",df_est["CodigoEstacion"][0] )
                vector.append(c)
            elif n > 1:
                print("el paso de tiempo ",i, " tiene ",n," estaciones que coindice")
                for j in range(n):
                    print(i, "- El codigo de estación es= ",df_est["CodigoEstacion"][j] )
                    c2=(i,df_est["CodigoEstacion"][j],df_est["NombreEstacion"][j],df_est["Departamento"][j],
                              df_est["Municipio"][j],df_est["ZonaHidrografica"][j],df_est["Latitud"][j],
                              df_est["Longitud"][j])
                    vector2.append(c2)
    print(" el archivo final tiene ", len(vector), " filas unicas")
    
    #se guarda la información
    #guardar el archivo csv
    df=pd.DataFrame(vector)
    df_noencontrados=pd.DataFrame(vector1)
    df_varios=pd.DataFrame(vector2)
    
    df.to_csv(direccion1,header=None, index=None, sep=';')
    df_noencontrados.to_csv(direccion2,header=None, index=None, sep=';')
    df_varios.to_csv(direccion3,header=None, index=None, sep=';')
    print("se guardan los archivos para ")

#direccion1 = archivo de salida de los coordenadas que solo tienen una coincidencia
#direccion2 = archivo de salida de los coordenadas que no tienen coincidencia
#direccion3 = archivo de salida de los coordenadas que tienen varias coincidencia  
        
        



#daniel
d_A_entradad="/home/marcelae/Desktop/FACOM/aeropuertos/airport_coord.csv"
usecols_AEd=[1,2]
variacion_latd=(0.09/2)
variacion_lond=(0.17921/2) 
direccion1d="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/analisis_por_lat_lon/C1.csv"
direccion2d="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/analisis_por_lat_lon/sinC.csv"
direccion3d="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/analisis_por_lat_lon/variasC.csv" 

#julio
d_A_entradaj="/home/marcelae/Desktop/FACOM/aeropuertos/Aeropuertos.csv"
usecols_AEj=[2,3]
variacion_latj=0.009
variacion_lonj=0.017921  

direccion1j="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/julio/analisis_por_lat_lon/C1.csv"
direccion2j="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/julio/analisis_por_lat_lon/sinC.csv"
direccion3j="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/julio/analisis_por_lat_lon/variasC.csv"
  

engt = "sqlite:////home/marcelae/Desktop/FACOM/db/temperatura_2.db"
engp = "sqlite:////home/marcelae/Desktop/FACOM/db/precipitacion_2.db"
tablap="precipitacion"
tablat="temperatura"


#daniel
rangocuadrado_coordenadas(d_A_entradad,usecols_AEd,variacion_latd,variacion_lond,
                          direccion1d,direccion2d,direccion3d,engp,tablat)

#julio
rangocuadrado_coordenadas(d_A_entradaj,usecols_AEj,variacion_latj,variacion_lonj,
                          direccion1j,direccion2j,direccion3j,engp,tablat)


