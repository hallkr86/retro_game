import pygame
import sys
import time
from tetris.retro_tetris import RetroTetris

def main():
    # Initialize Pygame
    pygame.init()
    
    # Classic arcade resolution
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    FPS = 60
    
    # Create display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Retro Tetris - Classic 1980s Style with Audio")
    clock = pygame.time.Clock()
    
    # Create classic Tetris game
    game = RetroTetris(screen, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    try:
        # Game loop with audio-friendly timing
        running = True
        while running:
            dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            # Small pause to give audio processing time
            if dt < 0.016:  # If running faster than 60 FPS
                time.sleep(0.002)  # 2ms pause for audio breathing room
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    game.handle_input(event)
            
            # Update game
            game.update(dt)
            
            # Render game
            game.render()
            
            # Update display
            pygame.display.flip()
    
    finally:
        # Clean up audio resources
        game.cleanup()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
