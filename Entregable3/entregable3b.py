import sys
from typing import *

from Entregable3.brikerdef import Move, Block, Level
from Entregable3.bt_scheme import PartialSolutionWithOptimization, BacktrackingOptSolver, Solution, State


def bricker_opt_solve(level):
    class BrikerOpt_PS(PartialSolutionWithOptimization):
        def __init__(self, block: Block, decisions: Tuple[Move, ...], pasos: int):
            self.block = block
            self.decisions = decisions
            self.meta = level.get_targetpos()
            self.pasos=pasos

        def is_solution(self)-> bool:
            return self.block.is_standing_at_pos(self.meta)

        def get_solution(self) -> Solution:
            if self.is_solution(): return self.decisions

        def successors(self) -> Iterable["BrikerOpt_PS"]:
            if self.is_solution(): return
            for mov in self.block.valid_moves(level.is_valid):

                yield BrikerOpt_PS(self.block.move(mov), self.decisions+(mov,), self.pasos+1)

        def state(self) -> State:
            return self.block

        def f(self) -> Union[int, float]:
            return self.pasos

    initial_ps = BrikerOpt_PS(Block(level.get_startpos(), level.get_startpos()), (), 0)
    return BacktrackingOptSolver.solve(initial_ps)

def imprime(num: int, sol):
    ficheroF = open("solution"+str(num)+".txt", "w")
    ficheroF.write(str(sol))

if __name__ == '__main__':
    #level_filename = "level1.txt"  # TODO: Cámbialo por sys.argv[1]

    if len(sys.argv) == 1:
        level_filename = sys.argv[1]
    else:
        print("Uso: entregable3a.py <level_filename.txt> ")

    print("<BEGIN BACKTRACKING>\n")

    # la última solución que devuelva será la más corta
    solutions = list(bricker_opt_solve(Level(level_filename)))

    if len(solutions)==0:
        print("El puzle no tiene solución.")
    else:
        best_solution = solutions[-1]
        string_solution = "".join(best_solution) #convierte la solución de lista  a  string
        #imprime(1,string_solution)
        print("La solución más corta es: {0} (longitud: {1})".format(string_solution, len(string_solution)))

    print("\n<END BACKTRACKING>")
