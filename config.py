"""
Connect Four Game Configuration
"""

# Game constants
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER = 1
AI = 2

# Color settings
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Display settings
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
BUTTON_HEIGHT = 50
MENU_HEIGHT = 100
SIZE = (WIDTH, HEIGHT + BUTTON_HEIGHT + MENU_HEIGHT)

# AI settings
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

DIFFICULTY_LEVELS = {
    1: "Easy",
    2: "Medium",
    3: "Hard"
}

SEARCH_DEPTHS = {
    1: 2,  # Easy: 2 levels deep
    2: 4,  # Medium: 4 levels deep
    3: 6   # Hard: 6 levels deep
}

# Animation settings
DROP_SPEED = 50  # milliseconds between animation frames