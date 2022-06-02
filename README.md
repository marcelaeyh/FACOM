
# Base de datos IDEAM

Este documento contiene toda la información básica necesaria sobre la base de datos construida por dos estudiantes de la Universidad de Antioquia con el fin de organizar y unificar las bases de datos del IDEAM tomadas de la página web de datos abiertos Colombia: datos.gov.co

La base de datos en formato .db contiene 13 tablas relacionadas entre sí por medio de llaves foráneas con la información de una serie de estaciones distribuidas por todo el territorio nacional, que recopilan en tiempo real datos de algunas variables meteorológicas.

A continuación se presenta una descripción de cada una de las tablas de la base de datos con sus respectivas columnas.

## Tabla categoria
### Columnas:

* **cod_categoria (integer):** Llave primaria autoincremental.

* **nombre_categoria (character varying(100)):** Categorías de las estaciones de acuerdo con su clase.


## Tabla tecnologia
### Columnas:

* **cod_tecnologia (integer):** Llave primaria autoincremental.

* **nombre_tecnologia (character varying(100)):** Tipos de estaciones de medición: convencional, automática con telemetría, automática sin telemetría.


## Tabla estado
### Columnas:

* **cod_estado (integer):** Llave primaria autoincremental.

* **nombre_estado (character varying(100)):** Condiciones de funcionamiento en las que se encuentra actualmente la estación.


## Tabla departamento
### Columnas:

* **cod_departamento (integer):** Llave primaria autoincremental.

* **nombre_departamento (character varying(100)):** Contiene los 32 departamentos de Colombia y Bogotá DC.


## Tabla zonahidrografica
### Columnas:

* **cod_zonahidrografica (integer):** Llave primaria autoincremental.

* **nombre_zonahidrografica (character varying(100)):** Zonas Hidrograficas en las que se encuentran las estaciones.


## Tabla momento_observacion
### Columnas:

* **cod_momento_observacion (integer):** Llave primaria autoincremental.

* **nombre_fecha_observacion (timestamp without time zone):** Fechas desde el 1 de enero del 2000 a las 00:00:00 horas, hasta el 1 de enero del 2031 a las 00:00:00 horas en intervalos de 10 minutos.


## Tabla variable
### Columnas:

* **cod_variable (integer):** Llave primaria autoincremental.

* **descripcion variable (character varying(100)):** Breve descripción de la variable meteorológica.

* **unidad_medida (character varying (100)):** Unidades de las variables en medición.

* **codigo_sensor (integer):** Código del sensor que realiza las mediciones.


## Tabla municipio
### Columnas:

* **cod_municipio (integer):** Llave primaria autoincremental.

* **nombre_municipio (character varying(100)):** Municipios de Colombia donde se encuentran las estaciones.

* **cod_departamento (integer):** Llave foránea que relaciona cada municipio con la tabla departamento.


## Tabla estacion
### Columnas:

* **cod_estacion (bigint):** Llave primaria a partir del código (identificador único) de cada estación.

* **nombre_estacion (character varying(100)):** Nombre identificador de las estaciones meteorológicas.

* **latitud (double precision):** Latitud geográfica de la estación en grados.
* **longitud (double precision):** Longitud geográfica de la estación en grados.
* **altitud (double precision):** Altura sobre el nivel del mar a la que se encuentra la estación en metros.
* **cod_municipio (double precision):** Llave foránea que relaciona cada estación con la tabla municipio.
* **cod_zonahidrografica (integer):** Llave foránea que relaciona cada estación con la tabla zonahidrografica.
* **cod_categoria (integer):** Llave foránea que relaciona cada estación con la tabla categoria.
* **cod_tecnologia (integer):** Llave foránea que relaciona cada estación con la tabla tecnologia.
* **cod_estado (integer):** Llave foránea que relaciona cada estación con la tabla estado.

## Tabla observacion
### Columnas:

* **cod_observacion (bigint):** Llave primaria autoincremental.
* **valor_observado (double precision):** Dato numérico resultante de la medición de alguna de las variables en las estaciones.
* **calidad_dato (integer):** Clasificación de los valores observados, 0 = Dato físicamente posible, 1 = Dato dudoso, 2 = Dato posiblemente erróneo.
 * **cod_estacion (bigint):** Llave foránea que relaciona cada valor observado con la tabla estacion.
* **cod_momento_observacion (bigint):** Llave foránea que relaciona cada valor observado con la tabla momento_observacion.
* **cod_variable (integer):** Llave foránea que relaciona cada valor observado con la tabla variable.


