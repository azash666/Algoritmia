import sys
from typing import List, Tuple

import kdtree as KDTree

HORIZONTAL = KDTree.Axis.X
VERTICAL = KDTree.Axis.Y
Orientacion = bool

def read_points(filename:str)-> List[Tuple[float, float]]:
    with open(filename, mode='r') as file:
        puntos_2D = []
        for linea in file:
            valores_punto = extract_Point(linea)
            puntos_2D.append(valores_punto)
    return puntos_2D


def extract_Point(linea):
    valores_linea = linea.split(' ')
    coordenada_x = float(valores_linea[0])
    coordenada_y = float(valores_linea[1])
    valores_punto = (coordenada_x, coordenada_y)
    return valores_punto

def build_kd_tree(points: List[Tuple[float, float]]) -> KDTree:


    #Casos base

    if(len(points)==0):
        return None
    elif (len(points) ==1):
        return KDTree.KDLeaf(points[0])

    #Recursividad

    else:
        cantidadDePuntos = len(points)
        medio = cantidadDePuntos // 2
        ordenacionHorizontal = sorted(points, key=lambda i: i[0])
        ordenacionVertical = sorted(points, key=lambda i: i[1])

        if(ordenacionHorizontal[-1][0]-ordenacionHorizontal[0][0] >= ordenacionVertical[-1][1]-ordenacionVertical[0][1]):
            eje = HORIZONTAL
        else:
            eje = VERTICAL

        if(eje==HORIZONTAL):
            arbol1 = build_kd_tree(ordenacionHorizontal[0:medio])
            arbol2= build_kd_tree(ordenacionHorizontal[medio:])
            mediana = hallaMediana(medio, ordenacionHorizontal, eje)
        else:
            arbol1 = build_kd_tree(ordenacionVertical[0:medio])
            arbol2= build_kd_tree(ordenacionVertical[medio:])
            mediana = hallaMediana(medio, ordenacionVertical, eje)


        nodo = KDTree.KDNode(eje, mediana, arbol1 ,arbol2 )
        return nodo

def hallaMediana(medio: int, points: List[Tuple[float, float]], eje: Orientacion) -> float:
    cantidadDePuntos = len(points)
    if (cantidadDePuntos % 2 == 0):
        return (points[medio-1][eje] + points[medio][eje]) / 2
    return points[medio][eje]


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        list_points = read_points(sys.argv[1])
        kd_tree_solution = build_kd_tree(list_points)
        print(kd_tree_solution.pretty())
    else:
        print('Argumentos introducidos incorrectos.')






