"""
Connect Four Game Logic
"""

ROWS = 6
COLS = 7
EMPTY = 0
PLAYER = 1
AI = 2

def create_board():
    """ empty Connect Four board"""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def drop_piece(board, row, col, piece):
    """ piece on the board on the specified position"""
    board[row][col] = piece

def is_valid_location(board, col):
    """Checks if a column has space for a new piece"""
    return board[0][col] == EMPTY

def get_valid_locations(board):
    """Returns a list of columns where a piece can be placed"""
    return [col for col in range(COLS) if is_valid_location(board, col)]

def get_next_open_row(board, col):
    """Returns the lowest empty row in the specified column,
    In Connect Four, pieces fall to the bottom of the column.
    """
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return -1

def winning_move(board, piece):
    """Checks if the last move resulted in a win"""
    # Check horizontal locations
    for c in range(COLS-3):
        for r in range(ROWS):
            if (board[r][c] == piece and board[r][c+1] == piece and 
                board[r][c+2] == piece and board[r][c+3] == piece):
                return True

    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS-3):
            if (board[r][c] == piece and board[r+1][c] == piece and 
                board[r+2][c] == piece and board[r+3][c] == piece):
                return True

    # Check positively sloped diagonals
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if (board[r][c] == piece and board[r+1][c+1] == piece and 
                board[r+2][c+2] == piece and board[r+3][c+3] == piece):
                return True

    # Check negatively sloped diagonals
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if (board[r][c] == piece and board[r-1][c+1] == piece and 
                board[r-2][c+2] == piece and board[r-3][c+3] == piece):
                return True

    return False

def is_board_full(board):
    return all(board[0][col] != EMPTY for col in range(COLS))

def print_board(board):

    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            if board[row][col] == EMPTY:
                print("   |", end="")
            elif board[row][col] == PLAYER:
                print(" X |", end="")
            else:
                print(" O |", end="")
        print()
    print("|", end="")
    for col in range(COLS):
        print("===|", end="")
    print()
    print("|", end="")
    for col in range(COLS):
        print(f" {col} |", end="")
    print("\n")