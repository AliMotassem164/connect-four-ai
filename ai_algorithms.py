
import random
from game_logic import get_valid_locations, drop_piece, get_next_open_row, winning_move

ROWS = 6
COLS = 7
EMPTY = 0
PLAYER = 1
AI = 2

#####################
# Heuristic Functions #
#####################

def evaluate_window_h1(line, player):
    """Heuristic 1: """
    opponent = PLAYER if player == AI else AI
    player_count = line.count(player)
    opponent_count = line.count(opponent)
    
    if opponent_count == 0:
        if player_count == 2:
            return 10
        elif player_count == 3:
            return 100
        elif player_count == 4:
            return 1000
    return 0

def evaluate_board_h1(board, player):
    """Heuristic 1: """
    score = 0
    opponent = PLAYER if player == AI else AI

    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            line = [board[row][col + i] for i in range(4)]
            score += evaluate_window_h1(line, player)

    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            line = [board[row + i][col] for i in range(4)]
            score += evaluate_window_h1(line, player)

    # Positive Diagonal *Sahm Nazel yemen*
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            line = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window_h1(line, player)

    # Negative Diagonal *Sahm Nazel shemal*
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            line = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window_h1(line, player)

    return score

def evaluate_window_h2(line, player):
    """Heuristic 2: Evaluates a window of 4 cells"""
    opponent = PLAYER if player == AI else AI
    player_count = line.count(player)
    opponent_count = line.count(opponent)
    empty_count = line.count(EMPTY)

    if player_count == 4:
        return 1000
    elif player_count == 3 and empty_count == 1:
        return 50
    elif player_count == 2 and empty_count == 2:
        return 10
    elif opponent_count == 3 and empty_count == 1:
        return -80  # Blocking opponents potential win
    return 0

