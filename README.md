# Orgafile
Programa que reorganiza carpetas por mes/año y puede hacer una destrucción de subcarpetas para que los archivos queden reorganizados unicamente por mes/año.

En **Ayuda -> Forma de uso**, se encuentra una explicación para usar el programa.

## Explicación del código.
Este programa se basa principalmente en hacer un recorrido DFS (preorder) en Arboles n-arios.
En el caso que se use el modo de destruccion de subcarpetas, se recorre el árbol directorio hasta lelgar a una hoja (una carpeta sin subcarpetas), y los ficheros son movidos a la carpeta padre. La carpeta hijo es luego eliminada.
Si hay archivos que tenían el mismo nombre y extensión se renombra el archivo de esta manera: nombre.ext -> nombre_.ext
Al tener todos los archivos en un mismo directorio, se organizan por mes/año.

En el caso de estar en modo de NO destrucción de subcarpetas, al llegar a la carpeta hoja se realiza la organizacion por mes/año de archivos. Al terminar con las carpetas hojas se realiza la misma organizacion en la carpeta padre, hasta el directorio seleccionado.
