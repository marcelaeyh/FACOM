import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sqlalchemy import create_engine
import numpy as np
from tqdm import tqdm  

#------------------------#----------------------------#-----------------------#
# Estaciones IDEAM
eng = 'sqlite:////Volumes/DiscoMarcela/facom/presion.db'

ideam = pd.read_csv('/Users/mac/Desktop/Article_volcano/info_volcan.csv',sep=';',usecols=([1,2,3,4,5,6]))
ideam = ideam.drop(20)
ideam = ideam.drop(19)
ideam
    
for i in tqdm(ideam.Codigo):
    q = '''
    SELECT *
    FROM presion 
    WHERE FechaObservacion 
    LIKE '01/15/2022%'
    AND CodigoEstacion == {}
    '''.format(int(i))
    
    df = pd.read_sql(q,con=eng)

    df["FechaObservacion"]=pd.to_datetime(df['FechaObservacion'],format='%m/%d/%Y %I:%M:%S %p')
    df = df.sort_values("FechaObservacion")
    
    plt.figure(figsize=(11,5))

    plt.plot(df.FechaObservacion,df.ValorObservado)
    plt.title("Presión [hPa] vs Tiempo [Horas] en "+df.Municipio.unique()[0]+" el 15 de enero de 2022" ,fontsize="16")
    plt.xlabel("Tiempo [Horas]",fontsize="16")
    plt.ylabel("Presión [hPa]",fontsize="16")
    plt.grid()
    
    plt.savefig()
#------------------------#----------------------------#-----------------------#
# Estaciones UdeA

eng_t = 'sqlite:////Users/mac/Desktop/local_facom/Volcan/db Meteoro/meteoro-turbo.db'
eng_o = 'sqlite:////Users/mac/Desktop/local_facom/Volcan/db Meteoro/meteoro-oriente.db'

query= '''
SELECT "Tiempo Sistema","Barometer" 
FROM DatosMeteoro 
WHERE "Tiempo Sistema" 
BETWEEN '2022-01-12 00:00:00.000000' AND '2022-01-17 23:59:00.000000'
'''

t1217 = pd.read_sql(query, con = eng_t)
o1217 = pd.read_sql(query,con = eng_o)

t1217["Tiempo Sistema"] = pd.to_datetime(t1217["Tiempo Sistema"],format = "%Y-%m-%d %H:%M:%S.%f")
o1217["Tiempo Sistema"] = pd.to_datetime(o1217["Tiempo Sistema"],format = "%Y-%m-%d %H:%M:%S.%f")


t1217["Tiempo Sistema"] = t1217["Tiempo Sistema"] + datetime.timedelta(hours=9,minutes=54)
o1217["Tiempo Sistema"] = o1217["Tiempo Sistema"] + datetime.timedelta(hours=5)

o =  o1217.sort_values("Tiempo Sistema")
t = t1217.sort_values("Tiempo Sistema")
o = o.reset_index(drop='index')
t = t.reset_index(drop='index')

oi = o[o["Tiempo Sistema"] >= '2022-01-15 00:00:00']
of = o[o["Tiempo Sistema"] <= '2022-01-15 23:59:59']

ti = t[(t["Tiempo Sistema"] >= '2022-01-15 00:00:00')]
tf = t[t["Tiempo Sistema"]  <= '2022-01-15 23:59:59']

o = o[oi.index[0]:of.index[-1]]
t = t[ti.index[0]:tf.index[-1]]

o = o.reset_index(drop='index')
t = t.reset_index(drop='index')

t.columns = ["fecha","presion"]
t = t.sort_values("fecha")

o.columns = ["fecha","presion"]
o = o.sort_values("fecha")

plt.figure(figsize=(15,5))

plt.plot(t.fecha,t.presion)
plt.title("Presión [hPa] vs Tiempo [Horas] en Turbo el 15 de enero 2022" ,fontsize="16")
plt.xlabel("Tiempo [Horas]",fontsize="16")
plt.ylabel("Presión [hPa]",fontsize="16")
plt.grid()

plt.figure(figsize=(15,5))

plt.plot(o.fecha,o.presion)
plt.title("Presión [hPa] vs Tiempo [Horas] en Oriente el 15 enero 2022", fontsize="16")
plt.xlabel("Tiempo [Horas]",fontsize="16")
plt.ylabel("Presión [hPa]",fontsize="16")
plt.grid()

#------------------------#----------------------------#-----------------------#
# Estaciones SIATA

est = [59,68,73,82,83,105,122,197,198,199,201,202,203,206,207,249,252,269,271,313,318,345,355,360,362,367,368,397,399,403,419,427,448,478,542]
len(est)

siata = pd.read_csv('/Users/mac/Desktop/FACOM/1_Proyectos/5_volcan/Presión estaciones SIATA/Estaciones.csv',encoding='latin1')

for i in est:
    df = pd.read_csv('/Users/mac/Desktop/FACOM/1_Proyectos/5_volcan/Presión estaciones SIATA/csv/estacion_data_presion_'+str(i)+'__20220101_20220131.csv')
    df.fecha_hora = pd.to_datetime(df.fecha_hora)
    
    # Pasar a UTC
    #df.fecha_hora = df.fecha_hora + datetime.timedelta(hours=5)
    
    df =  df.sort_values("fecha_hora")
    df = df.reset_index(drop='index')
    
    oi = df[df.fecha_hora>= '2022-01-15 00:00:00']
    of = df[df.fecha_hora <= '2022-01-15 23:59:59']
    
    df = df[oi.index[0]:of.index[-1]]
    df = df.reset_index(drop='index')

    plt.figure(figsize=(12,5))

    plt.plot(df.fecha_hora,df.Presion,label='Codigo = '+str(i))
    plt.title("Presión [hPa] vs Tiempo [Horas] en "+siata.Ciudad[siata.Ciudad[siata.Codigo == i].index[0]]+" el 15 enero 2022 (UTC-5)", fontsize="16")
    plt.xlabel("Tiempo [Horas]",fontsize="16")
    plt.ylabel("Presión [hPa]",fontsize="16")
    plt.grid()
    plt.legend()
    
    plt.savefig('/Users/mac/Desktop/FACOM/1_Proyectos/5_volcan/Article_volcano/g/SIATA/LOCAL_es/01152022-'+str(i)+'.png')
