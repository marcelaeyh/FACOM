#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 23:00:54 2022

@author: luisa
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:39:16 2018
Código para lectura y procesamiento de datos de la estación meteorológica del
ITM. A partir de datos cada 5 min, se entregan archivos con series horarias y
diarias para las variables de interés.
@author: vasquez
"""

#Librerías útiles
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import datetime
import os
import windrose #https://github.com/python-windrose/windrose
from windrose import WindroseAxes


path = '/home/alejandro/WebUdeA/Estacion_UdeA-Oriente/'
metvar = 'Wind Speed' # La variable a extraer por este script
metvar2 = "Wind Direction"
qctrlmx = 1000.0  # Máximo valor aceptable
qctrlmn = -1.0    # Mínimo valor aceptable
varyaxis = "Vspd (km/h)" # En gráfica
pltymx = 10.0      # En gráfica
pltymn = 0.0       # En gráfica 
varofile = "WRose_"    # En archivo de salida


# Leyendo los tres archivos con fechas más recientes:
os.system("rm "+path+"/zzListaDatos*.txt")
os.system("ls -d "+path+"/DatosEstacion* > "+path+"/zzListaDatos.txt")
os.system("tail -3 "+path+"/zzListaDatos.txt > "+path+"/zzListaDatos3Dias.txt")
ifile = ["file1","file2","file3"]
f = open('zzListaDatos3Dias.txt', 'r')
ii=0
for line in f:
    #print repr(line)
    infilei = line.strip()
    #print infilei    
    ifile[ii] = infilei
    ii = ii + 1
    

# Seleccionando solo la variable de interés metvar 
# y uniendo la información en los tres archivos leidos
dfi1 = pd.read_csv(ifile[0], usecols=['Tiempo Sistema',metvar,metvar2])   
dfi1.rename(columns={metvar:'wspd'}, inplace=True)
dfi1.rename(columns={metvar2:'wdir'}, inplace=True)
dfi1.rename(columns={'Tiempo Sistema':'Fecha'}, inplace=True)
# Seleccionando cosas
spd1 = np.array(dfi1.wspd)*1.6
dir1 = np.array(dfi1.wdir)
fchs1 = dfi1.Fecha


dfi2 = pd.read_csv(ifile[1], usecols=['Tiempo Sistema',metvar,metvar2])   
dfi2.rename(columns={metvar:'wspd'}, inplace=True)
dfi2.rename(columns={metvar2:'wdir'}, inplace=True)
dfi2.rename(columns={'Tiempo Sistema':'Fecha'}, inplace=True)
# Seleccionando cosas
spd2 = np.array(dfi2.wspd)*1.6
dir2 = np.array(dfi2.wdir)
fchs2 = dfi2.Fecha

dfi3 = pd.read_csv(ifile[2], usecols=['Tiempo Sistema',metvar,metvar2])   
dfi3.rename(columns={metvar:'wspd'}, inplace=True)
dfi3.rename(columns={metvar2:'wdir'}, inplace=True)
dfi3.rename(columns={'Tiempo Sistema':'Fecha'}, inplace=True)
# Seleccionando cosas
spd3 = np.array(dfi3.wspd)*1.6
dir3 = np.array(dfi3.wdir)
fchs3 = dfi3.Fecha
        
fig=plt.figure(figsize=(12,12))     #Define figura con cierto tamano
ax1 = fig.add_subplot(221,projection='windrose')    #Reserva el primer espacio en una figura que esta dividida en 4 (2filas X 2columnas) y llama la subrutina windrose que va a ser usada
ax1.bar(dir1, spd1, bins=np.arange(0, 10, 1),)    #Grafica rosa de vientos con barras de diferentes colores dependiendo la velocidad (cada 5m/s de 0 a 40)
ax1.set_title('Dia 1')
#ax1.legend(loc=4)    

ax2 = fig.add_subplot(222,projection='windrose')    #Reserva el segundo espacio en una figura que esta dividida en 4 y llama la subrutina windrose que va a ser usada
ax2.bar(dir2, spd2, bins=np.arange(0, 10, 1))
ax2.set_title('Dia 2')
ax2.set_legend(loc='best', bbox_to_anchor=(0.2, -0.2, 0.5, 0.),fontsize=25,title='Velocidad [km/h]') #Define la posicion de la leyenda (va a ocupar la cuarta posicion de la figura dividida en 4) tomando los valores de esta grafica (el intervalo es el mismo para todos y es suficiente con usar una sola)

ax3 = fig.add_subplot(223,projection='windrose')    #Reserva el tercer espacio en una figura que esta dividida en 4 y llama la subrutina windrose que va a ser usada
ax3.bar(dir3, spd3, bins=np.arange(0, 10, 1))
ax3.set_title('Dia 3')
#ax3.set_legend()

#outfig = varofile + '3dias_' + diaplt + '_HoraCorr.png'
outfig = varofile + '3dias_' + 'diaTest' + '_HoraCorr.png'
plt.savefig(outfig, dpi=300, bbox_inches='tight')
#plt.savefig('windrose3dias.png')    #Crea archivo de salida en formato jpg    
