import pygame
import random
import time
from tetris.constants import *
from tetris.universal_audio import UniversalAudio

class RetroTetris:
    """Classic retro Tetris game with authentic 1980s features only"""
    
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        
        # Classic Tetris board
        self.board = [[None for _ in range(10)] for _ in range(20)]
        
        # Simple piece shapes (classic 7 tetrominoes)
        self.pieces = {
            'I': [[(0, 1), (0, 0), (0, -1), (0, -2)],   # Vertical
                  [(-1, 0), (0, 0), (1, 0), (2, 0)]],   # Horizontal
            'O': [[(0, 0), (1, 0), (0, 1), (1, 1)]],    # Square - no rotation
            'T': [[(0, 0), (-1, 0), (1, 0), (0, -1)],   # T-piece - 4 rotations
                  [(0, 0), (0, -1), (0, 1), (1, 0)],
                  [(0, 0), (-1, 0), (1, 0), (0, 1)],
                  [(0, 0), (0, -1), (0, 1), (-1, 0)]],
            'S': [[(0, 0), (-1, 0), (0, -1), (1, -1)],   # S-piece - 2 rotations
                  [(0, 0), (0, -1), (1, 0), (1, 1)]],
            'Z': [[(0, 0), (1, 0), (0, -1), (-1, -1)],   # Z-piece - 2 rotations
                  [(0, 0), (0, 1), (1, 0), (1, -1)]],
            'J': [[(0, 0), (-1, 0), (1, 0), (-1, -1)],   # J-piece - 4 rotations
                  [(0, 0), (0, -1), (0, 1), (1, -1)],
                  [(0, 0), (-1, 0), (1, 0), (1, 1)],
                  [(0, 0), (0, -1), (0, 1), (-1, 1)]],
            'L': [[(0, 0), (-1, 0), (1, 0), (1, -1)],    # L-piece - 4 rotations
                  [(0, 0), (0, -1), (0, 1), (1, 1)],
                  [(0, 0), (-1, 0), (1, 0), (-1, 1)],
                  [(0, 0), (0, -1), (0, 1), (-1, -1)]]
        }
        
        # Classic colors (NES Tetris palette)
        self.colors = {
            'I': CYAN, 'O': YELLOW, 'T': PURPLE, 'S': GREEN,
            'Z': RED, 'J': BLUE, 'L': ORANGE
        }
        
        # Game state
        self.current_piece = None
        self.current_x = 5
        self.current_y = 0
        self.current_rotation = 0
        self.current_type = None
        
        # Classic scoring (original Nintendo scoring)
        self.score = 0
        self.lines = 0
        self.level = 0
        
        # Timing
        self.fall_time = 0
        self.fall_speed = 1.0  # 1 second initially
        
        # Game state
        self.game_over = False
        self.paused = False
        
        # Audio system (universal compatibility)
        self.audio = UniversalAudio()
        
        # Spawn first piece
        self.spawn_piece()
        
        # Start background music
        self.audio.start_music()
    
    def spawn_piece(self):
        """Spawn a new random piece"""
        self.current_type = random.choice(list(self.pieces.keys()))
        self.current_piece = self.current_type  # Fix: Set current_piece
        self.current_x = 4  # Center better (0-9 board, so 4 is more centered)
        self.current_y = 0
        self.current_rotation = 0
        
        # Check game over
        if not self.is_valid_position():
            self.game_over = True
            self.audio.stop_music()
            self.audio.play_sound('game_over')
    
    def is_valid_position(self, test_x=None, test_y=None, test_rotation=None):
        """Check if current piece position is valid"""
        x = test_x if test_x is not None else self.current_x
        y = test_y if test_y is not None else self.current_y
        rotation = test_rotation if test_rotation is not None else self.current_rotation
        
        piece_shape = self.pieces[self.current_type][rotation % len(self.pieces[self.current_type])]
        
        for dx, dy in piece_shape:
            new_x = x + dx
            new_y = y + dy
            
            # Check bounds
            if new_x < 0 or new_x >= 10 or new_y >= 20:
                return False
            
            # Check collision (allow pieces above board)
            if new_y >= 0 and self.board[new_y][new_x] is not None:
                return False
        
        return True
    
    def place_piece(self):
        """Place current piece on board"""
        piece_shape = self.pieces[self.current_type][self.current_rotation % len(self.pieces[self.current_type])]
        color = self.colors[self.current_type]
        
        for dx, dy in piece_shape:
            x = self.current_x + dx
            y = self.current_y + dy
            if 0 <= y < 20 and 0 <= x < 10:
                self.board[y][x] = color
        
        # Clear lines
        self.clear_lines()
        
        # Spawn next piece
        self.spawn_piece()
    
    def clear_lines(self):
        """Clear completed lines (classic Tetris line clearing)"""
        lines_cleared = 0
        y = 19
        
        while y >= 0:
            if all(self.board[y][x] is not None for x in range(10)):
                # Line is complete - remove it
                del self.board[y]
                self.board.insert(0, [None for _ in range(10)])
                lines_cleared += 1
            else:
                y -= 1
        
        # Play line clear sound
        if lines_cleared > 0:
            self.audio.play_sound('line_clear')
        
        # Classic scoring
        if lines_cleared > 0:
            line_scores = [0, 40, 100, 300, 1200]  # Original Nintendo scoring
            self.score += line_scores[lines_cleared] * (self.level + 1)
            self.lines += lines_cleared
            
            # Level up every 10 lines (classic)
            old_level = self.level
            new_level = self.lines // 10
            if new_level > self.level:
                self.level = new_level
                # Classic speed curve (gets very fast)
                self.fall_speed = max(0.1, 1.0 - (self.level * 0.1))
    
    def move_piece(self, dx, dy):
        """Try to move piece"""
        if self.is_valid_position(self.current_x + dx, self.current_y + dy):
            self.current_x += dx
            self.current_y += dy
            return True
        return False
    
    def rotate_piece(self):
        """Try to rotate piece"""
        new_rotation = (self.current_rotation + 1) % len(self.pieces[self.current_type])
        if self.is_valid_position(test_rotation=new_rotation):
            self.current_rotation = new_rotation
            return True
        return False
    
    def handle_input(self, event):
        """Handle classic Tetris input"""
        if event.type == pygame.KEYDOWN:
            if self.game_over:
                if event.key == pygame.K_r:
                    self.restart()
                return
            
            if event.key == pygame.K_p:
                self.paused = not self.paused
                if self.paused:
                    self.audio.pause_music()
                else:
                    self.audio.resume_music()
            elif not self.paused:
                if event.key == pygame.K_LEFT:
                    self.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    if self.move_piece(0, 1):
                        self.score += 1  # Soft drop bonus
                elif event.key == pygame.K_UP:
                    self.rotate_piece()
    
    def update(self, dt):
        """Update game logic"""
        if self.game_over or self.paused:
            return
        
        # Simple gravity
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            if not self.move_piece(0, 1):
                self.place_piece()
    
    def render(self):
        """Render classic Tetris"""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw board
        board_x = 300
        board_y = 50
        block_size = 25
        
        # Board background
        board_rect = pygame.Rect(board_x, board_y, 10 * block_size, 20 * block_size)
        pygame.draw.rect(self.screen, BLACK, board_rect)
        pygame.draw.rect(self.screen, WHITE, board_rect, 2)
        
        # Draw placed pieces (only within board bounds)
        for y in range(20):
            for x in range(10):
                if self.board[y][x] is not None:
                    block_rect = pygame.Rect(
                        board_x + x * block_size,
                        board_y + y * block_size,
                        block_size, block_size
                    )
                    pygame.draw.rect(self.screen, self.board[y][x], block_rect)
                    pygame.draw.rect(self.screen, WHITE, block_rect, 1)
        
        # Draw current piece (only within board bounds and below UI)
        if self.current_type is not None and not self.game_over:
            piece_shape = self.pieces[self.current_type][self.current_rotation % len(self.pieces[self.current_type])]
            color = self.colors[self.current_type]
            
            for dx, dy in piece_shape:
                x = self.current_x + dx
                y = self.current_y + dy
                # Only draw if within board bounds AND below the top UI area
                if 0 <= x < 10 and 0 <= y < 20 and y >= 0:
                    block_rect = pygame.Rect(
                        board_x + x * block_size,
                        board_y + y * block_size,
                        block_size, block_size
                    )
                    pygame.draw.rect(self.screen, color, block_rect)
                    pygame.draw.rect(self.screen, WHITE, block_rect, 1)
        
        # Classic UI (drawn AFTER pieces so it appears on top)
        font = pygame.font.Font(None, 36)
        
        # Score
        score_text = font.render(f"SCORE", True, WHITE)
        self.screen.blit(score_text, (50, 100))
        score_value = font.render(f"{self.score:06d}", True, WHITE)
        self.screen.blit(score_value, (50, 130))
        
        # Lines
        lines_text = font.render(f"LINES", True, WHITE)
        self.screen.blit(lines_text, (50, 180))
        lines_value = font.render(f"{self.lines:03d}", True, WHITE)
        self.screen.blit(lines_value, (50, 210))
        
        # Level
        level_text = font.render(f"LEVEL", True, WHITE)
        self.screen.blit(level_text, (50, 260))
        level_value = font.render(f"{self.level:02d}", True, WHITE)
        self.screen.blit(level_value, (50, 290))
        
        # Simple controls
        controls_font = pygame.font.Font(None, 20)
        controls = ["← → MOVE", "↓ DROP", "↑ ROTATE", "P PAUSE", "R RESTART"]
        for i, control in enumerate(controls):
            text = controls_font.render(control, True, LIGHT_GRAY)
            self.screen.blit(text, (600, 100 + i * 25))
        
        # Game over (drawn last so it's on top of everything)
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("GAME OVER", True, WHITE)
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(game_over_text, text_rect)
            
            restart_font = pygame.font.Font(None, 24)
            restart_text = restart_font.render("PRESS R TO RESTART", True, WHITE)
            restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
            self.screen.blit(restart_text, restart_rect)
        
        # Pause (drawn last so it's on top of everything)
        if self.paused and not self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)  # 50% transparency
            overlay.fill((0, 0, 0))  # Black overlay
            self.screen.blit(overlay, (0, 0))
            
            # Large centered PAUSED text
            pause_font = pygame.font.Font(None, 96)  # Larger font
            pause_text = pause_font.render("PAUSED", True, WHITE)
            text_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2))
            
            # Add a subtle shadow effect
            shadow_text = pause_font.render("PAUSED", True, (64, 64, 64))  # Dark gray shadow
            shadow_rect = shadow_text.get_rect(center=(self.width // 2 + 3, self.height // 2 + 3))
            self.screen.blit(shadow_text, shadow_rect)
            
            # Main text
            self.screen.blit(pause_text, text_rect)
            
            # Instructions below
            instruction_font = pygame.font.Font(None, 36)
            instruction_text = instruction_font.render("Press P to Resume", True, LIGHT_GRAY)
            instruction_rect = instruction_text.get_rect(center=(self.width // 2, self.height // 2 + 80))
            self.screen.blit(instruction_text, instruction_rect)
    
    def restart(self):
        """Restart the game"""
        self.board = [[None for _ in range(10)] for _ in range(20)]
        self.score = 0
        self.lines = 0
        self.level = 0
        self.fall_speed = 1.0
        self.fall_time = 0
        self.game_over = False
        self.paused = False
        self.spawn_piece()
        self.audio.start_music()
    
    def cleanup(self):
        """Clean up resources"""
        self.audio.cleanup()
