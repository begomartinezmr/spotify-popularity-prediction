## Programa final

El programa final está únicamente compuesto por los dos scripts *spotipy_releases.py* y *spotify_processing.py*. Recordemos los pasos para su ejecución:

 1. Primero ejecutamos el script *spotify_releases.py* como un script python ordinario (asumiendo que se cumplen los requisitos de autenticación de spotify en portada)
 ```
 Terminal 1 $ python3 spotipy_releases.py
 ```
 2. Cuando el primer proceso quede a la espera de una conexión TCP, lanzamos el script *spotify_processing.py* como un *spark job*
  ```
 Terminal 2 $ spark-submit spotify_processing.py
 ```

## La carpeta *unused alternative model* 

Está carpeta no forma parte del programa final, simplemente son modelos alternativos a la regresión lineal sobre la popularidad tal y como se explica en la portada de este repositorio
