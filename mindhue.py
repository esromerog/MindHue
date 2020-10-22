#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import math
import sys
import random
import copy
try:
    from audioplayer import AudioPlayer
except:
    print("No se encontró la biblioteca de 'audioplayer'. \nFavor de instalarla o revisar la documentación para más detalles.")
    sys.exit(1)
try:
    import keyboard
except:
    print("No se encontró la biblioteca de 'keyboard'. \nFavor de instalarla o revisar la documentación para más detalles.")
    sys.exit(1)

#Equipo de desarrolladores
#SquarePair: Julio Ignacio Pérez Peñaloza | A01640078
#SoundHue: José Esteban Romero Gómez | A01639031

#Funciones para SoundHue
#Impresión del tablero
def simple_print(matrix):
    for lista in matrix:
        for elemento in lista:
            print(f"{elemento:^3}", end=" ")
        print()

#Detectar si ya está presionado el teclado
def keypress(keystroke, cp):
    #La función utiliza cp (current_press) para que no le dejes picado
    if keyboard.is_pressed(keystroke):
        if not(cp):
            cp=True
    else:
        cp=False
    return cp

#Registrar los eventos del usuario para asignarle puntuación
def score_rating(timestamps, events, time, counter, current_press):
    #Los parámetros de esta función son muy importantes, pues describen las  bases del programa
    #Timestamps - Los tiempos en los que deben ocurrir cosas
    #Events - La tecla que se debe presionar
    #Time - El tiempo actual
    #Counter - En qué evento vamos
    #Current Press - Si las teclas ya está presionada (evita que el usuario pueda dejarle picado)
    score=0
    max_score=0
    #Checa, con un margen de 0.2 segundos, si el usuario presionó la tecla correcta a tiempo
    if (counter<len(timestamps)) and math.isclose(time,timestamps[math.floor(counter)],abs_tol=0.1):
        paloma_de_ciudad=events[math.floor(counter)]
        counter+=1
        for indice in range(len(paloma_de_ciudad)):
            if paloma_de_ciudad[indice]==1:
                if indice==0:
                    max_score+=1
                    if keyboard.is_pressed("left arrow") and not(current_press[0]):
                        score+=1
                    current_press[0]=keypress("left arrow", current_press[0])
                elif indice==1:
                    max_score+=1
                    if keyboard.is_pressed("up arrow") and not(current_press[1]):
                        score+=1
                    current_press[1]=keypress("up arrow", current_press[1])
                elif indice==2:
                    max_score+=1
                    if keyboard.is_pressed("down arrow") and not(current_press[2]):
                        score+=1
                    current_press[2]=keypress("down arrow", current_press[2])
                elif indice==3:
                    max_score+=1
                    if keyboard.is_pressed("right arrow") and not(current_press[3]):
                        score+=1
                    current_press[3]=keypress("right arrow", current_press[3])
    current_press[0]=keypress("left arrow", current_press[0])
    current_press[1]=keypress("up arrow", current_press[1])
    current_press[2]=keypress("down arrow", current_press[2])
    current_press[3]=keypress("right arrow", current_press[3])

    return score,counter,max_score,current_press

#Procesa las entradas para cuando se despliegan. Convierte la lista de eventos en una lista de símbolos
def process_output(matrix):
    processed_times=[]
    for lista in matrix:
        new_list=[]
        for indice in range(len(lista)):
            if lista[indice]==1 or lista[indice]==True:
                if indice==0:
                    data=LEFT
                if indice==1:
                    data=UP
                if indice==2:
                    data=DOWN
                if indice==3:
                    data=RIGHT
            else:
                data=" "
            new_list.append(data)
        processed_times.append(new_list)
    return processed_times

#Procesa la parte de arriba del programa, es decir, que los círculos que indican qué había presionado el usuario
def process_teclado(lista):
    processed_teclado=[" "]
    for indice in range(len(lista)):
        if lista[indice]==True:
            dato=u"\u25CF"
        else:
            dato=u"\u25CB"
        processed_teclado.append(dato)
    processed_teclado.append(" ")
    return processed_teclado

#Procesa los tiempos para asegurarse que todos estén redondeados
def timestamps_prep(timestamps):
    time_final=[]
    for elemento in timestamps:
        time_final.append(round(elemento,1))
    return time_final

