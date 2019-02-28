from typing import *


# ---------------------------------------------------------------------------------------------------------

class Move:
    Left = "L"
    Right = "R"
    Up = "U"
    Down = "D"


# ---------------------------------------------------------------------------------------------------------

class Pos2D:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def add_row(self, d) -> "Pos2D":
        return Pos2D(self.row + d, self.col)

    def add_col(self, d) -> "Pos2D":
        return Pos2D(self.row, self.col + d)

    def __eq__(self, other):
        if not isinstance(other, Pos2D): return False
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

    def __repr__(self):
        return "Pos2D({}, {})".format(self.row, self.col)


# ---------------------------------------------------------------------------------------------------------

class Level:
    def __init__(self, filename: str):
        self._mat = [line.strip() for line in open(filename).readlines()]
        self.rows = len(self._mat)
        self.cols = len(self._mat[0])
        self._sPos = self.find_character('S')
        self._tPos = self.find_character('T')
        #raise NotImplementedError

    def is_valid(self, pos: Pos2D) -> bool:

        if((pos.col not in range (0,self.cols)) or (pos.row not in range (0,self.rows))):
            return False
        if(self._mat[pos.row][pos.col]=='-'):
            return False
        return True

        # TODO: IMPLEMENTAR - Debe devolver False para cualquier posición fuera del tablero o para
        # posiciones marcadas con '-'. Para todos los demás casos debe devolver True.
        #raise NotImplementedError

    def get_startpos(self) -> Pos2D:
        return self._sPos

    def get_targetpos(self) -> Pos2D:
        return self._tPos

    def find_character(self, character:str) -> Pos2D:
        row = 0
        for line in self._mat:
            if character in line:
                return Pos2D(row,line.index(character))
            row+=1
        return None
# ---------------------------------------------------------------------------------------------------------

