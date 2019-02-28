import sys
import operator
from copy import deepcopy
from typing import *

Folleto = Tuple[int, int, int]  # (num_folleto, anchura, altura)
PosicionFolleto = Tuple[int, int, int, int]  # (num_folleto, num_hoja, pos_x ,pos_y)


# Buscamos en folletos, aquel que quepa dentro de las medidas dadas.
def buscaFolleto(folletos, ancho, alto):
    for index in range(len(folletos)):
        folleto = folletos[index]
        if folleto[1] <= ancho and folleto[2] <= alto:
            return folleto


# Buscamos el folleto que tenga más area
def buscaAreaMayor(folletos: List[Folleto]) -> Folleto:
    folletoAreaMayor = Folleto
    areaMayor = -1;
    for folleto in folletos:
        area = folleto[1] * folleto[2]
        if (area > areaMayor):
            areaMayor = area;
            folletoAreaMayor = folleto
    return folletoAreaMayor


# Rellenamos una hoja
def reparteEnHoja(n: int, folletos: List[Folleto], hojaNumero: int) -> List[PosicionFolleto]:

    copiaFolletos = deepcopy(folletos)
    mayor = buscaAreaMayor(copiaFolletos)
    folletos.remove(mayor)
    hojaADevolver = []
    relleno = [0] * n
                                        #Relleno es un vector con los espacios ocupados, en vertical, desde la parte superior del papel.
                                        # Por ejemplo el siguiente papel con X ocupado:

                                        #   X  X  O  O  O
                                        #   X  X  O  O  O
                                        #   X  X  O  O  O
                                        #   O  O  O  O  O
                                        #   O  O  O  O  O

                                        # Tendría de vector relleno = [3, 3, 0, 0, 0]


    # Miramos que el folleto más grande, quepa en la hoja
    if mayor[1] <= n and mayor[2] <= n:
        for i in range(mayor[1]):
            relleno[i] += mayor[2]
        hojaADevolver.append((mayor[0], hojaNumero, 0, 0))

    fila = 1
    while fila <= n:
        # Buscamos cuantos huecos consecutivos hay en esa fila
        numDeHuecos = 0
        huecoHayado = False
        puesto = False
        folleto = None
        posicionEnHoja = int
        for i in range(n + 1):
            if i > 0 and not puesto:
                if relleno[i - 1] < fila:
                    huecoHayado = True
                    numDeHuecos += 1
                if huecoHayado and relleno[i - 1] >= fila:
                    posicionEnHoja = (i - numDeHuecos, fila)
                    folleto = buscaFolleto(folletos, numDeHuecos, n - fila + 1)
                    if(folleto is None):
                        huecoHayado = False
                        numDeHuecos = 0
                    else:
                        puesto = True
                elif huecoHayado and i == n:
                    posicionEnHoja = (i - numDeHuecos + 1, fila)
                    folleto = buscaFolleto(folletos, numDeHuecos, n - fila + 1)
                    puesto = True

        # Si no hay folleto que quepa o no hay hueco en la fila, folleto == None
        if folleto is None:
            fila += 1
        else:
            folletos.remove(folleto)
            hojaADevolver.append((folleto[0], hojaNumero, posicionEnHoja[0] - 1, posicionEnHoja[1] - 1))
            for i in range(folleto[1]):
                relleno[posicionEnHoja[0] + i - 1] = fila - 1 + folleto[2]
    return hojaADevolver


# Ordenamos folletos, primero en anchura y, para una misma anchura, en altura
def ordenarFolletos(folletos: List[Folleto]) -> List[Folleto]:
    folletos.sort(key=operator.itemgetter(1, 2))
    folletos.reverse()
    return folletos


# m=tamaño del papel
# Función principal que crea la solución
def optimizaFolletos(m: int, folletos: List[Folleto]) -> List[PosicionFolleto]:
    folletosOrdenados = ordenarFolletos(folletos)
    conjuntoHojas = []
    hojaNumero = 1
    while len(folletosOrdenados) > 0:
        hoja = reparteEnHoja(m, folletosOrdenados, hojaNumero)
        conjuntoHojas += hoja
        hojaNumero += 1
    # sorted(conjuntoHojas, key=lambda i: i[0]) #Esto debería ordenar por el numero de folleto
    conjuntoHojas.sort(key=operator.itemgetter(0))
    # sorted(conjuntoHojas, key = lambda i: i[0]) #Esto debería ordenar por el numero de folleto
    return conjuntoHojas


# Lee el fichero .txt con los datos
def lee_fichero_imprenta(nombreFichero: str) -> Tuple[int, List[Folleto]]:
    with open(nombreFichero, mode='r') as file:
        tamanyo = int(file.readline())
        folletos = []
        for linea in file:
            folleto = extraeFolleto(linea)
            folletos.append(folleto)
    valores = (tamanyo, folletos)
    return valores


def extraeFolleto(linea):
    valores_folleto = linea.split(' ')
    num = int(valores_folleto[0])
    horizontal = int(valores_folleto[1])
    vertical = int(valores_folleto[2])
    tupla_folleto = (num, horizontal, vertical)
    return tupla_folleto


def muestra_solucion(solucion: "List[PosicionFolleto]"):
    for folleto in solucion:
        print(str(folleto[0]) + ' ' + str(folleto[1]) + ' ' + str(folleto[2]) + ' ' + str(folleto[3]))


def guarda_resultado(solucion: "List[PosicionFolleto]", ficheroF):
    for folleto in solucion:
        ficheroF.write(str(folleto[0]) + ' ' + str(folleto[1]) + ' ' + str(folleto[2]) + ' ' + str(folleto[3]) + "\n")


if __name__ == "__main__":
    if len(sys.argv) in [2, 3] :
        impresion = lee_fichero_imprenta(sys.argv[1])
        solucion = optimizaFolletos(impresion[0], impresion[1])
        muestra_solucion(solucion)

        if len(sys.argv) == 3 :
            nombreNuevoFichero = sys.argv[2]
            ficheroF = open(nombreNuevoFichero, "w")
            guarda_resultado(solucion, ficheroF)
            ficheroF.close()
    else:
        print( "Uso: imprenta.py <fichImprenta.txt> [<fichSolucion.txt>] (Opt: Genera un archivo con la solución)")
