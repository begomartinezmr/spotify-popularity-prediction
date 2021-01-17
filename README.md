# Spotify Pop Predictor
Proyecto final de la asignatura Cloud Computing and Big Data de la Universidad Complutense de Madrid (Curso 2020-21)

## Introducción
La idea de la aplicación es predecir en streaming la popularidad de las canciones de las *new_releases* de Spotify. Para ello haremos uso de un modelo de regresión lineal previamente entrenado a partir de un [dataset de unas 160k canciones](https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks) que contienen diferentes parámetros y métricas de los distintos temas.

## El modelo y los datos
Para crear el modelo de predicción, partimos de un [dataset que contine unas 160k canciones](https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks) alojadas en Spotify cuyo año de publicación va desde 1921 hasta la actualidad. Cada canción viene descrita en el dataset por las siguientes variables: `id`, `name`, `artists`, `year`, `valence`, `acousticness`, `danceability`, `duration_ms`, `energy`, `explicit`, `instrumentalness`, `key`, `liveness`, `loudness`, `mode`, `popularity`, `release_date`, `speechiness` y `tempo`. Podemos observar que se trata de una serie de variables y métricas muy heterogénes y quizá no todas sean relevantes para nuestro modelo de regresión. Por ello conviene relizar un estudio y limpieza previa del conjunto para conservar solo aquellas veriables útiles para el predictor. 

 ### Estudio y limpieza 
 A grandes rasgos podemos diferenciar dos grandes tipos de columnas en el conjunto: `las variables no numéricas` (describen atributos de la pista como su nombre, artista, identificador) y `las variables numéricas` (describen diversas métricas del sonido, duración o incluso otros atributos como el año de lanzamiento). Para nuestro modelo de regresión, utilizaremos `las variables numéricas`. 
 Es conveniente además conocer cuáles de estás métricas guardan un mayor grado de correlación con la variable a predecir ya que así nuestro modelo de regresión ofrecerá resultados más precisos y fiables que si utilizamos variables menos significativas. ![] (https://github.com/begomartinezmr/spotify-popularity-study/blob/main/datasets/popularity_corr.png)

## La aplicación
La aplicación está basada en un modelo cliente-servidor comunicados a través de un socket TCP. La idea es tener un proceso conectado a la interfaz python de spotify [(spotipy)](https://spotipy.readthedocs.io/en/2.16.1/#module-spotipy.client) para recibir los álbumes *new_releases* a través de ella y poder enviarlos al segundo proceso en formato csv para que este pueda realizar la predicción a traves del modelo de regresión. A continuación exponemos los detalles de ambos scripts:

 - **spotify_releases** es el proceso que se conecta con la interfaz de spotify y recupera la información de las *new_releases*. Éste método recupera albumes enteros, por lo que el proceso debe encargarse de recuperar las pistas que conforman cada album. Una vez las recupera todas, las envía al proceso **spotify_processing** como una tabla de pistas con sus correspondiente atributos en formato csv. Cabe destacar que tan solo recuperaremos aquellos atributos que utiliza nuestro modelo de predicción que detallamos anteriormente.

- **spotify_processing** es el proceso que conecta con **spotify_releases** para recibir los nuevos albumes como tablas de pistas, las formatea adecuadamente y las pasa por el modelo de predicción. Antes de conectar con **spotify_releases**, el proceso crea y entrena el modelo a partir de los datos de *spotify_model.csv*.

## La interfaz Spotipy
Spotipy es una interfaz python que ofrece Spotify a los desarrolladores para tener completo acceso a los datos que ofrece Spotify. Para poder utilizarla, se requiere un proceso previo de autenticación mediante un identificador del cliente y una clave secreta que se pueden pasar como argumento del objeto *SpotifyClientCredentials()* o colocarse como variables de entorno en que se ejecuta el proceso. Para obtener dichas claves se deben seguir los siguientes pasos:

 1. Registar una cuenta de usuario ordinario de Spotify (o iniciar sesión en una previamente existente)
 2. Entrar en la plataforma de [desarrolladores de Spotify](https://developer.spotify.com/dashboard)
 3. Seleccionar el botón `Create an app` y especificar un nombre y una descripción de la aplicación así como aceptar todos los términos de uso
 4. Una vez creada la aplicación en el developer dashboard de spotify, tan solo tenemos que consultar las claves asociadas a ella
