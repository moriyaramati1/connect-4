import copy
import colorama
from colorama import Fore

colorama.init(autoreset=True)
BOLD = '\33[1m'
EMPTY = 0
SIZE = 4
BOARD_SIZE = 7
ZERO = 0.00001


class Player:
    Human = 1
    Computer = SIZE + 1
    NONE = 0


class Status:
    VICTORY = 10 ** 20
    LOSS = -VICTORY
    TIE = 0



class Game:
    def __init__(self):
        self.game_board = [BOARD_SIZE * [0] for i in range(BOARD_SIZE - 1)]
        self.board_value = ZERO
        self.player = Player.NONE
        self.empty_cells = BOARD_SIZE * (BOARD_SIZE - 1)
        self.columns = BOARD_SIZE
        self.rows = BOARD_SIZE - 1

    def marks_board(self, row, col):
        self.game_board[row][col] = Player.Human if self.player == Player.Human else Player.Computer

    def is_empty(self, row, col):
        return self.game_board[row][col] == EMPTY

    def filled_column(self, col):
        return self.game_board[0][col] != EMPTY

    def find_row(self, col):        
        for row in range(len(self.game_board) - 1, -1, -1):   # run on rows from bottom to top.
            if self.game_board[row][col] == EMPTY:  #we reached to an empty cell that is the row.
                return row


def value(game_state: Game):
    return game_state.board_value


def create():
    """
    Creates a new game state.
    :return: game state object
    """
    return Game()


def print_state(game_state: Game):
    for row in range(game_state.rows):  # run on the number of rows.
        print("\n --- --- --- --- --- --- ---\n|", end="")

        # the following code prints the values in different colors,
        # you need to download the package above for this.
        for col in range(game_state.columns):  # run on the number of columns.
            if game_state.game_board[row][col] == Player.Computer:  # if it is the computers turn.
                print(BOLD + Fore.RED + " X", end="")  # print a red X.
                print(" |", end="")
            elif game_state.game_board[row][col] == Player.Human:  # if it is the humans turn.
                print(BOLD + Fore.BLUE + " O", end="")  # print a blue O.
                print(" |", end="")
            else:
                print("", " ", "|", end="")

    print("\n --- --- --- --- --- --- --- ", end="")  # separate between the rows of the board.
    # print underneath the board the different columns of the board the player can choose for its move.
    print("\n  0   1   2   3   4   5   6  \n")

    val = value(game_state)
    if val == Status.VICTORY:  # if computer won.
        print("Ha ha ha I won!")
    elif val == Status.LOSS:  # if human won.
        print("You did it!")
    elif val == Status.TIE:  # if the game end with a tie.
        print("It's a TIE")


def is_finished(game_state: Game):
    
    return True if game_state.empty_cells == 0 else  game_state.board_value in [Status.TIE, Status.LOSS, Status.VICTORY]
    

def is_human_turn(game_state: Game):
    """
    :param game_state: The game object
    :return: this function returns true of its the humans turn to play.
    """
    return game_state.player == Player.Human


def who_is_first(game_state: Game):
    """
    :param game_state: The game object
    :return: this function allows the user to decide who plays first.
    """

    user_input = input("Who plays first? 1-me /anything else-you.: ")
    game_state.player = Player.Computer if user_input == "1" else Player.Human


def cell_not_exist(game_state: Game, row, col):
    """
    :param game_state: The game object
    :param row: A row number
    :param col: A column number
    :return: return true if the cell (r2,c2) doesnt exist on the board.
    """
    is_out_of_range = row < 0 or col < 0 or row >= len(game_state.game_board) or col >= game_state.columns
    return is_out_of_range



def get_steps(row1, col1, row2, col2):
    """
    This function return the horizontal step from cell to cell and the vertical step from cell to cell.
    :param row1: The current row
    :param col1: The current column
    :param row2: Another row
    :param col2: Another column
    :return: the steps
    """
    horizontal_step = (row2 - row1) // (SIZE - 1)
    vertical_step = (col2 - col1) // (SIZE - 1)
    return horizontal_step, vertical_step


