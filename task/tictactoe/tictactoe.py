# write your code here
from random import choice


class TicTacToe:
    def __init__(self):
        self.field = [["" for _ in range(3)] for _ in range(3)]
        self.empty = [(x, y) for x in range(3) for y in range(3)]
        self.winner = None

    @staticmethod
    def is_winner(v):
        if v == ["X", "X", "X"]:
            return "X"
        elif v == ["O", "O", "O"]:
            return "O"
        else:
            return None

    def column(self, j):
        return [self.field[i][j] for i in range(3)]

    def diagonal(self):
        return [self.field[i][i] for i in range(3)]

    def antidiagonal(self):
        return [self.field[i][2 - i] for i in range(3)]

    def set_winner(self, x, y):
        self.winner = self.is_winner(self.field[x])
        if not self.winner:
            self.winner = self.is_winner(self.column(y))
            if not self.winner:
                if x == y:
                    self.winner = self.is_winner(self.diagonal())
                elif x + y == 2:
                    self.winner = self.is_winner(self.antidiagonal())

    @staticmethod
    def threeable(v, mark):
        if v.count("") == 1:
            if mark in v:
                if v.count(mark) == 2:
                    return True, v.index("")
            else:
                return False, v.index("")
        return None

    def sensible_ai(self, mark):
        coordinates = choice(self.empty)
        for i in range(3):
            able = self.threeable(self.field[i], mark)
            if able:
                coordinates = i, able[1]
                if able[0]:
                    return coordinates
        for j in range(3):
            able = self.threeable(self.column(j), mark)
            if able:
                coordinates = able[1], j
                if able[0]:
                    return coordinates
        able = self.threeable(self.diagonal(), mark)
        if able:
            coordinates = able[1], able[1]
            if able[0]:
                return coordinates
        able = self.threeable(self.antidiagonal(), mark)
        if able:
            return able[1], 2 - able[1]
        return coordinates

    def silent_move(self, x, y):
        self.field[x][y] = "X" if len(self.empty) % 2 else "O"
        self.empty.remove((x, y))
        self.set_winner(x, y)

    def reset_move(self, x, y):
        self.field[x][y] = ""
        self.empty.append((x, y))

    def minimax(self, ai_mark):
        moves = []
        turn = "X" if len(self.empty) % 2 else "O"
        empty_cells = self.empty.copy()
        for cell in empty_cells:
            self.silent_move(*cell)
            if self.winner == ai_mark:
                moves.append((10, cell))
            elif self.winner:
                moves.append((-10, cell))
            elif not self.empty:
                moves.append((0, cell))
            else:
                moves.append((self.minimax(ai_mark)[0], cell))
            self.reset_move(*cell)
        if turn == ai_mark:
            return max(moves, key=lambda m: m[0])
        else:
            return min(moves, key=lambda m: m[0])

    def ai_choice(self, level):
        ai_mark = "X" if len(self.empty) % 2 else "O"
        if level == "easy":
            print('Making move level "easy"')
            return choice(self.empty)
        if level == "medium":
            print('Making move level "medium"')
            return self.sensible_ai(ai_mark)
        if level == "hard":
            print('Making move level "hard"')
            return self.minimax(ai_mark)[1]

    def print_field(self):
        print("-" * 9)
        for row in self.field:
            print("| {:1} {:1} {:1} |".format(*row))
        print("-" * 9)

    def next_move(self, x, y=None):
        if y is None:
            x, y = self.ai_choice(x)
        self.silent_move(x, y)
        self.print_field()

    def continues(self):
        return not self.winner and self.empty

    def print_state(self):
        if self.winner:
            print(f"{self.winner} wins")
        elif self.empty:
            print("Game not finished")
        else:
            print("Draw")


class OutOfRangeError(ValueError):
    pass


class CellOccupiedError(ValueError):
    pass


class BadParametersError(ValueError):
    pass


def get_coordinates():
    while True:
        try:
            coordinates = [int(number) - 1 for number in input("Enter the coordinates: ").split()]
            if not (0 <= coordinates[0] <= 2 and 0 <= coordinates[1] <= 2):
                raise OutOfRangeError
            if tic_tac_toe.field[coordinates[0]][coordinates[1]]:
                raise CellOccupiedError
        except IndexError:
            print("You should provide at least two coordinates!")
        except OutOfRangeError:
            print("Coordinates should be from 1 to 3!")
        except CellOccupiedError:
            print("This cell is occupied! Choose another one!")
        except ValueError:
            print("You should enter numbers!")
        else:
            return coordinates[0], coordinates[1]


def user_vs_ai(ai):
    while tic_tac_toe.continues():
        x, y = get_coordinates()
        tic_tac_toe.next_move(x, y)
        if tic_tac_toe.continues():
            tic_tac_toe.next_move(ai)
        else:
            break
    tic_tac_toe.print_state()


def user_vs_user():
    while tic_tac_toe.continues():
        x, y = get_coordinates()
        tic_tac_toe.next_move(x, y)
    tic_tac_toe.print_state()


def ai_vs_ai(ai1, ai2):
    while tic_tac_toe.continues():
        tic_tac_toe.next_move(ai1)
        if tic_tac_toe.continues():
            tic_tac_toe.next_move(ai2)
        else:
            break
    tic_tac_toe.print_state()


def play(player1, player2):
    if player1 == "user":
        if player2 == "user":
            user_vs_user()
        else:
            user_vs_ai(player2)
    else:
        if player2 == "user":
            tic_tac_toe.next_move(player1)
            user_vs_ai(player1)
        else:
            ai_vs_ai(player1, player2)


modes = ["user", "easy", "medium", "hard"]
while True:
    try:
        command = input("Input command: ").split()
        if command[0] == "exit":
            break
        if command[1] not in modes or command[2] not in modes:
            raise BadParametersError
    except (IndexError, BadParametersError):
        print("Bad parameters!")
    else:
        tic_tac_toe = TicTacToe()
        tic_tac_toe.print_field()
        play(command[1], command[2])
