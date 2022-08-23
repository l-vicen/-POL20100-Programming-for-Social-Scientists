from __future__ import annotations
import itertools
import copy

class Position:
    def __init__(self, row: int, col: int) -> Position:
        if row > 2 or row < 0:
            raise ValueError()

        if col > 2 or col < 0:
            raise ValueError()

        self.row = row
        self.col = col

    def __repr__(self) -> str:
        return f'Position(row={self.row}, col={self.col})'

    def __eq__(self, other):
        return True if self.row == other.row and self.col == other.col else False

    @property
    def get_row(self) -> int:
        return self.row

    @property
    def get_col(self) -> int:
        return self.col


class Board:
    state: list[list[int]]

    def __init__(self) -> Board:
        self.state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.encoders = {0: "-", 1: "X", 2: "O"}
        self.tmpPlayer = 0

    def __str__(self) -> str:
        return '''
                     {}  |  {}  |  {}  
                   _____|_____|_____
                        |     |     
                     {}  |  {}  |  {}  
                   _____|_____|_____
                        |     |     
                     {}  |  {}  |  {}  
                        |     |    '''.format(self.encoders.get(self.state[0][0]),
                                              self.encoders.get(self.state[0][1]),
                                              self.encoders.get(self.state[0][2]),
                                              self.encoders.get(self.state[1][0]),
                                              self.encoders.get(self.state[1][1]),
                                              self.encoders.get(self.state[1][2]),
                                              self.encoders.get(self.state[2][0]),
                                              self.encoders.get(self.state[2][1]),
                                              self.encoders.get(self.state[2][2]))

    def reset(self) -> None:
        self.state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    @property
    def __getPlayer__(self):
        return self.tmpPlayer

    @property
    def __getState__(self) -> list[list[int]]:
        return self.state

    def __setitem__(self, position: Position, value: int) -> None:

        if self[position] == 1:
            raise ValueError("X/O already exist at that position!")
        if self[position] == 2:
            raise ValueError("X/O already exist at that position!")
        if value > 2:
            raise ValueError("(0,1,2) are the only acceptable inputs.")
        if value < 0:
            raise ValueError("(0,1,2) are the only acceptable inputs.")

        if (self.tmpPlayer != value and value != 0):
            self.state[position.row][position.col] = value
            self.tmpPlayer = value

        else:
            raise ValueError("Can Not Played in a row!")


    def __getitem__(self, position: Position):
        row, col = position.row, position.col
        return self.state[row][col]

    @property
    def is_valid(self) -> bool:
        for i, l in enumerate(self.state):
            if len(l) != 3:
                return False
            if i > 2:
                return False
            if l[i] >= 3:
                return False

        single_list = list(itertools.chain(*self.state))
        xs = single_list.count(1)
        os = single_list.count(2)
        all_zeros = single_list.count(0)

        if xs % 2 == 0 and os % 2 == 0 and all_zeros != 9:
            return False
        return True

    @property
    def round(self) -> int:
        single_list = list(itertools.chain(*self.state))
        all_zeros = single_list.count(0)
        return 9 - all_zeros

    @property
    def winner(self) -> int:
        status = [self.encoders.get(self[Position(0, 0)]) + self.encoders.get(self[Position(1, 1)]) + self.encoders.get(
            self[Position(2, 2)]),
                self.encoders.get(self[Position(0, 2)]) + self.encoders.get(self[Position(1, 1)]) + self.encoders.get(
                    self[Position(2, 0)]),
                self.encoders.get(self[Position(0, 0)]) + self.encoders.get(self[Position(0, 1)]) + self.encoders.get(
                    self[Position(0, 2)]),
                self.encoders.get(self[Position(1, 0)]) + self.encoders.get(self[Position(1, 1)]) + self.encoders.get(
                    self[Position(1, 2)]),
                self.encoders.get(self[Position(2, 0)]) + self.encoders.get(self[Position(2, 1)]) + self.encoders.get(
                    self[Position(2, 2)]),
                self.encoders.get(self[Position(0, 0)]) + self.encoders.get(self[Position(1, 0)]) + self.encoders.get(
                    self[Position(2, 0)]),
                self.encoders.get(self[Position(0, 1)]) + self.encoders.get(self[Position(1, 1)]) + self.encoders.get(
                    self[Position(2, 1)]),
                self.encoders.get(self[Position(0, 2)]) + self.encoders.get(self[Position(1, 2)]) + self.encoders.get(
                    self[Position(2, 2)])]

        for s in status:
            if s == "XXX":
                return 1
            if s == "OOO":
                return 2
        return 0

    @property
    def is_finished(self) -> bool:
        if self.winner == 1 or self.winner == 2:
            return True
        if self.round == 9:
            return True
        return False

class Agent:

    def make_move(self, board: Board) -> Position:

        my_board = Board()
        my_board.state = board.state

        EDGES = [Position(0,0), Position(0,2), Position(2,0), Position(2,2)]
        SIDES = [Position(0,1), Position(1,0), Position(1,2), Position(2,1)]

        emptyPositions = []
        for i in range(len(my_board.state)):
            for j in range(len(board.state[i])):
                position = Position(i, j)
                if board[position] == 0:
                    emptyPositions.append(position)

        for simulatedPosition in emptyPositions:
            copyBoard = copy.deepcopy(my_board)
            copyBoard[simulatedPosition] = 1
            if copyBoard.winner == 1:
                return simulatedPosition

        for simulatedPosition in emptyPositions:
            copyBoard = copy.deepcopy(my_board)
            copyBoard[simulatedPosition] = 2
            if copyBoard.winner == 2:
                return simulatedPosition

        for position in emptyPositions:
            if position in EDGES:
                return position

        center = Position(1,1)
        if (my_board[center] == 0):
            return center

        for position in emptyPositions:
            if position in SIDES:
                return position

if __name__ == "__main__":
    board = Board()
    agent = Agent()


    while True:
        while not board.is_finished:
            try:
                row, col = (int(val) for val in input("Your input: ").split(","))
                move = Position(row, col)
                board[move] = 2

            except Exception as e:
                print("[ERROR] Wrong input or illegal move:", e)
                continue

            if not board.is_finished:
                move = agent.make_move(board)
                board[move] = 1
                print(board)

        if board.winner:
            print(board)
            print(f"Player {board.winner} wins!")
        else:
            print("Draw! No one wins!")
        board.reset()