#Prepara los tiempos para la interpretación del tablero. El desface hace que se aparezcan antes y que lleguen arriba al momento de la acción
def time_prep(tiempo, desface):
    #Lo único que hace es sumar, pero así se puede ejecutar la suma con una sola función y si se tienen que hacer cambios, está por separado
    return (tiempo+desface)

#Lee el archivo donde está escrita la canción
def song_read(archivo):
    song=open(archivo,"r")
    events=song.readlines()
    timestamps=events[0].rstrip().split(",")
    tiempos=[]
    for elemento in timestamps:
        tiempos.append(float(elemento))
    
    preliminar=events[1].split(";")
    preliminar.pop()
    events=[]
    for row in preliminar:
        row_fnl=row.split(",")
        events.append(row_fnl)

    eventos=[]
    for linea in events:
        new_line=[]
        for elemento in linea:
            new_line.append(int(elemento))
        eventos.append(new_line)
        
    song.close()

    return tiempos, eventos
    
def render_screen(events=[[1,1,1,1]], timestamps=[1], desface=0, calibration=False,duration=5): #Esta es la función más compleja que despliega todo en pantalla y procesa los eventos del usuario
    #Creación inicial de la matriz
    #Es una función con parámetros predefinidos que son los que se utilizan para la calibración
    #Eventos es lo que ocurrirá a lo largo de la canción
    #Timestamps son los tiempos en los que ocurren estos eventos
    #Desface es lo que la calibración calcula y lo que determina qué tanto antes se tienen que proyectar los eventos para que lleguen arriba a tiempo
    #Duration determina la duración de la canción
    matrix=[]
    vertical_size=20
    line_rate=0.08
    for _ in range(vertical_size+1):
        matrix.append([" " for _ in range(6)])
    #Se imprimen las flechitas que se agreguen
    output=process_output(events)
    frames=timestamps_prep(timestamps)
    start=time.time()
    tiempo=0.0
    puntuacion=0
    event_counter=0
    cont_test=0
    cont_score=0
    currently_pressed=[False, False,False,False] #La matriz con lo que ya presionaste
    #El modo calibración para detectar el tiempo que la computadora particular tarda en que un elemento llegue de abajo hasta arriba del tablero
    if calibration:
        output=[[LEFT,UP,DOWN,RIGHT]]
        time_avrg=0
        time_init=time.time()
        cont_loops=0
    while (tiempo<duration and not(keyboard.is_pressed("esc"))): #El loop principal que se interrumpe con 'esc'
        if calibration:
            time_init=time.time()
        for i in range(vertical_size,0,-1): #Dentro de este for loop se cicla el teclado
            if keyboard.is_pressed("esc"):
                break
            matrix[0]=[" ",LEFT,UP,DOWN,RIGHT," ",f"Score: {puntuacion}"]
            last_line=[" " for _ in range(6)]
            tiempo=time.time()-start
            fnltime=time_prep(tiempo, desface)
            if (event_counter<len(frames)) and math.isclose(fnltime,frames[math.floor(event_counter)],abs_tol=0.1): #Checa los eventos que ocurren en el tablero
                for element in range(4):
                    last_line[element+1]=output[event_counter][element]
                event_counter+=1
            limpia()
            if calibration:
                print("Calibrando... ")
            tiempo=time.time()-start
            resultados=score_rating(timestamps,events,tiempo,cont_score,currently_pressed) #Checa los eventos que ocurren por parte del usuario
            currently_pressed=resultados[3]
            teclado=process_teclado(currently_pressed)
            for element in teclado:
                print(f"{element:^3}",end=" ") 
            print()
            puntuacion+=resultados[0]
            cont_score=resultados[1]
            #Append y pop eliminan dos elementos de la matriz para que se recorra todo y cicle
            matrix.append(last_line)
            matrix.pop(1)
            simple_print(matrix)
            time.sleep(line_rate) #Duerme la computadora un tiempo determinado para que cada frame tenga siento intervalo de tiempo
            tiempo=time.time()-start
        if calibration:
            time_end=time.time()-time_init
            time_avrg+=time_end
            cont_loops+=1
    if calibration:
        return time_avrg/cont_loops
    else:
        return puntuacion

