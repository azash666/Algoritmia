import sys
from typing import *

from Entregable3.brikerdef import Move, Block, Level
from Entregable3.bt_scheme import PartialSolutionWithVisitedControl, Solution, State, BacktrackingVCSolver


def bricker_vc_solve(level: Level):
    class BrikerVC_PS(PartialSolutionWithVisitedControl):
        def __init__(self, block: Block, decisions: Tuple[Move, ...]):
            self.block = block
            self.decisions = decisions
            self.meta = level.get_targetpos()
            print(self.decisions)

        def is_solution(self) -> bool:
            return self.block.is_standing_at_pos(self.meta)

        def get_solution(self) -> Solution:
             if self.is_solution(): return self.decisions


        def successors(self) -> Iterable["BrikerVC_PS"]:
            if self.is_solution(): return
            for mov in self.block.valid_moves(level.is_valid):
                print(mov)
                yield BrikerVC_PS(self.block.move(mov), self.decisions+(mov,))


        def state(self) -> State:
            return self.block
            # TODO: Implementar


    # TODO: crea initial_ps y llama a BacktrackingVCSolver.solve
    initial_PS = BrikerVC_PS(Block(level.get_startpos(), level.get_startpos()),())
    return BacktrackingVCSolver.solve(initial_PS)



if __name__ == '__main__':
    #level_filename = "level2.txt"  # TODO: Cámbialo por sys.argv[1]

    if len(sys.argv) == 1 : level_filename = sys.argv[1]
    else: print( "Uso: entregable3a.py <level_filename.txt> ")

    print("<BEGIN BACKTRACKING>\n")

    for solution in bricker_vc_solve(Level(level_filename)):
        string_solution = "".join(solution)  # convierte la solución de lista a string
        print("La primera solución encontrada es: {0} (longitud: {1})".format(string_solution, len(string_solution)))
        break

    print("\n<END BACKTRACKING>")