#------------------------#----------------------------#-----------------------#
# Coordenadas
coo_volcan = [-20.557107766098405, -175.38186428377438]
coo_turbo = [8.094314856114538, -76.7338430092313]
coo_oriente = [6.106154134522639, -75.38783679205099]

#distancia entre puntos

def dis_recta(x1,y1,x2,y2):
    d = np.sqrt((x2-x1)**2+(y2-y1)**2)
    return d*111.11 # Sale en km

def dis_esfe(lat1,lon1,lat2,lon2):
    r = 6378
    dlat = lat2-lat1
    dlon = lon2-lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*(np.sin(dlon/2)**2)
    d = 2*r*np.arcsin(np.sqrt(a))
    
    return d

dis_v_t = dis_esfe(coo_turbo[0]*np.pi/180,coo_turbo[1]*np.pi/180,coo_volcan[0]*np.pi/180,coo_volcan[1]*np.pi/180)
dis_t_o = dis_esfe(coo_turbo[0]*np.pi/180,coo_oriente[1]*np.pi/180,coo_turbo[0]*np.pi/180,coo_turbo[1]*np.pi/180)
dis_v_o = dis_esfe(coo_oriente[0]*np.pi/180,coo_oriente[1]*np.pi/180,coo_volcan[0]*np.pi/180,coo_volcan[1]*np.pi/180)

# tiempos

h_o = o.fecha[o.presion == o.presion.max()]
h_t = t.fecha[t.presion == t.presion.max()]
h_v = pd.to_datetime('2022-01-15 04:02:00')
h_blog = pd.to_datetime('2022-01-15 11:30:00')


def t_sec(df):
    return (df.hour*3600 + df.minute*60 +df.second)

s_o = t_sec(h_o[h_o.index[0]])
s_t = t_sec(h_t[h_t.index[0]])
s_v = t_sec(h_v)
s_blog = t_sec(h_blog)

dt_v_t = s_t - s_v
dt_t_o = s_o - s_t
dt_v_o = s_o - s_v
dt_blog = s_blog-s_v

# Velocidades

v_v_t = dis_v_t/dt_v_t*1000
v_v_o = dis_v_o/dt_v_o*1000
v_t_o = dis_t_o/dt_t_o*1000
v_blog = 9081.528/dt_blog*1000


fv = pd.DataFrame(columns = ["comparacion","distancia (km)","tiempo (seg)","velocidad (m/s)"])
fv.comparacion = ['volcan-turbo','turbo-oriente','volcan-oriente','blog']
fv['distancia (km)'] = [dis_v_t,dis_t_o,dis_v_o,9081.528]
fv['tiempo (seg)'] = [dt_v_t,dt_t_o,dt_v_o,dt_blog]
fv['velocidad (m/s)'] = [v_v_t,v_t_o,v_v_o,v_blog]

fv

# ------------------------------------------------------------------
# Análisis velocidades, estaciones seleccionadas

estaciones = pd.read_csv('/Users/mac/Desktop/FACOM/1_Proyectos/5_volcan/Article_volcano/completo_estaciones.csv')
'''
estaciones.fecha_max = pd.to_datetime(estaciones.fecha_max)

max(estaciones.fecha_max)

for i in range(27,41):
    sep = estaciones[estaciones.fecha_max == pd.to_datetime('2022-01-15 09:'+str(i)+':00')]
    if len(sep) > 0:
        sep.to_csv('/Users/mac/Desktop/FACOM/1_Proyectos/5_volcan/gif animado.png/gif nuevo/'+str(i)+'.csv')
'''
 
v_1 = estaciones['velocidad(m/s)'][1] # Turbo
v_2 = estaciones['velocidad(m/s)'][23] # Copacabana
v_3 = estaciones['velocidad(m/s)'][13] # Simijacá

t_1 = estaciones['tiempo_llegada(horas)'][1]
t_2 = estaciones['tiempo_llegada(horas)'][23]
t_3 = estaciones['tiempo_llegada(horas)'][13]

d_1 = estaciones['distancia_volcan(km)'][1]
d_2 = estaciones['distancia_volcan(km)'][23]
d_3 = estaciones['distancia_volcan(km)'][13]

fv = pd.DataFrame(columns = ["comparacion","distancia (km)","tiempo (seg)","velocidad (m/s)"])
fv.comparacion = ['volcan-turbo','turbo-copacabana','volcan-simijacá','turbo-copacabana','copacabana-simijacá']
fv['distancia (km)'] = [d_1,d_2,d_3,d_2-d_1,d_3-d_2]
fv['tiempo (seg)'] = [t_1,t_2,t_3,t_2-t_1,t_3-t_2]
fv['velocidad (m/s)'] = [v_1,v_2,v_3,(d_2-d_1)/(t_2-t_1),(d_3-d_2)/(t_3-t_2)]

fv