#Función que se encarga de escoger una canción con el ingreso del usuario
def song_choose(decide, lista):
    #Decide es la decisión y lista es la lista de canciones
    nombre=""
    duracion=-1
    index=0
    if decide.isdigit() and int(decide)<=len(lista):
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

#Despliega el menú de canciones
def menu(lista_canciones):
    print("SoundHue – Inicio")
    print("=== Lista de canciones ===")
    for i in range(len(lista_canciones)):
        print(f"{i+1}. {lista_canciones[i][0]} - {lista_canciones[i][1]}")
    print("Para salir, teclea: Salir \n")

#Todo el menú de SoundHue
def soundhue(dato_magico, nombre):
    #Dato_mágico - El resultado de la calibración. Es un parámetro porque la calibración sólo se corre una vez al entrar al juego
    #Nombre es el nombre del usuario que se utiliza para el leaderboard
    lista_canciones=[["Mania", "Madeon", "Mania",138],
    ["Polygon Dust", "Porter Robinson","Polygon",210],
    ["Animal Crossing Theme Song","Canelita","Canelita",98],
    ["Cinema (Remix)","Skrillex", "Cinema",308],
    ["Rooftops", "Lostprophets","Rooftops",240],
    ["Misery Business", "Paramore","Paramore",200]]
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
            print(f"Ha elegido {lista_canciones[indice][0]} por {lista_canciones[indice][1]}")
            eventos=song_read("./Canciones/"+cancion+".txt")[1]
            tiempos=song_read("./Canciones/"+cancion+".txt")[0]
            print("Su canción comenzará pronto \nPresione esc para salir en cualquier momento \nCuando empiece, ajuste el volumen de sus audífonos para la mejor experiencia")
            time.sleep(3)
            player=AudioPlayer(f"./Canciones/{cancion}.mp3")
            player.volume=20
            player.play()
            puntuacion=render_screen(eventos,tiempos,dato_magico,False,duracion)
            player.close()
            highscore(nombre,str(puntuacion),lista_canciones[indice][0])
            read_scores(lista_canciones[indice][0])
            input(f"\nSu puntacion fue de {puntuacion} puntos. \nPresione ENTER para continuar \nSi tiene problemas para regresar, intente borrar este texto y posteriormente presione ENTER ")
        else:
            error=True
                
#Guarda las puntuaciones más altas en un archivo
def highscore(nombre, puntuacion,juego):
    #Recibe el nombre, la puntuación y el juego (o canción) en el que se hizo el score
     lista=[juego,nombre,puntuacion]
     indice=-1
     scores=[]
     indice_nombre=-1
     try:
          with open("highscores.txt","r") as highscores:
               for linea in highscores:
                    auxiliar=linea.strip("\n").split(",")
                    scores.append(auxiliar)
          for index in range(len(scores)):
               if juego==scores[index][0]:
                    if int(puntuacion)>int(scores[index][2]):
                         indice=index
                    if nombre==scores[index][1]:
                         indice_nombre=index
     except FileNotFoundError:
          indice=0
     if indice_nombre==-1:
          scores.insert(indice+1,lista)
     elif indice_nombre!=-1 and indice!=-1:
          scores[indice_nombre][2]=puntuacion

     with open("highscores.txt","w") as highscores:
          for linea in scores:
               highscores.write(",".join(linea)+"\n")

#Despliega las puntuaciones con base en el juego en el que están escritas
def read_scores(juego):
    print(f"Tablero de puntuaciones altas en {juego}")
    with open("highscores.txt","r") as highscores:
        cont=1
        highscores=highscores.readlines()
        for linea in reversed(highscores):
            line_fnl=linea.strip("\n").split(",")
            if line_fnl[0]==juego:
                print(f"{cont}. {line_fnl[1]}: {line_fnl[2]}")
                cont+=1
            
#Funciones de 2048

#Borra el tablero anterior para desplegar el nuevo sin necesidad de desplegar una y otra vez el tablero en la terminal
def limpia():
    if os.name == 'nt':
        os.system('cls') #Windows
    else:
        os.system('clear') #Mac/linux

