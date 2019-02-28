from algoritmia.datastructures.queues import Fifo
from algoritmia.datastructures.digraphs import UndirectedGraph
from labyrinthviewer import LabyrinthViewer

import sys


# Crea un grafo a partir de un fichero. Para ello crea dos listas, una de pasillos y otra de paredes.
#    Lo primero que devuelve es la lista de caminos.
#    Lo segundo que devuelve es la lista de paredes
#    Lo tercero que devuelve es el número de filas
#    Lo cuarto que de devuelve es el número de columnas

def crear_laberinto(archivo_lab) -> "(List<(T,T)>, List<(T,T)>, Int, Int)":
    pasillos = []
    desechados = []
    columna = 0  # Esto lo pongo por un warning que me da despues, que me dice que puede no estar inicializado
    with open(archivo_lab, mode='r') as file:
        fila = 0
        for linea in file:
            coordenadas_linea = linea.split(',')
            columna = 0
            for celdas in coordenadas_linea:
                if 's' not in celdas:
                    pasillos.append(((fila, columna), (fila + 1, columna)))
                else:
                    desechados.append(((fila, columna), (fila + 1, columna)))
                # end if
                if 'e' not in celdas:
                    pasillos.append(((fila, columna), (fila, columna + 1)))
                else:
                    desechados.append(((fila, columna), (fila, columna + 1)))
                # end if

                columna += 1
            # end for
            fila += 1
        # end for

    # Lo siguiente se hace por un exceso de paredes que se añaden en la última fila y columna. De esta forma los eliminamos.

    for r in range(fila):
        if ((r, columna - 1), (r, columna)) in desechados:
            desechados.remove(((r, columna - 1), (r, columna)))
    for c in range(columna):
        if ((fila - 1, c), (fila, c)) in desechados:
            desechados.remove(((fila - 1, c), (fila, c)))
    return (pasillos, desechados, fila, columna)


# Esta función devuelve un diccionario con los pares Celda(en formato (x, y)) --> Pasos(Entero)

def marca_pasos_desde(g: "UndirectedGraph<T>", v_entrada: "T") -> "Dictionary[Cells]->Int":
    CuentaPasos = {}
    CuentaPasos[v_entrada] = 0
    # Seguimos el modelo de recorre_vertices_anchura
    queue = Fifo()
    seen = set()
    queue.push(v_entrada)
    seen.add(v_entrada)
    while len(queue) > 0:
        v = queue.pop()
        for suc in g.succs(v):
            if suc not in seen:
                queue.push(suc)
                seen.add(suc)
                # Los pasos de esa casilla son uno más que los de su padre
                CuentaPasos[suc] = CuentaPasos[v] + 1
    return CuentaPasos


# Esta función busca la pared que hace mínimo el recorrido si se elimina. Devuelve esa pared.

def buscapared(paredes: "List<(T,T)>", pasosEntrada: "Dictionary[Cells]->Int",
               pasosSalida: "Dictionary[Cells]->Int") -> "(T,T)":
    u, v = paredes.pop()

    minimonumero = pasosEntrada[u] + pasosSalida[v]
    if minimonumero > pasosEntrada[v] + pasosSalida[u]: minimonumero = pasosEntrada[v] + pasosSalida[u]
    minimo = (u, v)
    for u, v in paredes:
        minimoaux = pasosEntrada[u] + pasosSalida[v]
        if minimoaux > pasosEntrada[v] + pasosSalida[u]: minimoaux = pasosEntrada[v] + pasosSalida[u]
        if minimoaux < minimonumero:
            minimonumero = minimoaux
            minimo = (u, v)
        elif minimoaux == minimonumero:
            ####--Ahora compruebo en que posición está la pared para saber con cual quedarme--####
            # minimo actual
            (y1, x1), (y2, x2) = minimo
            # nuevo minimo
            y3, x3 = u
            y4, x4 = v

            # Lo siguiente comprueba que en caso de que sean iguales, que coja la pared que esté más a la izquierda
            # y, en caso de que sean iguales, la que esté más arriba.

            if x3 < x1 or (x3 == x1 and (x4 < x2 or (x4 == x2 and y3 < y1))):
                minimo = (u, v)
                minimonumero = minimoaux
    u, v = minimo
    # Revisa el enunciado si no se entiende esto
    if v < u:
        minimo = (v, u)
    return minimo