def counts_seq(game_state: Game, r1, c1, dr, dc):
    """
    This function runs on the seq from (r1,c1) to the direction.
    and summing the different cell values, how many X and ho many O in this seq.
    :param game_state:
    :param r1: The current row
    :param c1: The current column
    :param dr: horizontal step
    :param dc: vertical step
    :return: How many X and O there are in this sequence.
    """
    ones = fourth = 0
    for i in range(SIZE):
        val = game_state.game_board[r1 + i * dr][c1 + i * dc]
        if val == Player.Human:
            ones += val
        else:
            fourth += val
    return fourth, ones


def check_seq(game_state: Game, r1, c1, r2, c2):
    """
     This function checks a seq of four cells on the board from (r1,c1) to (r2,c2)
     r1, c1 are on the board.
     if r2, c2 are not on the board the function returns 0
     if all cells are X returns VIC, if all O returns LOSS.
     if there are X and O returns 0.
     if only X returns 2**sum, if only O returns -2**(-sum).
     :param game_state: The game object
     :param r1: The current row
     :param c1: The current column
     :param r2: Another row
     :param c2: Another column
     :return: The heuristic value
    """
    if cell_not_exist(game_state, r2, c2):
        return EMPTY

    dr, dc = get_steps(r1, c1, r2, c2)

    fourth, ones = counts_seq(game_state, r1, c1, dr, dc)
    # if the seq contains X and O in it return 0 because as part of the heuristic we don't count this kind of seq.
    if ones != 0 and fourth != 0:
        return 0

    total = fourth - ones

    # if computer has 4 X, victory.
    if fourth == Player.Computer * SIZE:
        return Status.VICTORY

    # if human has 4 O, loss.
    if ones == Player.Human * SIZE:
        return Status.LOSS

    if total > 0:  # the seq has less then four x but no O so we return very big value.
        return 2 ** total
    if total < 0:  # the seq has less then four O but no x so we return very small value.
        return -(2 ** (-total))

    return 0


def make_move(game_state: Game, row, col):
    """
    This function puts a mark on the board in (r,c) for human or computer, assuming it is a legal move.
    then we switch turns, and re-evaluate the heuristic value.
    :param game_state: The game object
    :param row: A row
    :param col: A column
    """
    game_state.marks_board(row, col)
    game_state.empty_cells -= 1
    # Switch the player
    game_state.player = Player.Human if game_state.player == Player.Computer else Player.Computer

    dr = [-SIZE + 1, -SIZE + 1, 0, SIZE - 1]
    dc = [0, SIZE - 1, SIZE - 1, SIZE - 1]
    game_state.board_value = ZERO
    for Row in range(len(game_state.game_board)):
        for Col in range(len(game_state.game_board[0])):

            for i in range(len(dr)):

                # if the cell isn't empty send to check seq.
                if not game_state.is_empty(Row, Col):
                    t = check_seq(game_state, Row, Col, Row + dr[i], Col + dc[i])
                    if t in [Status.LOSS, Status.VICTORY]:
                        game_state.board_value = t
                        return
                    else:
                        game_state.board_value += t

    # if no more empty cells, tie.
    if game_state.empty_cells == EMPTY:
        game_state.board_value = Status.TIE


def input_move(game_state: Game):
    """
    This function reads, enforces legality and executes the user's move.
    :param game_state: The game object
    """
    print_state(game_state)
    flag = True  # helper
    while flag:
        try:
            move = int(input("Enter the column for your next move: "))
            col = move % 7  # column to fill a cell.

            if move < 0 or game_state.filled_column(col):
                print("Illegal move.")
            else:
                row = game_state.find_row(col)
                flag = False
                make_move(game_state, row, col)
        except ValueError:
            print("Illegal move.")


# this function returns a list of the next states of s.
def get_next(game_state: Game):
    """
    :param game_state:  The game object
    :return: A list of all next states of the board, and their heuristic value
    """
    next_states = []
    for c in range(game_state.columns):
        flag = True  # helper until we reach a empty row on column.

        for r in range(game_state.rows - 1, -1, -1):  # run on rows from bottom to top.
            if game_state.is_empty(r, c) and flag:  # if the cell is empty and flag.
                tmp = copy.deepcopy(game_state)
                make_move(tmp, r, c)
                next_states += [tmp]
                flag = False
    # for human the next states are sorted according to the heuristic value from small to big and for computer thr opisite.
    # if the player is computer then the resdiu is 0, and we need it to be reversed.
    player = game_state.player % Player.Computer
    next_states.sort(key=lambda element: value(element),reverse=not player)
    return next_states