def evaluate_board_h2(board, player):
    """Heuristic 2: """
    score = 0
    opponent = PLAYER if player == AI else AI

    # center column
    center_col = [board[r][COLS // 2] for r in range(ROWS)]
    center_count = center_col.count(player)
    score += center_count * 6

    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            line = [board[row][col + i] for i in range(4)]
            score += evaluate_window_h2(line, player)

    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            line = [board[row + i][col] for i in range(4)]
            score += evaluate_window_h2(line, player)

    # Positive Diagonal
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            line = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window_h2(line, player)

    # Negative Diagonal
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            line = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window_h2(line, player)

    return score

###################
# Algorithm Functions #
###################

def get_simple_move(board):
    """ a random move"""
    valid = get_valid_locations(board)
    if valid:
        return random.choice(valid)
    return 0

def get_heuristic1_move(board):
    """Heuristic 1 """
    best_score = float('-inf')
    valid = get_valid_locations(board)
    best_col = random.choice(valid) if valid else 0
    
    for col in valid:
        # Create a  board
        temp = [row[:] for row in board]
        row = get_next_open_row(temp, col)
        drop_piece(temp, row, col, AI)
        score = evaluate_board_h1(temp, AI)
        
        if score > best_score:
            best_score = score
            best_col = col
            
    return best_col

def get_heuristic2_move(board):
    """ Heuristic 2    :"""
    best_score = float('-inf')
    valid = get_valid_locations(board)
    best_col = random.choice(valid) if valid else 0
    
    for col in valid:
        #  board
        temp = [row[:] for row in board]
        row = get_next_open_row(temp, col)
        drop_piece(temp, row, col, AI)
        score = evaluate_board_h2(temp, AI)
        
        if score > best_score:
            best_score = score
            best_col = col
            
    return best_col

def minimax_basic(board, depth, maximizing_player):
    """Basic MiniMax algorithm """
    valid = get_valid_locations(board)
    is_terminal = depth == 0 or winning_move(board, PLAYER) or winning_move(board, AI) or not valid
    
    if is_terminal:
        if winning_move(board, AI):
            return (None, 1000000)
        elif winning_move(board, PLAYER):
            return (None, -1000000)
        elif not valid:  # Game is a draw
            return (None, 0)
        else:  # depth is zero
            return (None, 0)
    
    if maximizing_player:
        value = float('-inf')
        column = random.choice(valid)
        
        for col in valid:
            temp = [row[:] for row in board]
            row = get_next_open_row(temp, col)
            drop_piece(temp, row, col, AI)
            new_score = minimax_basic(temp, depth-1, False)[1]
            
            if new_score > value:
                value = new_score
                column = col
                
        return column, value
    
    else:  # Minimiz player
        value = float('inf')
        column = random.choice(valid)
        
        for col in valid:
            temp = [row[:] for row in board]
            row = get_next_open_row(temp, col)
            drop_piece(temp, row, col, PLAYER)
            new_score = minimax_basic(temp, depth-1, True)[1]
            
            if new_score < value:
                value = new_score
                column = col
                
        return column, value

def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    """MiniMax algorithm with Alpha-Beta pruning"""
    valid = get_valid_locations(board)
    is_terminal = depth == 0 or winning_move(board, PLAYER) or winning_move(board, AI) or not valid
    
    if is_terminal:
        if winning_move(board, AI):
            return (None, 1000000)
        elif winning_move(board, PLAYER):
            return (None, -1000000)
        elif not valid:  # Game is a draw
            return (None, 0)
        else:  # depth is zero
            return (None, 0)
    
    if maximizing_player:
        value = float('-inf')
        column = random.choice(valid)
        
        for col in valid:
            temp = [row[:] for row in board]
            row = get_next_open_row(temp, col)
            drop_piece(temp, row, col, AI)
            new_score = minimax_alpha_beta(temp, depth-1, alpha, beta, False)[1]
            
            if new_score > value:
                value = new_score
                column = col
                
            alpha = max(alpha, value)
            if alpha >= beta:
                break
                
        return column, value
    
    else:  # Minimiz player
        value = float('inf')
        column = random.choice(valid)
        
        for col in valid:
            temp = [row[:] for row in board]
            row = get_next_open_row(temp, col)
            drop_piece(temp, row, col, PLAYER)
            new_score = minimax_alpha_beta(temp, depth-1, alpha, beta, True)[1]
            
            if new_score < value:
                value = new_score
                column = col
                
            beta = min(beta, value)
            if alpha >= beta:
                break
                
        return column, value

def minimax_h1(board, depth, maximizing_player):
    """MiniMax algorithm with Heuristic 1"""
    valid = get_valid_locations(board)
    is_terminal = depth == 0 or winning_move(board, PLAYER) or winning_move(board, AI) or not valid
    
    if is_terminal:
        if winning_move(board, AI):
            return (None, 1000000)
        elif winning_move(board, PLAYER):
            return (None, -1000000)
        elif not valid:  # Game is a draw
            return (None, 0)
        else:  # depth is zero
            return (None, evaluate_board_h1(board, AI))
    
    if maximizing_player:
        value = float('-inf')
        column = random.choice(valid)
        
        for col in valid:
            temp = [row[:] for row in board]
            row = get_next_open_row(temp, col)
            drop_piece(temp, row, col, AI)
            new_score = minimax_h1(temp, depth-1, False)[1]
            
            if new_score > value:
                value = new_score
                column = col
                
        return column, value
    
    else:  # Minimiz player
        value = float('inf')
        column = random.choice(valid)
        
        for col in valid:
            temp = [row[:] for row in board]
            row = get_next_open_row(temp, col) 
            drop_piece(temp, row, col, PLAYER)
            new_score = minimax_h1(temp, depth-1, True)[1]
            
            if new_score < value:
                value = new_score
                column = col
                
        return column, value

def minimax_h2(board, depth, maximizing_player):
    """MiniMax algorithm with Heuristic 2"""
    valid = get_valid_locations(board)
    is_terminal = depth == 0 or winning_move(board, PLAYER) or winning_move(board, AI) or not valid
    
    if is_terminal:
        if winning_move(board, AI):
            return (None, 1000000)
        elif winning_move(board, PLAYER):
            return (None, -1000000)
        elif not valid:  # Game is a draw
            return (None, 0)
        else:  # depth is zero
            return (None, evaluate_board_h2(board, AI))
    
    if maximizing_player:
        value = float('-inf')
        column = random.choice(valid)
        
        for col in valid:
            temp = [row[:] for row in board]
            row = get_next_open_row(temp, col)
            drop_piece(temp, row, col, AI)
            new_score = minimax_h2(temp, depth-1, False)[1]
            
            if new_score > value:
                value = new_score
                column = col
                
        return column, value
    
    else:  # Minimiz player
        value = float('inf')
        column = random.choice(valid)
        
        for col in valid:
            temp = [row[:] for row in board]
            row = get_next_open_row(temp, col)
            drop_piece(temp, row, col, PLAYER)
            new_score = minimax_h2(temp, depth-1, True)[1]
            
            if new_score < value:
                value = new_score
                column = col
                
        return column, value
                                                    #True/False
def minimax_alpha_beta_h1(board, depth, alpha, beta, maximizing_player):
    """MiniMax algorithm with Alpha-Beta pruning and Heuristic 1"""

    # tagme3 elmota7 tel3b feiiih
    valid = get_valid_locations(board)
    '''3omk mo3in ybka heuristic,player==min, Ai=max                                                                 '''
    is_terminal = depth == 0 or winning_move(board, PLAYER) or winning_move(board, AI) or not valid #no move 
    
    if is_terminal:
        if winning_move(board, AI):
            return (None, 1000000) #terminal scores
        elif winning_move(board, PLAYER):
            return (None, -1000000)
        elif not valid:  # Game is a draw
            return (None, 0)
        else:  # depth is zero
            return (None, evaluate_board_h1(board, AI)) #no every thing ybka h1
    
    if maximizing_player: #role =Ai
        value = float('-inf') # 3shan tkon ay natigaaa akbar menhhha wee te7adeshha
        column = random.choice(valid)
        
        for col in valid:
            temp = [row[:] for row in board]
            row = get_next_open_row(temp, col)
            drop_piece(temp, row, col, AI)
            new_score = minimax_alpha_beta_h1(temp, depth-1, alpha, beta, False)[1] #recursion algorithm
            #law eldragga elgededa ahsan men el7alya
            if new_score > value:
                value = new_score
                column = col
                
            alpha = max(alpha, value)
            if alpha >= beta:
                break
         #perfect col and value       
        return column, value
    
    else:  # Minimiz player role= human
        value = float('inf')
        column = random.choice(valid)
        
        for col in valid:
            temp = [row[:] for row in board]
            row = get_next_open_row(temp, col)
            drop_piece(temp, row, col, PLAYER)
            new_score = minimax_alpha_beta_h1(temp, depth-1, alpha, beta, True)[1]
            
            if new_score < value:
                value = new_score
                column = col
                
            beta = min(beta, value) #as5ar kemma wgdaha min
            if alpha >= beta:
                break
                
        return column, value

def minimax_alpha_beta_h2(board, depth, alpha, beta, maximizing_player):
    """MiniMax algorithm with Alpha-Beta pruning and Heuristic 2"""
    valid = get_valid_locations(board)
    is_terminal = depth == 0 or winning_move(board, PLAYER) or winning_move(board, AI) or not valid
    
    if is_terminal:
        if winning_move(board, AI):
            return (None, 1000000)
        elif winning_move(board, PLAYER):
            return (None, -1000000)
        elif not valid:  # Game is a draw
            return (None, 0)
        else:  # depth is zero
            return (None, evaluate_board_h2(board, AI))
    
    if maximizing_player:
        value = float('-inf')
        column = random.choice(valid)
        
        for col in valid:
            temp = [row[:] for row in board]
            row = get_next_open_row(temp, col)
            drop_piece(temp, row, col, AI)
            new_score = minimax_alpha_beta_h2(temp, depth-1, alpha, beta, False)[1]
            
            if new_score > value:
                value = new_score
                column = col
                
            alpha = max(alpha, value)
            if alpha >= beta:
                break
                
        return column, value
    
    else:  # Minimiz player
        value = float('inf')
        column = random.choice(valid)
        
        for col in valid:
            temp = [row[:] for row in board]
            row = get_next_open_row(temp, col)
            drop_piece(temp, row, col, PLAYER)
            new_score = minimax_alpha_beta_h2(temp, depth-1, alpha, beta, True)[1]
            
            if new_score < value:
                value = new_score
                column = col
                
            beta = min(beta, value)
            if alpha >= beta:
                break
                
        return column, value

######################
# Interface Function #
######################

def get_ai_move(board, algorithm, level=2):
    """difficulty level"""
    depths = {1: 2,  # Easy
              2: 4,  # Medium
              3: 6}  # Hard
    
    depth = depths.get(level, 4)
    
    if algorithm == 0:  # Random
        return get_simple_move(board)
    
    elif algorithm == 1:  # Heuristic 1
        return get_heuristic1_move(board)
    
    elif algorithm == 2:  # Heuristic 2
        return get_heuristic2_move(board)
    
    elif algorithm == 3:  # MiniMax Basic
        return minimax_basic(board, depth, True)[0]
    
    elif algorithm == 4:  # MiniMax with Alpha-Beta pruning
        return minimax_alpha_beta(board, depth, float('-inf'), float('inf'), True)[0]
    
    elif algorithm == 5:  # MiniMax with Heuristic 1
        return minimax_h1(board, depth, True)[0]
    
    elif algorithm == 6:  # MiniMax with Heuristic 2
        return minimax_h2(board, depth, True)[0]
        
    elif algorithm == 7:  # MiniMax with Alpha-Beta pruning and Heuristic 1
        return minimax_alpha_beta_h1(board, depth, float('-inf'), float('inf'), True)[0]
    
    elif algorithm == 8:  # MiniMax with Alpha-Beta pruning and Heuristic 2
        return minimax_alpha_beta_h2(board, depth, float('-inf'), float('inf'), True)[0]
        
    else:  # Default: random choice
        return get_simple_move(board)