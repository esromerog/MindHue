# Casos de Prueba y Documentación - MindHue
###### Esteban Romero | A01639031
Este documento estará divido en las distintas secciones donde hay interacción con el usuario. Aquí se explica cada caso de prueba en los distintos niveles de interacción que fueron desarrollados por mí. 
***
## Antes de empezar
### Instalar las dependencias
*Importante:* el programa fue desarrollado en macOS. En Windows se conoce un error con el que las canciones sólo despliegan las primeras notas y es por ello que la experiencia del usuario puede ser muy diferente.
Video del desarrollo: https://youtu.be/x0U5TzOLUlI

Antes de comenzar y poder correr el código como usuario, es importante tomar en cuenta que se deben instalar las dos bibliotecas utilizadas para el proyecto. Durante el proceso se trabajó en un ambiente virtual, sin embargo, se asume que el usuario tendrá acceso a Python 3 para instalar las bilbiotecas y que manejará sus propios ambientes de desarrollo. Las únicas dos bibliotecas adicionales son `keyboard` y `audioplayer`. Se pueden instalar por separado en el Command Prompt (Windows) o Terminal (macOS) usando:
* `pip install keyboard`
* `pip install audiplayer`

Si Command Prompt o Terminal ya está en el directorio, también es posible:
* `pip install -r requirements.txt`

#### Ejecutar el programa
###### macOS: Error de ejecución
Es posible que se desplieguen errores al correr el programa en un sistema operativo que no le dé aceso al teclado. Para evitarlo, solamente se puede correr como administrador. Una vez que Terminal haya navegado al directorio del archivo, en macOS esto se realiza de la siguiente forma:
* `sudo python3 mindhue.py`

Cuando se haga esto, Terminal pedirá permiso para las funciones de accesibilidad y se tendrá que otorgar desde las preferencias del sistema.
###### macOS: Error en las bibliotecas
Otro de los errores que pueden ocurrir durante la instalación es con un módulo llamado `AppKit`. Este error surge debido a que Python tiene múltiples instalaciones de un mismo módulo. Para arreglarlo, se puede crear un ambiente virtual o activar el que viene incluido (macOS) utilizando, una vez en el path:
* `source env/bin/activate`

Generalmente es mejor, sin embargo, que el usuario maneje sus propias dependencias.
***
## Menú Principal
Este es el código del menú principal con su respectivo debugging. Es importante fijarse en múltiples elementos:
* `input` del codigo
* Variable `error`

```python
nombre=input("Jugador, ingresa tu nombre: ")
error=False
while(juego!="salir"):
    limpia()
    if error:
        print("Hubo un error en tu selección – Lee las instrucciones del menú principal")
    print("""Mindhue – Inicio
    Selecciona el juego que desees comenzar:
    1. SquarePair – Desarrolla tus habilidades matemáticas en este juego de pensar
    2. SoundHue – Toca una canción y busca siempre la mejora continua

    Escribe 'Salir' para salir del programa
    """)

    juego=input("Ingresa el número o el nombre del juego que desees jugar: ").lower()

    if juego=="1" or juego=="squarepair":
        squarepair()
        error=False

    elif juego=="2" or juego=="soundhue":
        calibration=render_screen(calibration=True)
        error=False
        print("\nCalibración completada \nInicializando programa...")
        time.sleep(2)
        limpia()
        soundhue(calibration,nombre)
    else:
        error=True
```
##### Entrada
La entrada principal que se debe comprobar para que caiga dentro de los casos de prueba es:
```python 
input("Ingresa el número o el nombre del juego que desees jugar: ").lower()
``` 
##### Comprobación
Se puede bien escribir el nombre del juego o el número, puesto que los condicionales están diseñados para ambos.
```python
if juego=="1" or juego=="squarepair"
```
##### Salida
Otra de las opciones es *salir* y llega a ser útil para terminar el programa. El condicional while corre siempre que juego no sea salir.
```python
while(juego!="salir"):
```

*Notas de los ingresos*
* El `lower()` es muy útil para descartar las mayúsculas cuando el usuario escribe el nombre del juego.
* Si se ingresa un número fuera del rango, como lo sería `3` o `0`, despliega el mensaje de error la próxima iteración del menú. Las formas en las que sí acepta un ingreso válido
* Si se ingresa un string que no corresponde a los nombres de los juegos, también despliega ese error en el menú

