# Spotify Pop Predictor
Proyecto final de la asignatura Cloud Computing and Big Data de la Universidad Complutense de Madrid (Curso 2020-21)

## Introducción
La idea de la aplicación es predecir en streaming la popularidad de las canciones de las *new_releases* de Spotify. Para ello haremos uso de un modelo de regresión lineal previamente entrenado a partir de un [dataset de unas 160k canciones](https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks) que contienen diferentes parámetros y métricas de los distintos temas.

## El modelo y los datos
Para crear el modelo de predicción, partimos de un [dataset que contine unas 160k canciones](https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks) alojadas en Spotify cuyo año de publicación va desde 1921 hasta la actualidad. Cada canción viene descrita en el dataset por las siguientes variables: `id`, `name`, `artists`, `year`, `valence`, `acousticness`, `danceability`, `duration_ms`, `energy`, `explicit`, `instrumentalness`, `key`, `liveness`, `loudness`, `mode`, `popularity`, `release_date`, `speechiness` y `tempo`. Podemos observar que se trata de una serie de variables y métricas muy heterogénes y quizá no todas sean relevantes para nuestro modelo de regresión. Por ello conviene relizar un estudio y limpieza previa del conjunto para conservar solo aquellas veriables útiles para el predictor. 

 ### Estudio y limpieza 
 A grandes rasgos podemos diferenciar dos grandes tipos de columnas en el conjunto: `las variables no numéricas` (describen atributos de la pista como su nombre, artista, identificador) y `las variables numéricas` (describen diversas métricas del sonido, duración o incluso otros atributos como el año de lanzamiento). Para nuestro modelo de regresión, utilizaremos `las variables numéricas`. 
 Es conveniente además conocer cuáles de estás métricas guardan un mayor grado de correlación con la variable a predecir ya que así nuestro modelo de regresión ofrecerá resultados más precisos y fiables que si utilizamos variables menos significativas. 
 
 ![](https://github.com/begomartinezmr/spotify-popularity-study/blob/main/datasets/popularity_corr.png)
 
 Observamos que con mucha diferencia la variable que más correlacionada está con la popularidad de una pista es, con diferencia `year`, seguida de otras que tambien lo están en manor medida como `energy`, `acousticness` o `loudness`. El resto de variables guardan un grado de correlación con la popularidad bastante residual, por lo que será conveniente descartarlos de cara a la construcción de nuestro modelo ya que quizá sean perjudiciales. 
 
 ## El modelo 
 Optamos finalmente por utilizar un modelo de regresión lineal múltiple para establecer una relación estadística entre las variables seleccionadas y la popularidad. En este caso hemos optado por utilizar el modelo [LinearRegression de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html). Su funcionamiento es simple, genera el modelo con el metodo *fit(x,y)* a partir de una matriz de datos (cada fila describe una pista mediante las variables elegidas) y un vector de etiquetas que en nuestro caso contiene la popularidad de cada pista descrita en la matriz ya que esta es la variable objetivo. Una vez entrenado, podemos medir el error medio de sus predicciones comparandolas con las etiquetas originales. Con el modelo ya genereado, el método *predict(x)* devolverá las etiqutas que el modelo asocie a cada nueva pista descrita parámetro. Además, podemos usar el error medio del modelo para emitir nuestra predicción como un rango en vez de un único valor (*predicción ± error_medio*).  

## La aplicación
La aplicación está basada en un modelo cliente-servidor comunicados a través de un socket TCP. La idea es tener un proceso conectado a la interfaz python de spotify [(spotipy)](https://spotipy.readthedocs.io/en/2.16.1/#module-spotipy.client) para recibir los álbumes *new_releases* a través de ella y poder enviarlos al segundo proceso en formato csv para que este pueda realizar la predicción a traves del modelo de regresión. A continuación exponemos los detalles de ambos scripts:

 - **spotipy_releases** es el proceso que se conecta con la interfaz de spotify y recupera la información de las *new_releases*. Éste método recupera albumes enteros, por lo que el proceso debe encargarse de recuperar las pistas que conforman cada album. Una vez las recupera todas, las envía al proceso **spotify_processing** como una tabla de pistas con sus correspondiente atributos en formato csv. Cabe destacar que tan solo recuperaremos aquellos atributos que utiliza nuestro modelo de predicción que detallamos anteriormente.

- **spotify_processing** es el proceso que conecta con **spotify_releases** para recibir los nuevos albumes como tablas de pistas, las formatea adecuadamente y las pasa por el modelo de predicción. Antes de conectar con **spotify_releases**, el proceso crea y entrena el modelo a partir de los datos de *spotify_model.csv*.

## La interfaz Spotipy
Spotipy es una interfaz python que ofrece Spotify a los desarrolladores para tener completo acceso a los datos que ofrece Spotify. Para poder utilizarla, se requiere un proceso previo de autenticación mediante un identificador del cliente y una clave secreta que se pueden pasar como argumento del objeto *SpotifyClientCredentials()* o colocarse como variables de entorno en que se ejecuta el proceso. Para obtener dichas claves se deben seguir los siguientes pasos:

 1. Registar una cuenta de usuario ordinario de Spotify (o iniciar sesión en una previamente existente)
 2. Entrar en la plataforma de [desarrolladores de Spotify](https://developer.spotify.com/dashboard)
 3. Seleccionar el botón `Create an app` y especificar un nombre y una descripción de la aplicación así como aceptar todos los términos de uso
 4. Una vez creada la aplicación en el developer dashboard de spotify, tan solo tenemos que consultar las claves asociadas a ella

## Utilización de la aplicación
Como ya detallamos en el anterior apartado *La aplicación*, el programa está formado por dos scripts de python comunicados a través de un socket, por lo que necesitaremos dos terminales en las que ejecutar cada uno de ellos.
 1.Para poder ejecutar la aplicación es necesario instalar las siguientes dependencias:
 - **PySpark** siguiendo este [tutorial](https://medium.com/tinghaochen/how-to-install-pyspark-locally-94501eefe421)
 - [**Spotipy**](https://github.com/plamere/spotipy/tree/2.16.1) , librería de python para conectar con la API de Spotify.
 ```
 $ pip install spotipy 
 ```
 - [**SKlearn**](https://scikit-learn.org/stable/install.html) , librería para construir los modelos de Machine Learning.
 ```
 $ pip install  -U scikit-learn 
 ```
 - [**Pandas**](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html) , librería de Python para el análisis de datos.
 ```
 $ pip install pandas 
 ```

 2. Primero ejecutamos el script *spotify_releases.py* como un script python ordinario (asumiendo que se cumplen los requisitos de autenticación de spotify detallados en el apartado anterior)
 ```
 Terminal 1 $ python3 spotipy_releases.py
 ```
 3. Cuando el primer proceso quede a la espera de una conexión TCP, lanzamos el script *spotify_processing.py* como un *spark job*
  ```
 Terminal 2 $ spark-submit spotify_processing.py
 ```
## Modelos alternativos
Partiendo de un esquema similar en el que recibimos en streaming nuevas canciones, podemos proponer otros modelos alternativos con los que trabajar con los datos que no sean la prediccion de popularidad mediante regresión lineal que hemos implementado.  

 ### Clasificación binaria *explicit* mediante Regresión Logística
 En este modelo nos valemos de la libería nativa de Spark [Spark-ML](https://spark.apache.org/docs/2.0.0-preview/ml-guide.html) , para construir y entrenar el modelo. Tratamos de predecir si una canción contiene contenido explícito (que no es recomendable para niños o lenguaje ofensivo) o no. Para ellos hemos utilizado las columnas `valence`,`year`,`acousticness` y `danceability` del dataset y la característica a predecir es `explicit`, las pruebas muestran en torno a un 75% de acierto.

 ### Clasificación binaria de la popularidad mediante redes neuronales
 Para este modelo hemos empleado Scikit-Learn, hemos tranformado con ayuda de la función "popularidad", los valores de la polularidad que van del rango 0 a 100 en ceros o unos, en función de si este valor es mayor o menor que 30. De esta forma transformamos el problema de clasifación de 100 clases a 2 clases. Con este modelo se obtuvo un porcentaje de acierto en torno al 99%.

 ### Support vector machines SVM con kernel "gaussiano"
 Hemos empleaso Scikit-Learn con este modelo y se pretende predecir la popularidad y clasificarla en 100 clases (0...100). Con este modelo se obtuvo un porcentaje de acierto en torno al 60%.

 ## Resultados
 ### Terminal 1: Nuevos Lanzamientos de Spotify
 Waiting for TCP connection...
 
Connection established. Starting to receive new releases...

--------- NEW ALBUM RELEASED ---------

- Name: Utopia

- Year: 2019

- Tracks:

--- Intro

--- Canalla

--- Payasos

--- La Demanda

--- Millonario

--- El Beso Que No Le Di

--- ileso

--- Amor Enterrado

--- Me Quedo

--- Los Últimos

--- Años Luz

--- Bellas (feat. Romeo Santos)

--- Inmortal

------------------------------------------
 


 ## Autores
Este proyecto ha sido desarrollado por cuatro estudiantes de Ingeniería Informática de la Facultad Informática de la universidad Complutense de Madrid.

- Iago Zamorano - [Github](https://github.com/iagger)

- José Jímenez - [Github](https://github.com/jotajjjj)

- David Cantador - [Github](https://github.com/Rehis)

- Begoña Martínez - [Github](https://github.com/begomartinezmr)
