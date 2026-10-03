"""
Connect Four Test
"""

import pytest
from game_logic import create_board, drop_piece, is_valid_location, get_next_open_row, winning_move
from ai_algorithms import get_simple_move, get_heuristic1_move, get_heuristic2_move, minimax_basic

# Constants for testing
EMPTY = 0
PLAYER = 1
AI = 2
ROWS = 6
COLS = 7

def test_create_board():
    board = create_board()
    assert len(board) == ROWS
    assert len(board[0]) == COLS
    assert all(all(cell == EMPTY for cell in row) for row in board)

def test_drop_piece():
    board = create_board()
    drop_piece(board, 5, 3, PLAYER)  # Drop at row 5, col 3
    assert board[5][3] == PLAYER

def test_is_valid_location():
    board = create_board()
    
    # All locations should be valid in an empty board
    for col in range(COLS):
        assert is_valid_location(board, col)
    
    # Fill a column and test
    for row in range(ROWS):
        drop_piece(board, row, 0, PLAYER)
    
    assert not is_valid_location(board, 0)
    
def test_get_next_open_row():
    board = create_board()
    
    # In an empty board, the bottom row should be open
    for col in range(COLS):
        assert get_next_open_row(board, col) == ROWS - 1
    
    # Drop some pieces and test
    drop_piece(board, 5, 3, PLAYER)
    assert get_next_open_row(board, 3) == 4
    
    drop_piece(board, 4, 3, AI)
    assert get_next_open_row(board, 3) == 3

def test_horizontal_win():
    board = create_board()
    
    # Create a horizontal line of 4 for player
    for col in range(4):
        drop_piece(board, 5, col, PLAYER)
    
    assert winning_move(board, PLAYER)
    
    # Reset and test with no win
    board = create_board()
    for col in range(3):  # Only 3 in a row
        drop_piece(board, 5, col, PLAYER)
    
    assert not winning_move(board, PLAYER)

def test_vertical_win():
    board = create_board()
    
    # Create a vertical line of 4 for AI
    for row in range(5, 1, -1):
        drop_piece(board, row, 0, AI)
    
    assert winning_move(board, AI)
    
    # Reset and test with no win
    board = create_board()
    for row in range(5, 3, -1):  # Only 3 in a row
        drop_piece(board, row, 0, AI)
    
    assert not winning_move(board, AI)

def test_positive_diagonal_win():
    board = create_board()
    
    # Create a positive diagonal line for player
    drop_piece(board, 5, 0, PLAYER)
    drop_piece(board, 4, 1, PLAYER)
    drop_piece(board, 3, 2, PLAYER)
    drop_piece(board, 2, 3, PLAYER)
    
    assert winning_move(board, PLAYER)

def test_negative_diagonal_win():
    board = create_board()
    
    # Create a negative diagonal line for AI
    drop_piece(board, 2, 0, AI)
    drop_piece(board, 3, 1, AI)
    drop_piece(board, 4, 2, AI)
    drop_piece(board, 5, 3, AI)
    
    assert winning_move(board, AI)

def test_ai_simple_move():
    board = create_board()
    col = get_simple_move(board)
    assert 0 <= col < COLS
    
def test_ai_heuristic_moves():
    board = create_board()
    
    # Test heuristic 1
    col1 = get_heuristic1_move(board)
    assert 0 <= col1 < COLS
    
    # Test heuristic 2
    col2 = get_heuristic2_move(board)
    assert 0 <= col2 < COLS
    
    # Set up a winning move for AI and check if heuristic2 finds it
    board = create_board()
    for i in range(3):
        drop_piece(board, 5, i, AI)
    
    col = get_heuristic2_move(board)
    assert col == 3  # Should choose the winning move

def test_minimax_basic():
    board = create_board()
    
    # Empty board, should return a valid column
    col, _ = minimax_basic(board, 2, True)
    assert 0 <= col < COLS
    
    # Set up a winning move for AI and check if minimax finds it
    board = create_board()
    for i in range(3):
        drop_piece(board, 5, i, AI)
    
    col, score = minimax_basic(board, 2, True)
    assert col == 3  # Should choose the winning move
    
    # Set up a blocking move and check if minimax finds it
    board = create_board()
    for i in range(3):
        drop_piece(board, 5, i, PLAYER)
    
    col, _ = minimax_basic(board, 2, True)
    assert col == 3  # Should block player's potential win

if __name__ == "__main__":
    # Run the tests
    pytest.main(["-v"])