***
## Submenú Específico de SoundHue
El código para el submenú de SoundHue es similar al código principal con respecto a la lógica del ciclo.
* Se calibra el programa en el menú general una sola vez.
* Se utiliza un `while` para verificar la salida del programa
* Se despliega un mensaje de **error** al principio del menú si la opción pasada fue inválida.
```python
def soundhue(dato_magico, nombre):
    lista_canciones=[["Mania", "Madeon", "Mania",138],
    ["Polygon Dust", "Porter Robinson","Polygon",30],
    ["Animal Crossing Theme Song","Canelita","Canelita",0],
    ["Through the Fire and Flames","Dragonforce""FAF",0],
    ["Cinema","Skrillex", "Cinema",0]]

    decision=""
    error=False
    while (decision!="salir"):
        limpia()
        if error:
            print("La opción que usted ingresó fue inválida")
        menu(lista_canciones)
        decision=input("Escoge la canción escribiendo el número o el nombre: ").lower()
        cancion=song_choose(decision, lista_canciones)[0]
        duracion=song_choose(decision, lista_canciones)[1]
        indice=song_choose(decision, lista_canciones)[2]
        if duracion>0:
            error=False
            #Aquí va el código referente al juego
            input(f"\nSu puntacion fue de {puntuacion} puntos. \nPresione ENTER para continuar \nSi tiene problemas para regresar, intente borrar este texto y posteriormente presione ENTER")
        else:
            error=True
```
##### Input
El ingreso puede bien ser un valor número que referencíe un índice de la lista o el nombre de la canción como se despliega en el menú. No toma en cuenta mayúsculas debido al `lower()`

##### Verificación
La verificación la lleva a cabo la función `song_choose`, que se basa en la lista de canciones para verificar si la decisión estuvo ahí adentro. Cuando `song_choose` regresa un valor erróneo, la duración de la canción se regresará como `-1` y el resto del programa no corre.  Se explorará más este concepto en la siguiente sección.

##### Irregularidades
Es importante mencionar el último input cuando termina el juego ya sea con la tecla *esc* o bien finalizando la canción.
```python
input(f"\nSu puntacion fue de {puntuacion} puntos. \nPresione ENTER para continuar \nSi tiene problemas para regresar, intente borrar este texto y posteriormente presione ENTER")
```
Cuando se corre el programa principal, cada movimiento del keyboard, además de registrarse para el juego, se queda como un valor *"fantasma"*, es decir, que no se puede ver, pero que está en el buffer del `input()` y llega a ocasionar que no se registre. Cuando se selecciona un elemento del buffer, el input ya puede ser procesado por Python. Es mejor realizar este input adicional para que el menú principal no se vea afectado.
***
## Verificación de la validez del ingreso
La función `song choose` es la responsable de verificar la validez de la entrada. Es una función corta que únicamente recibe dos parámetros:
* `decide` -  El resultado del input del usuario
* `lista` - La lista de canciones

La función a fin de cuentas divide los ingresos de la siguiente forma:
* Si es un *valor numérico*
* Si es el *nombre de la canción*
* Si es *inválido*
```python
def song_choose(decide, lista):
    nombre=""
    duracion=-1
    index=0
    if decide.isdigit() and int(decide)<len(lista):
        index=int(decide)-1
        nombre=lista[index][2]
        duracion=lista[index][3]
    else:
        for linea in lista:
            for elemento in linea:
                if isinstance(elemento, str) and elemento.lower()==decide:
                    index=lista.index(linea)
                    nombre=linea[2]
                    duracion=linea[3]
    return nombre, duracion, index
```
Las salidas de la función son las que se requieren para correr el juego:
* `nombre` - El nombre del archivo de la canción (los archivos no pueden tener espacios, es por eso que se utiliza otro nombre)
* `index` - Esto determina el índice en el que está la decisión, es decir, el índice de la lista de la canción en la matriz. Se utiliza cuando se busca el nombre completo de la canción y no del archivo.
* `duracion` - Un argumento muy importante y necesario, ya que le dice al programa la duración de cada canción.

##### Categorización de las entradas
Los dos casos para encontrar el ingreso del usuario en la lista de canciones. Si ninguno de estos pasa `duración`continuará siendo `-1` y el programa lo ignorará en el ciclo general y mostrará un error.
###### Valor numérico
Cuando el ingreso del usuario es un valor numérico.
```python
if decide.isdigit() and int(decide)<len(lista):
```
Primero verifica si es un dígito a través de la función `isdigit()`. Si lo es, el `if` puede pasar al segundo argumento que checa si está dentro del rango de longitud de la lista. 
* Los valores no-numéricos pasarán a la siguiente función
* Un número negativo pasará como `False` en `isdigit()`
* Un numéro más allá de la longitud de la lista tampoco será aceptado.
```python
index=int(decide)-1
```
Posteriormente, declara el índice como el valor que ingresaste menos uno, ya que el usuario verá la lista empezando desde `1`, no desde `0` como Python referencía índices.

###### Nombre de la canción
Cuando el usuario ingresa el nombre de la canción la función se vuelve más compleja.
```python
for linea in lista:
    for elemento in linea:
```
Este for loop únicamente recorre la lista de canciones elemento por elemento para poder comparar la decisión con cada uno de las canciones en la lista. Se utiliza este método por si el usuario escribe una abreviatura que podría corresponder al nombre de la canción.
```python
if isinstance(elemento, str) and elemento.lower()==decide:
```
Para este if se tienen que analizar lo que se busca. 
* `isinstance()` - Se verifica si el elemento tiene que ser un string.
* `elemento.lower()==decide` - Si es igual a la decisión del usuario.

Si estos dos argumentos pasan, se encontrará el índice de la línea en la que iba el ciclo y el `nombre` y la `duración` se definirán en términos de valores de la lista y el juego estará listo para jugarse. Dentro del juego, lo único que se puede hacer es presionar *esc* para salir en cualquier momento o bien jugar normalmente.
***
