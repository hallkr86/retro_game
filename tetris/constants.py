# Tetris game constants

# Colors (retro Tetris palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Tetris piece colors (classic NES colors)
CYAN = (0, 255, 255)      # I-piece
BLUE = (0, 0, 255)        # J-piece  
ORANGE = (255, 165, 0)    # L-piece
YELLOW = (255, 255, 0)    # O-piece
GREEN = (0, 255, 0)       # S-piece
PURPLE = (128, 0, 128)    # T-piece
RED = (255, 0, 0)         # Z-piece

# Game board dimensions
BOARD_WIDTH = 10          # Standard Tetris width
BOARD_HEIGHT = 20         # Standard Tetris height
BLOCK_SIZE = 25           # Size of each block in pixels

# Game board position on screen
BOARD_X = 250
BOARD_Y = 50

# Game timing
INITIAL_FALL_SPEED = 1.0  # Seconds between automatic drops
FAST_DROP_SPEED = 0.05    # Speed when soft dropping
LOCK_DELAY = 0.5          # Time before piece locks in place

# Scoring
SCORE_SINGLE = 100        # 1 line
SCORE_DOUBLE = 300        # 2 lines  
SCORE_TRIPLE = 500        # 3 lines
SCORE_TETRIS = 800        # 4 lines (Tetris!)

# Level progression
LINES_PER_LEVEL = 10      # Lines needed to advance level
SPEED_INCREASE = 0.1      # How much faster each level gets
