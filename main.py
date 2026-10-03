"""
Connect Four 
"""

import argparse
from game_logic import create_board, drop_piece, is_valid_location, get_next_open_row, winning_move, print_board
from ai_algorithms import get_ai_move
from logger import log_info, log_error

class ConnectFour:
    def __init__(self):
        pass
    
    def run(self):
        print("GUI mode is under development. Please use text mode with '-t' flag.")

def run_text_mode(algorithm=1, difficulty=2):

    board = create_board()
    game_over = False
    turn = 0
    
    log_info("Game started")
    print("\nWelcome to Connect Four!")
    print("========================")
    print("You are RED (X), AI is YELLOW (O)")
    print(f"AI Algorithm: {algorithm}, Difficulty: {difficulty}")
    print("Enter column number (0-6) to drop a piece")
    print("Enter 'q' to quit\n")
    
    print_board(board)
    
    while not game_over:
        if turn == 0:
            col = input("Player's turn (0-6): ")
            
            if col.lower() == 'q':
                log_info("Player quit the game")
                print("Quitting game. Thanks for playing!")
                break
                
            try:
                col = int(col)
                if col < 0 or col >= 7:
                    log_error(f"Invalid column input: {col}")
                    print("Invalid column. Please enter a number between 0 and 6.")
                    continue
            except ValueError:
                log_error("Non-numeric input")
                print("Invalid input. Please enter a number between 0 and 6.")
                continue
                
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)
                log_info(f"Player moved to column {col}")
                
                print_board(board)
                
                if winning_move(board, 1):
                    log_info("Player won the game")
                    print("🎉 Player wins! 🎉")
                    game_over = True
                    break
                turn = 1
            else:
                log_error(f"Attempted move to full column: {col}")
                print("Column is full. Choose another one.")
                
        else:
            print("AI is thinking...")
            col = get_ai_move(board, algorithm, difficulty)
            log_info(f"AI chose column {col}")
            
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                
                print(f"AI drops piece in column {col}")
                print_board(board)
                
                if winning_move(board, 2):
                    log_info("AI won the game")
                    print("AI wins!")
                    game_over = True
                    break
                turn = 0
                
    log_info("Game session ended\n")

def main():

    try:
        parser = argparse.ArgumentParser(description='Connect Four with AI')
        parser.add_argument('-t', '--text', action='store_true', help='Run in text mode (no GUI)')
        parser.add_argument('-a', '--algorithm', type=int, default=1, choices=range(0, 9), help='AI algorithm (0-8)')
        parser.add_argument('-d', '--difficulty', type=int, default=2, choices=[1, 2, 3], help='Difficulty level (1=Easy, 2=Medium, 3=Hard)')
        
        args = parser.parse_args()
        
        if args.text:
            run_text_mode(args.algorithm, args.difficulty)
        else:
            game = ConnectFour()
            game.algorithm = args.algorithm
            game.difficulty = args.difficulty
            game.run()
    except Exception as e:
        log_error(f"Critical error: {str(e)}")

if __name__ == "__main__":
    main()