class Block:
    def __init__(self, b1: Pos2D, b2: Pos2D):
        assert isinstance(b1, Pos2D) and isinstance(b2, Pos2D)
        if b2.row < b1.row or (b2.row == b1.row and b2.col < b1.col):
            self._b1, self._b2 = b2, b1
        else:
            self._b1, self._b2 = b1, b2

    # -----------------------------------------------------------------------------
    # <BEGIN> Funciones para comparar correctamente objetos de tipo Block

    def __eq__(self, other):
        if not isinstance(other, Block): return False
        return self._b1 == other._b1 and self._b2 == other._b2

    # Necesario para poder meter objetos de tipo Block en colecciones
    def __hash__(self):
        return hash((self._b1, self._b2))

    # <END> Funciones para comparar correctamente objetos de tipo Block
    # -----------------------------------------------------------------------------

    def __repr__(self):
        return "Block({}, {})".format(self._b1, self._b2)

    def is_standing(self) -> bool:  # true si el bloque está de pie
        return self._b1.row == self._b2.row and self._b1.col == self._b2.col

    def is_standing_at_pos(self, pos: Pos2D) -> bool:
        # Devuelve true si el bloque está de pie en la posición indicada en el parámetro
        return self.is_standing() and self._b1.row == pos.row and self._b1.col == pos.col

    def is_lying_on_a_row(self) -> bool:  # true si el bloque está tumbado en una fila
        return self._b1.row == self._b2.row and self._b1.col != self._b2.col

    def is_lying_on_a_col(self) -> bool:  # true si el bloque está tumbado en una columna
        return self._b1.row != self._b2.row and self._b1.col == self._b2.col

    def valid_moves(self, is_valid_pos: Callable[[Pos2D], bool]) -> Iterable[Move]:

        if(self.is_standing()):
            if(is_valid_pos(Pos2D(self._b2.row + 2, self._b2.col)) and is_valid_pos(Pos2D(self._b1.row + 1, self._b1.col))): yield Move.Down
            if(is_valid_pos(Pos2D(self._b2.row - 1, self._b2.col)) and is_valid_pos(Pos2D(self._b1.row - 2, self._b1.col))): yield Move.Up
            if(is_valid_pos(Pos2D(self._b2.row, self._b2.col + 2)) and is_valid_pos(Pos2D(self._b1.row, self._b1.col + 1))): yield Move.Right
            if(is_valid_pos(Pos2D(self._b2.row, self._b2.col - 1)) and is_valid_pos(Pos2D(self._b1.row, self._b1.col - 2))): yield Move.Left

        if(self.is_lying_on_a_row()):
            if(is_valid_pos(Pos2D(self._b2.row + 1, self._b2.col)) and is_valid_pos(Pos2D(self._b1.row + 1, self._b1.col))): yield Move.Down
            if(is_valid_pos(Pos2D(self._b2.row - 1, self._b2.col)) and is_valid_pos(Pos2D(self._b1.row - 1, self._b1.col))): yield Move.Up
            if(is_valid_pos(Pos2D(self._b2.row, self._b2.col + 1)) and is_valid_pos(Pos2D(self._b1.row, self._b1.col + 2))): yield Move.Right
            if(is_valid_pos(Pos2D(self._b2.row, self._b2.col - 2)) and is_valid_pos(Pos2D(self._b1.row, self._b1.col - 1))): yield Move.Left

        if(self.is_lying_on_a_col()):
            if(is_valid_pos(Pos2D(self._b2.row + 1, self._b2.col)) and is_valid_pos(Pos2D(self._b1.row + 2, self._b1.col))): yield Move.Down
            if(is_valid_pos(Pos2D(self._b2.row - 2, self._b2.col)) and is_valid_pos(Pos2D(self._b1.row - 1, self._b1.col))): yield Move.Up
            if(is_valid_pos(Pos2D(self._b2.row, self._b2.col + 1)) and is_valid_pos(Pos2D(self._b1.row, self._b1.col + 1))): yield Move.Right
            if(is_valid_pos(Pos2D(self._b2.row, self._b2.col - 1)) and is_valid_pos(Pos2D(self._b1.row, self._b1.col - 1))): yield Move.Left

        # TODO: IMPLEMENTAR - Debe devolver los movimientos válidos dada la posición actual
        # Debe utilizar la funcion is_valid_pos para comprobar cada casilla
    
        # TODO: IMPLEMENTAR - Debe devolver los movimientos válidos dada la posición actual
        # Debe utilizar la funcion is_valid_pos para comprobar cada casilla

    def move(self, m: Move) -> "Block":

        b2 = Pos2D(self._b2.row, self._b2.col)
        b1 = Pos2D(self._b1.row, self._b1.col)

        if(self.is_standing()):
            if m == Move.Up:
                b=b2.add_row(-1)
                j =b1.add_row(-2)
            if m == Move.Down:
                b =b2.add_row(2)
                j =b1.add_row(1)
            if m == Move.Right:
                b =b2.add_col(2)
                j =b1.add_col(1)
            if m == Move.Left:
                b =b2.add_col(-1)
                j =b1.add_col(-2)

        if(self.is_lying_on_a_row()):
            if m == Move.Up:
                b =b2.add_row(-1)
                j =b1.add_row(-1)
            if m == Move.Down:
                b =b2.add_row(1)
                j =b1.add_row(1)
            if m == Move.Right:
                b =b2.add_col(1)
                j =b1.add_col(2)
            if m == Move.Left:
                b =b2.add_col(-2)
                j =b1.add_col(-1)

        if(self.is_lying_on_a_col()):
            if m == Move.Up:
                b =b2.add_row(-2)
                j =b1.add_row(-1)
            if m == Move.Down:
                b =b2.add_row(1)
                j =b1.add_row(2)
            if m == Move.Right:
                b =b2.add_col(1)
                j =b1.add_col(1)
            if m == Move.Left:
                b =b2.add_col(-1)
                j=b1.add_col(-1)


        bloque = Block(j,b)
        return bloque

        # TODO: IMPLEMENTAR - Debe devolver un nuevo objeto 'Block', sin modificar el original
        #raise NotImplementedError

# ---------------------------------------------------------------------------------------------------------