#Crea el tablero con n filas y n columnas, el parámetro "n" está dado en el programa principal       
def crear_tablero(n):
    tablero=[]
    for i in range (n):
        tablero.append([])
        for j in range (n):
            tablero[i].append(0)
    return tablero

#Despliega el tablero mostrando un espacio vacío en caso de que el valor dentro de la casilla sea un cero
def mostrar_tablero(tab):
    #Recibe como parámetro el tablero
    copia_tablero = copy.deepcopy(tab)
    for i in range (len(copia_tablero)):
        for j in range (len(copia_tablero)):
            if copia_tablero[i][j] == 0:
                copia_tablero[i][j] = ' '
#Agrega guiones y lineas para darle formato al tablero                
    print('-' *((7*len(copia_tablero) + 1)))
    for i in range(len(copia_tablero)):
        for j in range (len(copia_tablero)):
            print ('| {:4}'.format(copia_tablero[i][j]), end=' ')
        print('|')
        print('-' *((7*len(copia_tablero) + 1)))
    
#Agrega en una lista todas aquellas casillas que están vacías       
def cuadro_vacio(tab):
    vacio=[]
    for i in range(len(tab)):
        for j in range (len(tab)):
            if tab[i][j] == 0:
                vacio.append([i,j])
    return vacio

#Agrega un valor aleatorio entre 2 y 4 en alguna casilla vacía
def llenar_cuadro (tab,vac):
    n = random.choice([2,2,2,2,2,2,2,2,4,4]) #Para ganar rápido    512,1024
    if len(vac)!=0:
        cuadro = random.choice(vac)
        tab[cuadro[0]][cuadro[1]] = n
    return tab

#Función para realizar movimientos a la derecha
def derecha (tab):
    movimiento = 0
    for a in range(len(tab)):
        sumas = []
        for e in range (len(tab)-1):
            for i in range (-2, -len(tab)-1,-1):
                if tab[a][i] != 0 and tab[a][i+1]==0:
                    tab[a][i+1] = tab[a][i]
                    tab[a][i] = 0
                    movimiento+=1
                elif tab[a][i] != 0 and tab[a][i] == tab[a][i+1] and i not in sumas and i-1 not in sumas:
                    tab[a][i+1] *=2
                    tab[a][i]=0
                    sumas.append(i)
                    movimiento+=1
    return movimiento

#Función para realizar movimientos a la izquierda
def izquierda (tab):
    movimiento = 0
    for a in range(len(tab)):
        sumas = []
        for e in range (len(tab)-1):
            for i in range (1, len(tab)):
                if tab[a][i] != 0 and tab[a][i-1]==0:
                    tab[a][i-1] = tab[a][i]
                    tab[a][i] = 0
                    movimiento+=1
                elif tab[a][i] != 0 and tab[a][i] == tab[a][i-1] and i not in sumas and i+1 not in sumas:
                    tab[a][i-1] *=2
                    tab[a][i]=0
                    sumas.append(i)
                    movimiento+=1
    return movimiento

#Función para realizar movimientos hacia arriba
def arriba (tab):
    movimiento = 0
    for a in range(len(tab)):
        sumas = []
        for e in range (len(tab)-1):
            for i in range (1, len(tab)):
                if tab[i][a] != 0 and tab[i-1][a]==0:
                    tab[i-1][a] = tab[i][a]
                    tab[i][a] = 0
                    movimiento+=1
                elif tab[i][a] != 0 and tab[i][a] == tab[i-1][a] and i not in sumas and i+1 not in sumas:
                    tab[i-1][a] *=2
                    tab[i][a]=0
                    sumas.append(i)
                    movimiento+=1
    return movimiento

#Función para realizar movimientos hacia abajo
def abajo (tab):
    movimiento = 0
    for a in range(len(tab)):
        sumas = []
        for e in range (len(tab)-1):
            for i in range (-2, -len(tab)-1,-1):
                if tab[i][a] != 0 and tab[i+1][a]==0:
                    tab[i+1][a] = tab[i][a]
                    tab[i][a] = 0
                    movimiento+=1
                elif tab[i][a] != 0 and tab[i][a] == tab[i+1][a] and i not in sumas and i-1 not in sumas:
                    tab[i+1][a] *=2
                    tab[i][a]=0
                    sumas.append(i)
                    movimiento+=1
    return movimiento

