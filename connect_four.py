"""
Graphical User Interface

 GUI 
"""

import pygame
import sys    #control system like ElEnhaaa
import numpy as np
from game_logic import create_board, drop_piece, is_valid_location, get_next_open_row, winning_move, is_board_full
from ai_algorithms import get_ai_move
from logger import log_info
# sawabttt
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

ROWS = 6
COLS = 7
EMPTY = 0   #box empty
PLAYER = 1
AI = 2
'''
7agm E square and elyy gwah'''
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
#3ard we ertfa3
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE  
BUTTON_HEIGHT = 50
MENU_HEIGHT = 200  

# totalalla board
SIZE = (WIDTH, HEIGHT + BUTTON_HEIGHT + MENU_HEIGHT)

# Algorithm options
ALGORITHMS = {
    0: "Random",
    1: "Heuristic 1",
    2: "Heuristic 2",
    3: "MiniMax Basic",
    4: "MiniMax Alpha-Beta",
    5: "MiniMax + Heuristic 1",
    6: "MiniMax + Heuristic 2",
    7: "Minimax + Alpha-Beta + H1",
    8: "Minimax + Alpha-Beta + H2"
}

# Difficulty levels
DIFFICULTY_LEVELS = {
    1: "Easy",
    2: "Medium",
    3: "Hard"
}
#1
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
      #draw button  
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.current_color, (self.x, self.y, self.width, self.height))
        
        text_render = font.render(self.text, True, BLACK)
        text_rect = text_render.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        screen.blit(text_render, text_rect)
        #fi el2alb mosh sha5ala
    def is_hover(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            self.current_color = self.hover_color
            return True
        else:
            self.current_color = self.color
            return False
#2
class ConnectFour:
    def __init__(self):
        #initialize el pygame
        pygame.init()
        
        #  screeeeen of the game
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption('Connect Four AI')
        
        # 5otot
        self.font = pygame.font.SysFont('Arial', 25)
        self.small_font = pygame.font.SysFont('Arial', 18)
        self.large_font = pygame.font.SysFont('Arial', 40)
        
        # El7ala game over or not?
        self.game_over = False
        self.board = create_board()
        self.turn = 0  
        '''0: Player, 1: AI  turn like dorrrrrk'''
        
        
        self.algorithm = 5  # Default: MiniMax + Heuristic 1
        self.difficulty = 2  # Default: Medium
        
        #Restart button
        button_width = 150
        self.restart_button = Button(WIDTH//2 - button_width//2, HEIGHT + BUTTON_HEIGHT//2, 
                                     button_width, BUTTON_HEIGHT//2, "Restart Game", GRAY, WHITE)
        
        # algorithm buttons
        self.algo_buttons = []
        for i, algo_name in ALGORITHMS.items():
            btn_width = WIDTH // 3
            btn_height = MENU_HEIGHT // 4
            x = (i % 3) * btn_width
            y = HEIGHT + BUTTON_HEIGHT + (i // 3) * btn_height
            btn = Button(x, y, btn_width, btn_height, algo_name, GRAY, WHITE)
            self.algo_buttons.append((i, btn))
            
        #  difficulty 
        self.diff_buttons = []
        difficulty_area_start = HEIGHT + BUTTON_HEIGHT + (3 * MENU_HEIGHT // 4)
        for level, name in DIFFICULTY_LEVELS.items():
            btn_width = WIDTH // 3
            btn_height = MENU_HEIGHT // 4
            btn = Button((level-1) * btn_width, difficulty_area_start, 
                        btn_width, btn_height, name, GRAY, WHITE)
            self.diff_buttons.append((level, btn))
        #draw board and fill black on the board    
    def draw_board(self):
        
        self.screen.fill(BLACK)
        
        # draw rectangles and circles
        for c in range(COLS):
            for r in range(ROWS):
                pygame.draw.rect(self.screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
        
        #draw pieces red foe human and yellow for AI
        for c in range(COLS):
            for r in range(ROWS):
                if self.board[r][c] == PLAYER:
                    pygame.draw.circle(self.screen, RED, 
                                      (int(c*SQUARESIZE+SQUARESIZE/2), 
                                       HEIGHT - int((ROWS-r-1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                elif self.board[r][c] == AI:
                    pygame.draw.circle(self.screen, YELLOW, 
                                      (int(c*SQUARESIZE+SQUARESIZE/2), 
                                       HEIGHT - int((ROWS-r-1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
        
        #  drw the end side of the board
        pygame.draw.rect(self.screen, BLACK, (0, HEIGHT, WIDTH, BUTTON_HEIGHT + MENU_HEIGHT))
        
        #restart
        self.restart_button.draw(self.screen, self.font)
        
        # elketaba bta3 el algo ely e7tartooo
        algo_text = self.font.render("Algorithm Selection:", True, WHITE)
        self.screen.blit(algo_text, (10, HEIGHT + BUTTON_HEIGHT + 5))
        
       # ely e7tartooo lonoo green
        # 3shan el algo ely e7tartooo
        for algo_id, btn in self.algo_buttons:
            
            if algo_id == self.algorithm:
                btn.current_color = (100, 255, 100)  
            else:
                btn.current_color = GRAY
            btn.draw(self.screen, self.small_font)
            
        
        diff_text = self.font.render("Difficulty Level:", True, WHITE)
        self.screen.blit(diff_text, (10, HEIGHT + BUTTON_HEIGHT + (3 * MENU_HEIGHT // 4) - 25))
        
       # nafs el a5dar
        for level, btn in self.diff_buttons:
            
            if level == self.difficulty:
                btn.current_color = (100, 255, 100)  
            else:
                btn.current_color = GRAY
            btn.draw(self.screen, self.small_font)
            
        #state
        status_text = f"Current AI: {ALGORITHMS[self.algorithm]} - Difficulty: {DIFFICULTY_LEVELS[self.difficulty]}"
        status_surface = self.small_font.render(status_text, True, WHITE)
        self.screen.blit(status_surface, (10, HEIGHT + BUTTON_HEIGHT // 4))
        #update the display
        pygame.display.update()
        # animation m3fnnn
    def drop_animation(self, col, piece):
        #  dropping a piece
        row = get_next_open_row(self.board, col)
        final_y = HEIGHT - int((ROWS-row-1)*SQUARESIZE+SQUARESIZE/2)
        
        # (animation area) nemsa7
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        
        for y in range(SQUARESIZE//2, final_y + 1, 10):  
            
            self.draw_board()
            
            
            pos_x = col * SQUARESIZE + SQUARESIZE // 2
            color = RED if piece == PLAYER else YELLOW
            pygame.draw.circle(self.screen, color, (pos_x, y), RADIUS)
            
            pygame.display.update()
            pygame.time.wait(15)  
          #winner  
    def display_winner(self, winner):
        winner_text = "Player" if winner == PLAYER else "AI"
        log_info(f"{winner_text} won the game!") 
        text = "RED Wins!" if winner == PLAYER else "YELLOW Wins!"
        message = self.large_font.render(text, True, WHITE)
        rect = message.get_rect(center=(WIDTH // 2, SQUARESIZE // 2))
        
        #tabaaa soddda message win
        overlay = pygame.Surface((WIDTH, SQUARESIZE))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(message, rect)
        pygame.display.update()
        #draw
    def display_draw(self):
        log_info("Game ended in a draw")
        text = "Game Draw!"
        message = self.large_font.render(text, True, WHITE)
        rect = message.get_rect(center=(WIDTH // 2, SQUARESIZE // 2))
        
        #message
        overlay = pygame.Surface((WIDTH, SQUARESIZE))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(message, rect)
        pygame.display.update()
        
    def reset_game(self):
        log_info("Game restarted")
        self.board = create_board()
        self.game_over = False
        self.turn = 0  # Player start
        self.draw_board()
       # de mohhhhhemmmma awwwwway  
    def is_click_in_game_area(self, pos):
        
        return pos[1] < HEIGHT
        #main run
    def run(self):
        log_info("Game Started")
        self.draw_board()
        #infinity
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    # red piece on the top before playing
                if event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    
                    
                    if not self.game_over and self.turn == 0 and pos[1] < SQUARESIZE:
                        
                        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                        
                       
                        col = pos[0] // SQUARESIZE
                        if 0 <= col < COLS:  
                            pygame.draw.circle(self.screen, RED, (col * SQUARESIZE + SQUARESIZE // 2, SQUARESIZE // 2), RADIUS)
                            pygame.display.update()
                    
                    # Update button 
                    self.restart_button.is_hover(pos)
                    for _, btn in self.algo_buttons:
                        btn.is_hover(pos)
                    for _, btn in self.diff_buttons:
                        btn.is_hover(pos)
                    
                    #  UI elements
                    self.draw_board()
                    
              
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    
                    if self.restart_button.is_hover(pos):
                        self.reset_game()
                        continue
                        
                    #  algorithm buttons
                    algo_button_clicked = False
                    for algo_id, btn in self.algo_buttons:
                        if btn.is_hover(pos):
                            self.algorithm = algo_id
                            algo_button_clicked = True
                            self.draw_board()
                            break
                    
                    if algo_button_clicked:
                        continue
                            
                    #  difficulty buttons
                    diff_button_clicked = False
                    for level, btn in self.diff_buttons:
                        if btn.is_hover(pos):
                            self.difficulty = level
                            diff_button_clicked = True
                            self.draw_board()
                            break
                    
                    if diff_button_clicked:
                        continue
                    
                    # Players turn 
                    if not self.game_over and self.turn == 0 and self.is_click_in_game_area(pos):
                        col = pos[0] // SQUARESIZE
                        
                        if 0 <= col < COLS and is_valid_location(self.board, col):
                            log_info(f"Player moved to column {col}")
                            row = get_next_open_row(self.board, col)
                            self.drop_animation(col, PLAYER)
                            drop_piece(self.board, row, col, PLAYER)
                            
                            if winning_move(self.board, PLAYER):
                                self.draw_board()
                                self.display_winner(PLAYER)
                                self.game_over = True
                            elif is_board_full(self.board):
                                self.draw_board()
                                self.display_draw()
                                self.game_over = True
                            else:
                                self.turn = 1  # AI turn
                                self.draw_board()
            
            # AI turn
            if not self.game_over and self.turn == 1:
                #  delay 
                pygame.time.wait(500)
                
                #  AI move
                col = get_ai_move(self.board, self.algorithm, self.difficulty)
                log_info(f"AI (Algorithm: {ALGORITHMS[self.algorithm]}, Difficulty: {DIFFICULTY_LEVELS[self.difficulty]}) chose column {col}")  
               
                
                if is_valid_location(self.board, col):
                    row = get_next_open_row(self.board, col)
                    self.drop_animation(col, AI)
                    drop_piece(self.board, row, col, AI)
                    
                    if winning_move(self.board, AI):
                        self.draw_board()
                        self.display_winner(AI)
                        self.game_over = True
                    elif is_board_full(self.board):
                        self.draw_board()
                        self.display_draw()
                        self.game_over = True
                    else:
                        self.turn = 0  # Player turn
                        self.draw_board()

if __name__ == "__main__":
    game = ConnectFour()
    game.run()