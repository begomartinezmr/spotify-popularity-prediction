# Spotify Pop Predictor

## Introducción
La idea de la aplicación es predecir en streaming la popularidad de las canciones de las *new_releases* de Spotify. Para ello haremos uso de un modelo de regresión lineal previamente entrenado a partir de un [dataset de unas 160k canciones](https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks) que contienen diferentes parámetros y métricas de los distintos temas.

## El modelo y los datos


## La aplicación
La aplicación está basada en un modelo cliente-servidor comunicados a través de un socket TCP. La idea es tener un proceso conectado a la interfaz python de spotify [(spotipy)](https://spotipy.readthedocs.io/en/2.16.1/#module-spotipy.client) para recibir los álbumes *new_releases* a través de ella y poder enviarlos al segundo proceso en formato csv para que este pueda realizar la predicción a traves del modelo de regresión. A continuación exponemos los detalles de ambos scripts:

 - **spotify_releases** es el proceso que se conecta con la interfaz de spotify y recupera la información de las *new_releases*. Éste método recupera albumes enteros, por lo que el proceso debe encargarse de recuperar las pistas que conforman cada album. Una vez las recupera todas, las envía al proceso **spotify_processing** como una tabla de pistas con sus correspondiente atributos en formato csv. Cabe destacar que tan solo recuperaremos aquellos atributos que utiliza nuestro modelo de predicción que detallamos anteriormente.

- **spotify_processing** es el proceso que conecta con **spotify_releases** para recibir los nuevos albumes como tablas de pistas, las formatea adecuadamente y las pasa por el modelo de predicción. Antes de conectar con **spotify_releases**, el proceso crea y entrena el modelo a partir de los datos de *spotify_model.csv*.

## La interfaz Spotipy
Spotipy es una interfaz python que ofrece Spotify a los desarrolladores para tener completo acceso a los datos que ofrece Spotify. Para poder utilizarla, se requiere un proceso previo de autenticación 