#Define los requerimientos para finalizar el juego en caso de que se gane
def ganar (tab):
    for i in range (len(tab)):
        for j in range(len(tab[0])):
            if tab[i][j] == 2048:
                return True

#Define los requerimientos para finalizar el juego en caso de que se pierda           
def perder (tab):
    terminar = True
    for y in range (len(tab)):
        for x in range(len(tab)-1):
            if tab[y][x] == tab[y][x+1]:
                terminar = False
    for y in range (len(tab)-1):
        for x in range(len(tab)):
            if tab[y][x] == tab[y+1][x]:
                terminar = False
    return terminar

#Despliega la información del programa y el tablero inicial, continúa desplegando el nuevo tablero cada vez que
#recibe un movimiento válido, hasta que pierda o gane el usuario
def squarepair():
    tablero=crear_tablero(4)
    vacio=cuadro_vacio(tablero)
    tablero2 = llenar_cuadro(tablero,vacio)
    usuario = 1

    desplegar = False
    cant_mov=0
    entrada=''
    while entrada!='salir':
        limpia()

        if usuario != 0:
            vacio = cuadro_vacio(tablero)
            tablero2 = llenar_cuadro(tablero,vacio)
        entrada = ''
        
        while entrada not in ('w','a','s','d','salir'):
            limpia()
            print ('''                         Bienvenido a SquarePair
    Instrucciones: El juego consiste en mover el tablero las veces necesarias
    para juntar las casillas que tengan el mismo valor, si llegas a la casilla
                            "2048" ¡¡GANAS!!
    Movimientos: para mover el tablero usarás las siguientes teclas:
                                D = Derecha
                                A = Izquierda
                                W = Arriba
                                S = Abajo''')
            print('      ---------------------COMIENZA EL JUEGO---------------------')
            mostrar_tablero(tablero)
            entrada = input('----Mueve el tablero con las teclas A/S/D/W----').lower()

        else:     
            if entrada == "w" :
                arriba(tablero)
            elif entrada == "s" :
                abajo(tablero)
            elif entrada == "a" :
                izquierda(tablero)
            elif entrada == "d" :
                derecha(tablero)
        cant_mov+=1
        if ganar(tablero) and not desplegar:
            desplegar= True
            limpia()
            mostrar_tablero(tablero)
            print ('----Felicidades, ganaste----')
            print(f'----Usaste {cant_mov} movimientos----')
            input('Presiona ENTER para continuar')
            break
        
        if len(cuadro_vacio(tablero))==0 and perder(tablero)==True:
            print ('----Perdiste, inténtalo de nuevo----')
            print(f'----Usaste {cant_mov} movimientos----')
            input('Presiona ENTER para continuar')
            break

#Programa principal
game=""
usuario=input("Jugador, ingresa tu nombre: ")
error=False
#Encoding de las flechitas para Windows y Mac
if os.name == 'nt':
    #Windows
    LEFT="←"
    UP="↑"
    DOWN="↓"
    RIGHT="→"
else:
    #macOS o Linux
    LEFT=u"\u2B05"
    UP=u"\u2B06"
    DOWN=u"\u2B07"
    RIGHT=u"\u2B95"
    

while(game!="salir"):
    limpia()
    if error:
        print("Hubo un error en tu selección – Lee las instrucciones del menú principal")
    print("""Mindhue – Inicio
    Selecciona el juego que desees comenzar:
    1. SquarePair – Desarrolla tus habilidades matemáticas en este juego de pensar
    2. SoundHue – Toca una canción y busca siempre la mejora continua

    Escribe 'Salir' para salir del programa
    """)

    game=input("Ingresa el número o el nombre del juego que desees jugar: ").lower()
    
    #Selecciona el primer juego
    if game=="1" or game=="squarepair":
        squarepair()
        error=False
    #Selecciona el segundo juego
    elif game=="2" or game=="soundhue":
        calibration=render_screen(calibration=True)
        error=False
        print("\nCalibración completada \nInicializando programa...")
        time.sleep(1)
        limpia()
        soundhue(calibration,usuario)
    #Comprueba si hubo un input diferente con error
    else:
        error=True