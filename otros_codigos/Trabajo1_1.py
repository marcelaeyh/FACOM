#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 18:02:02 2021

@author:Jhon Alejandro Zuluaga- Luisa Fernanda Buriticá -Luisa Fernanda Torres

"""
#Se importan las librerías.
import numpy as np             #Librería para operaciones numéricas.
import matplotlib.pyplot as plt#Librería para generar gráficas.
import xarray as xr            #Librería para el manejo de archivos NetCDF.
import os                      #Librería para el manejo de funciones del sistema.
import cartopy                 #librería para el manejo de mapas.
import cartopy.crs as ccrs

#Se cargan los archivos y se extraen el valor de las varias variables.

#Temperatura.
ifile_2011_2015 = xr.open_dataset('t2m_mon_2011-2015.nc')  #Se abre el archivo.
t2m= (ifile_2011_2015.t2m ) - 273.15                       #Datos con la temperatura(°C).
lon= ifile_2011_2015.longitude                             #Datos con la longitud.
lat= ifile_2011_2015.latitude                              #Datos con la latitud.
time= ifile_2011_2015.time                                 #Datos con el tiempo.

#Topografía.
ifile_topografia= xr.open_dataset('altura_z_mascara.nc')   #Se abre el archivo.
z=ifile_topografia.z                                       #Datos con la altura.

#Ciclo anual
ifile_cicloanual = xr.open_dataset('CicloMedioAnual.nc')   #Se abre el archivo.
t2m_CMA_K=ifile_cicloanual.t2m                             #Datos con la temperatura(K).
t2m_CMA_c=(ifile_cicloanual.t2m)-273.15                    #Datos con la temperatura(°C).
lon_CMA=ifile_cicloanual.longitude                         #Datos con la longitud.
lat_CMA=ifile_cicloanual.latitude                          #Datos con la latitud.

#Promedios estacionales
ifile_PEM = xr.open_dataset('ProEstaMultianual4.nc')       #Se abre el archivo.
t2m_PEM_K=ifile_PEM.t2m                                    #Datos con la temperatura(K)
t2m_PEM_c=(ifile_PEM.t2m)-273.15                           #Datos con la temperatura(°C). 
lon_PEM=ifile_PEM.longitude                                #Datos con la longitud.
lat_PEM=ifile_PEM.latitude                                 #Datos con la latitud.


#__________________________________________________________________________________________
#__________________________________________________________________________________________

#Delimitación.

#Se crean las coordenadas para las áreas de interés.
#La Sabana.
lat1=5.0                                                   #Latitud más al sur.
lat2=5.5                                                   #Latitud más al norte.
lon1=-69.0                                                 #Longitud más al oeste.
lon2=-69.5                                                 #Longitud más al este.

#El Amazonas.
lat3=1.0                                                   #Latitud más al sur.
lat4=1.5                                                   #Latitud más al norte.
lon3=-77.0                                                 #Longitud más al oeste.
lon4=-76.5                                                 #Longitud más al este.

#Se crea el mapa.
fig = plt.figure(figsize=(15,10))                          #Tamaño a la hoja.
ax = fig.add_subplot(projection=ccrs.PlateCarree())        #Se indica que se va a graficar.
ax.set_extent([-66, -80, -5, 13])                          #Coordenadas de la hoja.
ax.coastlines('50m',linewidth = 2)                         #Contornos de continentes.
ax.add_feature(cartopy.feature.BORDERS, linewidth = 2)     #Contornos de países.
niveles_topografia=(50,100,500,1000,1500,2000,2500)        #Niveles de topografía.
contours=plt.contour(lon, lat, z[0,:,:],niveles_topografia, colors="black",
                     extend='both',linewidths = 0.5)       #Contornos de topografía.
plt.clabel(contours, inline=1, fontsize=10, fmt="%i")      #Líneas de topografía.
plt.title('Áreas de Interés ', size=20, loc='center', pad=8)    #Título del mapa.
gl= ax.gridlines(color="black",draw_labels=True,linestyle="--") #Líneas del grid.
gl.top_labels=False                 #Se omiten las etiquetas en la parte superior del mapa.
gl.right_labels=False               #Se omiten las etiquetas en la parte derecha del mapa.

#Cuadro para el área de la sabana.
ax.plot([lon1, lon2],[lat2, lat2], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
ax.plot([lon2, lon2],[lat1, lat2], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
ax.plot([lon1, lon2],[lat1, lat1], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
ax.plot([lon1, lon1],[lat1, lat2], 'black', transform=ccrs.PlateCarree(),linewidth = 3)

#Cuadro para el área de El Amazonas.
ax.plot([lon3, lon4],[lat4, lat4], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
ax.plot([lon4, lon4],[lat3, lat4], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
ax.plot([lon3, lon4],[lat3, lat3], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
ax.plot([lon3, lon3],[lat3, lat4], 'black', transform=ccrs.PlateCarree(),linewidth = 3)

plt.savefig('AreaInteres_t2m'  + '2011-2015' + '.png')     #Se guarda la figura.
    

#__________________________________________________________________________________________
#__________________________________________________________________________________________

#Ciclo anual.

#Se crean vectores.
meses=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre',
       'Octubre','Noviembre','Diciembre']                  #Meses para los títulos.
mesidx=['01','02','03','04','05','06','07','08',
        '09','10','11','12']               #Índices de los meses para nombrar los archivos.

for i in range(len(meses)):                                #Se crea ciclo.
    print(" ")
    print("Figura para mes: ",mesidx[i])   
    
    #Se crean los mapas.
    fig = plt.figure(figsize=(15,10))                      #Tamaño a la hoja.
    ax = fig.add_subplot(projection=ccrs.PlateCarree())    #Se indica que se va a graficar.
    ax.set_extent([-66, -80, -5, 13])                      #Coordenadas de la hoja.
    ax.coastlines('50m', linewidth = 2)                    #Contornos de continentes.
    ax.add_feature(cartopy.feature.BORDERS, linewidth = 2) #Contornos de países.
    niveles_temperatura=np.arange(15,30,1)                 #Rango de temperatura.
    mapa = plt.contourf(lon_CMA,lat_CMA,t2m_CMA_c[i,:,:],niveles_temperatura,
                        cmap="jet",extend='both')          #Contornos de temperatura.
    contours=plt.contour(lon, lat, z[0,:,:],niveles_topografia, colors="black",
                     extend='both',linewidths = 0.5)       #Contornos de topografía.
    plt.clabel(contours, inline=1, fontsize=10, fmt="%i")  #Líneas de topografía.
    plt.clim = (15,30)                                     #Límites paleta de colores.
    plt.colorbar(mapa, orientation="vertical",shrink=0.75) #Paleta de colores.
    plt.title('Temperatura Superficial (°C) \n Promedio Anual de \n' + meses[i]+ 
              ' 2011-2015', size=20, loc='center', pad=8)  #Título del mapa.
    gl= ax.gridlines(color="black",draw_labels=True,linestyle="--") #Líneas del grid.
    gl.top_labels=False             #Se omiten las etiquetas en la parte superior del mapa.
    gl.right_labels=False           #Se omiten las etiquetas en la parte derecha del mapa.

    #Cuadro para el área de la sabana.
    ax.plot([lon1, lon2],[lat2, lat2], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon2, lon2],[lat1, lat2], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon1, lon2],[lat1, lat1], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon1, lon1],[lat1, lat2], 'black', transform=ccrs.PlateCarree(),linewidth = 3)

    #Cuadro para el área de El Amazonas.
    ax.plot([lon3, lon4],[lat4, lat4], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon4, lon4],[lat3, lat4], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon3, lon4],[lat3, lat3], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon3, lon3],[lat3, lat4], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    
    plt.savefig('CicloMAnual_t2m_'  + '2011-15' + mesidx[i] + 
                '_' + meses[i] + '.png')                   #Se guarda la figura.


#__________________________________________________________________________________________
#__________________________________________________________________________________________

#Series de tiempo.

#Se crea la función con promedios espaciales.
def calcPromedioEsp(lat1, lat2, lng1, lng2, nombreSalida,archivoEntrada): 
    ifile= archivoEntrada 
    os.system("echo ")
    os.system("echo Promedios para Región limitada por:")
    os.system("echo South lat :"+str(lat1)+" ")            #Se define latitud sur.
    os.system("echo North lat :"+str(lat2)+" ")            #Se define latitud norte.
    os.system("echo West lon :"+str(lng1)+" ")             #Se define longitud sur.
    os.system("echo East lon :"+str(lng2)+" ")             #Se define longitud norte.
    os.system("rm -f tmp.nc fldmean.nc")
    os.system("cdo -f nc -r  sellonlatbox,"+str(lng1)+","+str(lng2)+","+str(lat1)+","+
              str(lat2)+" " + ifile +" " "tmp.nc")
    os.system("cdo -f nc -r  fldmean tmp.nc fldmean.nc") #Se halla valor medio con fldmean.
    os.system("rm -f tmp.nc")    
    filename = "./fldmean.nc"                              #Archivo temporal.
    h    = xr.open_dataset(filename)                       #Abrimos variable "h".
    f1   = h.t2m[:,:,:].values                             #Se cargan valores a "f1".
    fch  = h.time.values                                   #Se cargan valores a "fch". 
    ntim = fch.size
    f2 = np.reshape(f1, (ntim,1))
    aav2 = f2.flatten()                                    #Se almacena la serie de tiempo.
    h.close()                                              #Se cierra el archivo.
    
    #Se guarda la serie de tiempo del promedio temporal en un archivo ASCII:
    aav2name=nombreSalida+"_ts_mi-serie-sencilla_fch.txt"  #Se crea archivo ASCII.
    os.system("rm -f "+aav2name)    #Se borra el contenido del archivo para evitar errores.
    fl = open(aav2name,'w')
    for i in range(len(aav2)):                             #Se guardan los valores. 
        fl.write("%8.4f\n" % (aav2[i]))                      
    fl.close()                                             #Se cierra el archivo.
    os.system("rm -f fldmean.nc")
    print(" ")
    print("Serie con promedios espaciales guardada archivo ASCII")
    print(" ")
    return aav2

sabana=calcPromedioEsp(lat1,lat2,lon1,lon2,"sabana","CicloMedioAnual.nc")
amazonas=calcPromedioEsp(lat3,lat4,lon3,lon4,"amazonas","CicloMedioAnual.nc")
sabana60=calcPromedioEsp(lat1,lat2,lon1,lon2,"sabana",'t2m_mon_2011-2015.nc')
amazonas60=calcPromedioEsp(lat3,lat4,lon3,lon4,"amazonas",'t2m_mon_2011-2015.nc')

#Etiqueta de 60 meses 2011-2015.
meses_2011_2015=['Ene-2011','Feb-2011','Mar-2011','Abr-2011','May-2011','Jun-2011',
                 'Jul-2011','Ago-2011','Sep-2011','Oct-2011','Nov-2011','Dic-2011',
                 'Ene-2012','Feb-2012','Mar-2012','Abr-2012','May-2012','Jun-2012',
                 'Jul-2012','Ago-2012','Sep-2012','Oct-2012','Nov-2012','Dic-2012',
                 'Ene-2013','Feb-2013','Mar-2013','Abr-2013','May-2013','Jun-2013',
                 'Jul-2013','Ago-2013','Sep-2013','Oct-2013','Nov-2013','Dic-2013',
                 'Ene-2014','Feb-2014','Mar-2014','Abr-2014','May-2014','Jun-2014',
                 'Jul-2014','Ago-2014','Sep-2014','Oct-2014','Nov-2014','Dic-2014',
                 'Ene-2015','Feb-2015','Mar-2015','Abr-2015','May-2015','Jun-2015',
                 'Jul-2015','Ago-2015','Sep-2015','Oct-2015','Nov-2015','Dic-2015']

#Se grafica series de tiempo.
#Ciclo Medio Anual (2011-2015).
plt.figure(figsize=(15,8))                                 #Tamaño a la hoja.
plt.plot((sabana-273.15), 'red', linewidth=1.0)            #Se indica que se va a graficar.
plt.plot((amazonas-273.15), 'blue', linewidth=1.0)         #Se indica que se va a graficar.
plt.legend(["La Sabana", "El Amazonas"], loc = 1)          #Leyenda.
plt.title('Ciclo Medio Anual \n 2011-2015')                #Título del mapa.
plt.xlabel("Meses")                                        #Nombre del eje x.
plt.xticks(np.arange(0, 12, step=1), meses)
plt.yticks(np.arange(17,27,step= 0.5))                     #Límite del eje y.               
plt.ylabel("Temperatura (°C)")                             #Nombre del eje y. 
plt.grid()                                      
plt.savefig('CicloMAnual12'  + '_SabanavsAmaonas' + '.png')#Se guarda la figura
plt.show()                                                 #Se muestra la figura.

#Ciclo Anual (2011-2015)
plt.figure(figsize=(15,8))                                 #Tamaño a la hoja.
plt.plot((sabana60-273.15), 'red', linewidth=1.0)          #Se indica que se va a graficar.
plt.plot((amazonas60-273.15), 'blue', linewidth=1.0)       #Se indica que se va a graficar.
plt.legend(["La Sabana", "El Amazonas"], loc = 1)          #Leyenda. 
plt.title('Ciclo Anual \n 2011-2015')                      #Título del mapa.
plt.ylabel("Temperatura (°C)")                             #Nombre del eje y.  
plt.xticks(np.arange(0, 60, step=1), meses_2011_2015,
           rotation=90)                                    #Se indica que lleva el eje x
plt.yticks(np.arange(17,27,step= 0.5))                     #Límite del eje y.
plt.grid(color="lightgrey")                                              
plt.savefig('CicloAnual60'  + '_SabanavsAmaonas' + '.png') #Se guarda la figura.
plt.show()                                                 #Se muestra la figura.


#__________________________________________________________________________________________
#__________________________________________________________________________________________

#Promedios estacionales y promedios estacionales multianuales.

#Se crean vectores.
estaciones=['DEF','MAM','JJA','SON']                       #Estaciones para cada figura.
estidx=['01','02','03','04']                               #Índices de las estaciones.

for i in range(len(estaciones)):                           #Se crea ciclo.
    print(" ")
    print("Figura para estacion: ",estidx[i])
    
    #Creación del mapa
    fig = plt.figure(figsize=(15,10))                      #Tamaño a la hoja.
    ax = fig.add_subplot(projection=ccrs.PlateCarree())    #Se indica que se va a graficar.
    ax.set_extent([-66, -80, -5, 13])                      #Coordenadas de la hoja.
    ax.coastlines('50m',linewidth = 2)                     #Contornos de continentes.
    ax.add_feature(cartopy.feature.BORDERS, linewidth = 2) #Contornos de países
    niveles_temperatura=np.arange(15,30,1)                 #Rango de temperatura.
    mapa = plt.contourf(lon_PEM, lat_PEM, t2m_PEM_c[i,:,:],niveles_temperatura,
                        cmap="jet",extend='both')          #Contornos de temperatura.
    contours=plt.contour(lon, lat, z[0,:,:],niveles_topografia, colors="black",
                     extend='both',linewidths = 0.5)       #Contornos de topografía.
    plt.clabel(contours, inline=1, fontsize=10, fmt="%i")  #Líneas de topografía.
    plt.clim = (15,30)                                     #límites paleta de colores.
    plt.colorbar(mapa, orientation="vertical",shrink=0.75) #Paleta de colores.
    plt.title('Temperatura Superficial (°C) \n Promedio Estacional de \n' + estaciones[i]+ 
              ' 2011-2015', size=20, loc='center', pad=8)  #Título del mapa.
    gl= ax.gridlines(color="black",draw_labels=True,linestyle="--") #Líneas del grid.
    gl.top_labels=False             #Se omiten las etiquetas en la parte superior del mapa.
    gl.right_labels=False           #Se omiten las etiquetas en la parte derecha del mapa.   
    #Cuadro para el área de la sabana.
    ax.plot([lon1, lon2],[lat2, lat2], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon2, lon2],[lat1, lat2], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon1, lon2],[lat1, lat1], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon1, lon1],[lat1, lat2], 'black', transform=ccrs.PlateCarree(),linewidth = 3)

    #Cuadro para el área de El Amazonas.
    ax.plot([lon3, lon4],[lat4, lat4], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon4, lon4],[lat3, lat4], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon3, lon4],[lat3, lat3], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon3, lon3],[lat3, lat4], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    
    plt.savefig('PromedioEstacionalMultianual4'  + '2011-2015' + estidx[i] + '_' +
                estaciones[i] + '.png')                    #Se guarda la figura.
    
#Se grafica.
sabana4=calcPromedioEsp(lat1,lat2,lon1,lon2,"sabana","ProEstaMultianual4.nc") 
amazonas4=calcPromedioEsp(lat3,lat4,lon3,lon4,"amazonas","ProEstaMultianual4.nc")
sabana20=calcPromedioEsp(lat1,lat2,lon1,lon2,"sabana","PromedioEstacional20.nc")
amazonas20=calcPromedioEsp(lat3,lat4,lon3,lon4,"amazonas","PromedioEstacional20.nc") 

#Se etiquetan los promedios espaciales.
estacionesPM=['DEF-2011','MAM-2011','JJA-2011','SON-2011','DEF-2012','MAM-2012','JJA-2012',
              'SON-2012','DEF-2013','MAM-2013','JJA-2013','SON-2013','DEF-2014','MAM-2014',
              'JJA-2014','SON-2014','DEF-2015','MAM-2015','JJA-2015','SON-2015','D-2015']

 
#Promedio estacional multianual.
plt.figure(figsize=(15,8))                                 #Tamaño a la hoja.
plt.plot((sabana4-273.15), 'red', linewidth=1.0)           #Se indica que se va a graficar.
plt.plot((amazonas4-273.15), 'blue', linewidth=1.0)        #Se indica que se va a graficar.
plt.legend(["La Sabana", "El Amazonas"], loc = 1)          #Leyenda.
plt.title('Promedio Estacional Multianual \n 2011-2015')   #Título del mapa.
plt.xlabel("Meses")                                        #Nombre del eje x.
plt.ylabel("Temperatura (°C)")                             #Nombre del eje y.
plt.xticks(np.arange(0, 4, step=1), estaciones)            #Se indica que lleva el eje x.
plt.yticks(np.arange(17,27,step= 0.5))                     #Límite del eje y.
plt.grid(color="lightgrey")  
plt.savefig('ProEstMultianual4'+'_SabanavsAmaonas'+'.png') #Se guarda la figura.
plt.show()                                                 #Se muestra la figura.

#Promedio estacional.
plt.figure(figsize=(15,8))                                 #Tamaño a la hoja.
plt.plot((sabana20-273.15), 'red', linewidth=1.0)          #Se indica que se va a graficar.
plt.plot((amazonas20-273.15), 'blue', linewidth=1.0)       #Se indica que se va a graficar.
plt.legend(["La Sabana", "El Amazonas"], loc = 1)          #Leyenda.
plt.title('Promedio Estacional \n 2011-2015')              #Título del mapa.
plt.xlabel("Meses")                                        #Nombre del eje x.
plt.ylabel("Temperatura (°C)" )                            #Nombre del eje y.
plt.xticks(np.arange(0, 21, step=1),estacionesPM,
           rotation=90)                                    #Se indica que lleva el eje x.
plt.yticks(np.arange(17,27,step= 0.5))                     #Límite del eje y.
plt.grid(color="lightgrey")  
plt.savefig('PromedioEstacional21'+'_SabanavsAmaonas'+'.png') #Se guarda la figura. 
plt.show()                                                 #Se muestra la figura.


#__________________________________________________________________________________________
#__________________________________________________________________________________________

#Anomalías.

#Se grafica.
sabanaAnomalia60=calcPromedioEsp(lat1,lat2,lon1,lon2,"sabana","anomalias60.nc")
amazonaAnomalia60=calcPromedioEsp(lat3,lat4,lon3,lon4,"amazonas","anomalias60.nc")
ceros=np.array

#Anomalías mensuales.
plt.figure(figsize=(15,8))                                 #Tamaño a la hoja.
plt.plot((sabanaAnomalia60), 'r', linewidth=1.0)           #Se indica que se va a graficar.
plt.plot((amazonaAnomalia60), 'blue', linewidth=1.0)       #Se indica que se va a graficar.
plt.legend(["La Sabana", "El Amazonas"], loc = 1)          #Leyenda.
plt.title('Anomalías \n 2011-2015')                        #Título del mapa.
plt.axhline(y=0, xmin=0, xmax=60, color="black")           #Delimitacion de ejes.
plt.xlabel("Meses")                                        #Nombre del eje x.
plt.ylabel("Temperatura (°C)")                             #Nombre del eje y.
plt.xticks(np.arange(0, 60, step=1), meses_2011_2015,
           rotation=90) 
plt.yticks(np.arange(-0.6,0.8,step= 0.1))                  #Límite del eje y.
plt.grid(color="lightgrey")                                #Se indica que lleva el eje x.
plt.savefig('Anomalias60'  + '_SabanavsAmaonas' + '.png')  #Se guarda la figura.
plt.show()                                                 #Se muestra la figura. 

#Se selecciona febrero de 2012 y septiembre de 2015.
datos = xr.open_dataset('anomalias60.nc')                  #Se abre el archivo NetCDF.
t2m_A= (datos.t2m)                                         #Datos con anomalías.
lats_A = datos.latitude                                    #Datos con la latitud.
lons_A = datos.longitude                                   #Datos con la longitud. 
time_A = datos.time                                        #Datos con el tiempo.

kks = (14,57)                                              #Pasos de tiempo de interés.
kkst = ("14","57")                                         #Etiquetas.
kkofl = ("feb-2012","sep-2015")
kkoft = (" feb. 2012, "," sep. 2015, ")
kkx = range(len(kks))        #Arreglo para escoger el "for". En este ejemplo sería (0,1,2).

for i in range(len(kks)):                                  #Se crea ciclo.
    ti = kks[i]
    print(" ")
    print("Figura para mes: ",ti)
    
    #Se grafica.
    fig = plt.figure(figsize=(20,10))                      #Tamaño a la hoja.
    ax = fig.add_subplot(projection=ccrs.PlateCarree())    #Se indica que se va a graficar.
    ax.coastlines('50m',linewidth = 1.5)                   #Contornos de continentes.
    ax.add_feature(cartopy.feature.BORDERS)
    niveles_Anomalias=np.arange(-2,2.5,0.5)                #Niveles de anomalias.
    mapa=plt.contourf(lons_A, lats_A, t2m_A[ti,:,:],niveles_Anomalias,cmap="RdBu_r",
                        extend='both')                     #Contornos de anomalías.
    contours=plt.contour(lon, lat, z[0,:,:],niveles_topografia, colors="black",
                         extend='both',linewidths = 0.5)   #Contorno de topografía.
    plt.clabel(contours, inline=1, fontsize=10, fmt="%i")  #Líneas de topografía.
    plt.clim = (-2,2)                                      #Límites de paleta de colores.
    plt.colorbar(mapa, orientation="vertical",shrink=0.75) #Paleta de colores.
    otitle = "Anomalías de Temperatura Superficial \n" +kkoft[i]+"step "+kkst[i]
    plt.title(otitle, size=20, loc='center', pad=8)        #Título del mapa.
    gl= ax.gridlines(color="black",draw_labels=True,linestyle="--")  #Líneas del grid.
    gl.top_labels=False              #Se omite las etiquetas en la parte superior del mapa.
    gl.right_labels=False            #Se omite las etiquetas en la parte derecha del mapa.
   
    #Cuadro para el área de la sabana.
    ax.plot([lon1, lon2],[lat2, lat2], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon2, lon2],[lat1, lat2], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon1, lon2],[lat1, lat1], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon1, lon1],[lat1, lat2], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    
    #Cuadro para el área de El Amazonas.
    ax.plot([lon3, lon4],[lat4, lat4], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon4, lon4],[lat3, lat4], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon3, lon4],[lat3, lat3], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    ax.plot([lon3, lon3],[lat3, lat4], 'black', transform=ccrs.PlateCarree(),linewidth = 3)
    
    ofile = "Anomalia"+kkofl[i]+"_step_"+kkst[i] 
    plt.savefig( ofile + '.png')                            #Se guarda la figura.
    


 