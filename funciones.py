#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Funciones
"""
###############################################################################

# 1. 

#Esta función permite analizar un data frame con tres columnas (FechaObservación, 
# CodigoEstacion y ValorObservado) para la variable de precipitación, y además
# saca graficos de ciclos diurnos y ciclos mensuales para un solo año 

#direccion1 = dirección donde se va a guardar los png de los CMA
#direccion2 = Dirección donde se va a guardar los png de los CMD
#direccion3 = Dirección donde se va a guardar el archivo de salida final

#temperatura
def col3_analisis_t(df_v,direccion1,direccion2,direccion3):
    df_v["fecha"]=pd.to_datetime(df_v["FechaObservacion"])
    cod=df_v.CodigoEstacion.unique()
    n_1=len(cod)
    titulos=["CodigoEstacion","FechaInicial","FechaFinal","dxI","dxF","Tamaño","Maximo"
             ,"Minimo","Promedio","DesviacionEstandar","Mediana"]
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
            maxi=round(df.ValorObservado.max(),3)
            mini=round(df.ValorObservado.min(),3)
            media=round(df.ValorObservado.mean(),3)
            desviacion=round(np.std(df.ValorObservado),3)
            mediana=round(np.median(df.ValorObservado),3)
    
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
            plt.title("Ciclo Medio Diurno \n Estación " +str(cod_q) 
                      , size=20, loc='center', pad=8)
            plt.plot(hour,H,color="palevioletred",label=("Temperatura -",str(cod_q)))
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
            plt.title("Ciclo Anual 2018\n Estación= " +str(cod_q) 
                      , size=20, loc='center', pad=8)
            #plt.title("Ciclo medio anual \n Estación" )
            plt.plot(meses,Ma_mes,color="crimson",label=("Temperatura -",str(cod_q)))
            plt.legend()
            plt.xlabel("Tiempo (meses)")
            plt.ylabel("Temperatura [°C]")
            plt.grid()
            plt.minorticks_on()
            plt.savefig(direccion1+'CMA'  + '_IDEAM-' + str(cod_q) + '_' + str(i) + '.png')  
            
            #se guarda el archivo
    
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
#precipitación
def col3_analisis_p(df_v,direccion1,direccion2,direccion3):
    df_v["fecha"]=pd.to_datetime(df_v["FechaObservacion"])
    cod=df_v.CodigoEstacion.unique()
    n_1=len(cod)
    titulos=["CodigoEstacion","FechaInicial","FechaFinal","dxI","dxF","tamaño","Maximo"
             ,"Minimo","Promedio","DesviacionEstandar","Mediana"]
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
            maxi=round(df.ValorObservado.max(),3)
            mini=round(df.ValorObservado.min(),3)
            media=round(df.ValorObservado.mean(),3)
            desviacion=round(np.std(df.ValorObservado),3)
            mediana=round(np.median(df.ValorObservado),3)
    
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
            plt.title("Ciclo Medio Diurno \n Estación " +str(cod_q) 
                      , size=20, loc='center', pad=8)
            plt.plot(hour,H,color="slateblue",label=("Precipitacion -",str(cod_q)))
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
            plt.title("Ciclo Anual \n Estación= " +str(cod_q) 
                      , size=20, loc='center', pad=8)
            #plt.title("Ciclo medio anual \n Estación" )
            plt.plot(meses,Ma_mes,color="indigo",label=("Precipitacion -",str(cod_q)))
            plt.legend()
            plt.xlabel("Tiempo (meses)")
            plt.ylabel("Precipitación [mm]")
            plt.grid()
            plt.minorticks_on()
            plt.savefig(direccion1+'CMA'  + '_IDEAM-' + str(cod_q) + '_' + str(i) + '.png')  
            
            #se guarda el archivo
    
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
    
#Nota: se debería modificar para que saque los años, agregando una fecha inicial
#y una final, modificar para que sea más general.

#Ejmpplo
dfp=pd.read_csv(r"/media/luisa/Datos/FACOM/gits/FACOM/aeropuertos/entrega/precipitacion_2018_AeropuertosPD.csv")
dfp.columns=["FechaObservacion", "CodigoEstacion", "ValorObservado"]
direccion1p="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/png/anual_p/"
direccion2p="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/png/diurno_p/"
direccion3p="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/aeropuertos_p_2018.csv"
p,exep_p=col3_analisis_p(dfp,direccion1p,direccion2p,direccion3p)

###############################################################################

# 2.
#hallar las coordenadas cercanas a unas de referencia, en una base de datos, en un área cuadrada

#d_A_entrada= dirección del archivo de entrada para comparar,
#usecols_AE= columnas de referencia del archivo de entrada (lon y lat en ese orden)
#variacion_lat= distancia vertical del cuadro  para la busqueda
#variacion_lon= distancia horizontal del cuadro  para la busqueda
#direccion1 = archivo de salida de los coordenadas que solo tienen una coincidencia
#direccion2 = archivo de salida de los coordenadas que no tienen coincidencia
#direccion3 = archivo de salida de los coordenadas que tienen varias coincidencia

def rangocuadrado_coordenadas(d_A_entrada,usecols_AE,variacion_lat,variacion_lon,direccion1,direccion2,direccion3,eng,tabla):
    #se ingresa la información de entrada
    datos = pd.read_csv( d_A_entrada, usecols=usecols_AE)
    #se realiza el cambio en los nombres de las columnas para realizar un append
    datos.columns = ["lon","lat"]
    
    #Se crean los vectores para guardar
    
    #archivo con estaciones no encontradas
    titulos1 = ["lon","lat"]
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

#Ejemplo
d_A_entradad="/home/marcelae/Desktop/FACOM/aeropuertos/airport_coord.csv"
usecols_AEd=[1,2]
variacion_latd=(0.09/2)
variacion_lond=(0.17921/2) 
direccion1d="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/analisis_por_lat_lon/C1.csv"
direccion2d="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/analisis_por_lat_lon/sinC.csv"
direccion3d="/home/marcelae/Desktop/FACOM/aeropuertos/entrega/daniel/analisis_por_lat_lon/variasC.csv" 
engp = "sqlite:////home/marcelae/Desktop/FACOM/db/precipitacion_2.db"
tablap="precipitacion"
rangocuadrado_coordenadas(d_A_entradad,usecols_AEd,variacion_latd,variacion_lond,
                          direccion1d,direccion2d,direccion3d,engp,tablap)
###############################################################################
#3. 
#Generar un dataframe de una base de datos
#table_or_sql= nombre de la tabla
#eng = maquina, ubicación de la base de datos
def SQL_PD(table_or_sql,eng):
       engine = create_engine(eng)
       conn = engine.connect()
       generator_object = pd.read_sql(table_or_sql,con=conn)
       return generator_object 

#Ejmplo
cod = 21201200
my_query2='''
SELECT CodigoEstacion,FechaObservacion,ValorObservado,NombreEstacion,Departamento,
Municipio,ZonaHidrografica,Latitud,Longitud,DescripcionSensor,UnidadMedida 
FROM temperatura
WHERE (codigoestacion = {})
'''.format(int(cod))
df_est = SQL_PD(my_query2,eng)
###############################################################################
# 4.

#columnas son los nombres de las columnas para buscar, tabla es el nombre de la
#tabla en la que se va a buscar y el eng es la base de datos, por ejemplo:
#columnas="Municipio", tabla="precipitacion"
def my_query_distinct(columnas,tabla,eng):
    my_query='''
    SELECT DISTINCT {} 
    FROM {}
    '''.format(columnas,tabla)
    df = SQL_PD(my_query,eng)
    return df
###############################################################################

#5. 

#columnas son los nombres únicos de las columnas para buscar, tabla es el nombre de la
#tabla en la que se va a buscar, where es la condición de busqueda, por ejemplo :
#columnas="Municipio", tabla="precipitacion", where="CodigoEstacion = {}" , cod= 21201200
def my_query_distinct_where(columnas,tabla,eng,where,cod):
    my_query='''
    SELECT DISTINCT {} 
    FROM {}
    WHERE ({}={})
    '''.format(columnas,tabla,where,cod)
    df = SQL_PD(my_query,eng)
    return df
###############################################################################

#6.

#columnas son los nombres de las columnas para buscar, tabla es el nombre de la
#tabla en la que se va a buscar, where es la condición de busqueda, por ejemplo :
#columnas="Municipio", tabla="precipitacion", where="CodigoEstacion = {}" , cod= 21201200 

def my_query_where(columnas,tabla,eng,where,cod):
    my_query='''
    SELECT {} 
    FROM {}
    WHERE ({}={})
    '''.format(columnas,tabla,where,cod)
    df = SQL_PD(my_query,eng)
    return df
###############################################################################
#7.

#Saca un archivo csv con información de estadisticos, de valores individuales  
# de una base de datos. 
#direccion = Guarda los graficos del CICLO MEDIO ANUAL
#direccion2 =Guarda el archivo final csv
#direccion3 =Guarda los graficos del CICLO MEDIO DIURNO 

#Ejemplo
direccion="/home/marcelae/Desktop/FACOM/png/precipitacion_completo/anual/"
direccion2="/home/marcelae/Desktop/FACOM/Estaciones/precipitacion_información.csv"
direccion3="/home/marcelae/Desktop/FACOM/png/precipitacion_completo/diurno/"
engp= 'sqlite:////home/marcelae/Desktop/FACOM/db/precipitacion_2.db'
tabla="precipitacion"
p=analisis_variable(tabla, engp,direccion,direccion2,direccion3)


def analisis_variable(tabla, eng,direccion,direccion2,direccion3):
    #creación de vectores
    titulos=["Codigo Estacion","Nombre de estacion","Municipio","Departamento", "Zona Hidrográfica","Latitud"
             ,"Longitud","Fecha Inicial","Fecha Final","Muestreo valores iniciales","Muestreo valores finales","Numerofilas y columnas",
             "Máximo","Mínimo","Promedio","Desviación Estándar","Mediana"]
    vector=[titulos]
    exep=["codigos"]
    
    #encontrar los codigos de la base de datos ingresada
    columnas="CodigoEstacion"
    datos=my_query_distinct(columnas,tabla,eng)
    for i in tqdm(range(len(datos))):
        try:
            cod = datos["CodigoEstacion"][i]
            #cod=21201580
            #valores individuales de la base de datos para el codigo
            columnas1 = "NombreEstacion,Departamento,Municipio,ZonaHidrografica,Latitud,Longitud,DescripcionSensor,UnidadMedida"
            where = "CodigoEstacion"
            unicos_df = my_query_distinct_where(columnas1,tabla,eng,where,cod)
            #Valores variables de fecha y valor observado
            columnas2="FechaObservacion,ValorObservado "
            variables_df=my_query_where(columnas2,tabla,eng,where,cod)
            
            #-------------------------------------------------------------------#
            
            #fechas
            variables_df["fecha"]=pd.to_datetime(variables_df['FechaObservacion'],format='%m/%d/%Y %I:%M:%S %p')
            #organizar las filas de mayor a menor con respecto a la fecha
            variables_df = variables_df.sort_values(by='fecha')
            #Se resetean los indices
            variables_df=variables_df.reset_index(drop=True)
            #longitud de filas
            n=len(variables_df)
            #longitud de columnas
            shape = variables_df.shape
            #Obtener el nombre de las columnas
            #columns_names = variables_df.columns.values
            
            #Valores unicos
            #latitud y longitud
            lat=unicos_df["Latitud"][0]
            lon=unicos_df["Longitud"][0]
            #Municipio y departamento
            mu=unicos_df["Municipio"][0]
            dep=unicos_df["Departamento"][0]
            #Zona hidrografica y nombre de la estación
            zh=unicos_df["ZonaHidrografica"][0]
            ne=unicos_df["NombreEstacion"][0]
            #descrición del sensor y unidades
            desS=unicos_df["DescripcionSensor"][0]
            unidades=unicos_df["UnidadMedida"][0]
            #Paso de tiempo
            if n <=1 :
                print("SOLO TIENE UNA FECHA REGISTRADA")
                dxi=None
                dxf=None
                
            if n > 1:
                if variables_df["fecha"][0] != variables_df["fecha"][1]:
                    dxi=(variables_df["fecha"][1]-variables_df["fecha"][0]).seconds/60    
                else:
                    dxi=None
                    
                if variables_df["fecha"][n-1] != variables_df["fecha"][n-2]:
                    dxf=(variables_df["fecha"][n-1]-variables_df["fecha"][n-2]).seconds/60    
                else:
                    dxf=None
            
            print("")
            print("#---------------------------#")
            print("Estación",cod)
            print("")
            print("INFORMACIÓN INICIAL")
            print("")
            print("1. La fecha inicial =",variables_df["fecha"][0] )
            print("2. La fecha final =",variables_df["fecha"][n-1] )
            print("3. Muestreo valores iniciales =",dxi, "min")
            print("4. Muestreo valores finales =",dxf, "min")
            print("5. La cantidad de filas y columnas =",shape )
            #print("6. El nombre de las columnas es=",columns_names)
            print("7. Las primeras filas son= ")
            print(variables_df.head())
            print("8. Las últimas filas= ")
            print(variables_df.tail())
            print("")
            print("LATITUD Y LONGITUD")
            print("")
            print("9. latitud=", lat)
            print("10. longitud=", lon)
            print("")
            print("MUNICIPIO, DEPARTAMENTO, ZONA HIDROGRAFICA Y NOMBRE DE LA ESTACIÓN")
            print("")
            print("11. Municipio= ", mu)
            print("12. Departamento= ", dep)
            print("13. Zona Hidrografica= ", zh)
            print("14. Nombre de la estación= ", ne)
            print("")
            print("UNIDADES Y OTRAS DESCRIPCIONES")
            print("")
            print("15. Unidades de la variable de estudio= ", unidades)
            print("16. Descripción del sensor= ", desS)
            print("")
            
            #CALCULOS
            #max, min, promedio
            #Valor máximo
            maxi=variables_df.ValorObservado.max()
            mini=variables_df.ValorObservado.min()
            media=variables_df.ValorObservado.mean()
            desviacion=np.std(variables_df.ValorObservado)
            mediana=np.median(variables_df.ValorObservado)
    
            print("")
            print("ESTADISTICOS")
            print("")
            print("17. Valor máximo= ", maxi)
            print("18. Valor mínimo= ", mini)
            print("19. Valor medio= ", media)
            print("20. Desviación estandar", desviacion)
            print("21. Mediana= ", mediana)
    
    
            variables_df["year"]=pd.to_datetime(variables_df['fecha']).dt.year 
            variables_df["month"]=pd.to_datetime(variables_df['fecha']).dt.month
            variables_df["day"]=pd.to_datetime(variables_df['fecha']).dt.day  
            variables_df["hour"]=pd.to_datetime(variables_df['fecha']).dt.hour
            month=list(variables_df["month"].unique())
            month.sort() 
            hour=list(variables_df["hour"].unique())
            hour.sort()
            
            H=[]
            for j in tqdm(hour):
                hora=variables_df[variables_df.hour==j]
                mean_h=hora.ValorObservado.mean(skipna=True)
                H.append(mean_h)
                #print("Ingresa")
            
            print("")
            print("GRAFICOS")
            print("")
            
            plt.figure(figsize=(10,5))
            plt.title("Ciclo medio diurno \n Estación " +str(cod) +" - "+ne
                      , size=20, loc='center', pad=8)
            plt.plot(hour,H)
            plt.xlabel("Tiempo (horas)")
            plt.ylabel(desS+" ("+unidades+")")
            plt.grid()
            plt.savefig(direccion3+'CMD'  + '_IDEAM-' + str(cod) + '_' + str(i) + '.png') 
            
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
                mes=variables_df[variables_df.month==j]
                mean_m=mes.ValorObservado.mean(skipna=True)
                Ma_mes.append(mean_m)
                #print("Ingresa el promed|io del mes",j)
            meses=np.array(["Ene","Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", 
                            "Sep","Oct", "Nov", "Dic"])
            
            plt.figure(figsize=(10,5))
            plt.title("Ciclo medio anual \n Estación " +str(cod) +" - "+ne
                      , size=20, loc='center', pad=8)
            #plt.title("Ciclo medio anual \n Estación" )
            plt.plot(meses,Ma_mes)
            plt.xlabel("Tiempo en meses")
            plt.ylabel(desS+" ("+unidades+")")
            plt.grid()
            plt.savefig(direccion+'CMA'  + '_IDEAM-' + str(cod) + '_' + str(i) + '.png')  
    
            c=[cod,ne,mu,dep,zh,lat,lon,variables_df["fecha"][0],variables_df["fecha"][n-1],
               dxi,dxf,shape,maxi,mini,media,desviacion,mediana]
            
            vector.append(c)
            #print(vector)
            print("termina" ,i, "-",cod)
            print("#---------------------------#")
        except:
            print("La estación", cod, "No pudo ser ingresada")
            exep.append(cod)
            
            
    print("se termina de analizar la base de datos")
    df_final=pd.DataFrame(vector)
    df_final.to_csv(direccion2,sep=";")
    return(df_final,exep)

    