# La siguiente función busca el camino más corto desde v_entrada a v_salida y lo devuelve como una lista de aristas.

def shortestPath(g: "UndirectedGraph<T>", v_entrada: "T", v_salida: "T") -> "List<(T,T)>":
    # Primero creo una lista de aristas:
    aristas = []
    queue = Fifo()
    seen = set()
    queue.push((v_entrada, v_entrada))
    seen.add(v_entrada)
    while len(queue) > 0:
        u, v = queue.pop()
        aristas.append((u, v))
        for suc in g.succs(v):
            if suc not in seen:
                seen.add(suc)
                queue.push((v, suc))

    # Segundo creo un diccionario de BackPointers:
    bp = {}
    for (u, v) in aristas:
        bp[v] = u

    # Recorremos el laberinto desde la salida:
    camino = []
    v = v_salida
    camino.append(v)
    while bp[v] != v:
        v = bp[v]
        camino.append(v)

    # Le damos la vuelta al camino
    camino.reverse()
    return camino


# Añade a la lista de pasillos la pared que se le pasa como parámetro. Esto es como si derribasemos esa pared

def derribaPared(aristas, pared: "<(T,T)>") -> "UndirectedGraph<T>":
    aristas.append(pared)
    return UndirectedGraph(E=aristas)


# Función que implementa la salida gráfica del laberinto.

def imprimeGraficamente(labyrinth2, u, v, caminoOriginal, caminoNuevo, action) -> "none":
    if action == '-g':
        lv = LabyrinthViewer(labyrinth2, canvas_width=1024, canvas_height=600, margin=10)
        lv.add_path(caminoOriginal, "#00FF00", -1)
        lv.add_path(caminoNuevo, "#0000FF", 1)
        lv.add_marked_cell(u, 'red')
        lv.add_marked_cell(v, 'red')
        lv.run()


# Esto es el main

if __name__ == "__main__":
    if len(sys.argv) >= 2:                                                  # Sanity check de los argumentos de entrada
        sys.setrecursionlimit(100000)
        corredores, paredes, rows, cols = crear_laberinto(sys.argv[1])       # Creamos el grafo del laberinto y colocamos
        labyrinth = UndirectedGraph(E=corredores)                           #  los valores fijos
        entrada = (0, 0)
        salida = (rows - 1, cols - 1)

        pasosEntrada = marca_pasos_desde(labyrinth, entrada)                # Creamos un diccionario de pasos desde la entrada.
        pasosSalida = marca_pasos_desde(labyrinth, salida)                  # Creamos un diccionario de pasos desde la salida.

        u, v = buscapared(paredes, pasosEntrada, pasosSalida)               # Buscamos la pared a derribar ...
        labyrinth2 = derribaPared(corredores, (u, v))                       # ... y la derribamos.

        caminoOriginal = shortestPath(labyrinth, entrada, salida)           # Creamos el camino original con la pared sin derribar
        caminoNuevo = shortestPath(labyrinth2, entrada, salida)             # y el camino con la pared derribada

        pasosEntrada2 = marca_pasos_desde(labyrinth2, entrada)              # Creamos un diccionario de pasos desde la entrada, con la pared derribada

        x, y = u                                                            # Le damos formato e imprimimos la salida de pantalla
        a, b = v
        print(str(x) + " " + str(y) + " " + str(a) + " " + str(b))
        print(pasosEntrada[salida])
        print(pasosEntrada2[salida])

        if len(sys.argv) >= 3:
            action = sys.argv[2]
            imprimeGraficamente(labyrinth2, u, v, caminoOriginal, caminoNuevo, action)      # Aquí hacemos la salida gráfica (opcional)
            
    else:
        print("Uso: entregable1.py (fichero) [-g]")                         # Qué hace en caso de que no se introduzcan las entradas que se necesitan
    # end if
