#!/usr/bin/env python3
"""
Setup script for Retro Tetris Game
Checks system compatibility and provides setup instructions
"""

import sys
import pygame
import platform

def check_system():
    """Check system compatibility"""
    print("🎮 Retro Tetris - System Check")
    print("=" * 40)
    
    # Python version
    python_version = sys.version_info
    print(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 6):
        print("⚠️  Python 3.6+ recommended")
    else:
        print("✅ Python version OK")
    
    # Platform
    system = platform.system()
    print(f"Platform: {system}")
    
    # Pygame
    try:
        pygame_version = pygame.version.ver
        print(f"Pygame: {pygame_version}")
        print("✅ Pygame available")
    except:
        print("❌ Pygame not found")
        return False
    
    # Audio test
    print("\n🔊 Testing audio...")
    try:
        pygame.mixer.init()
        print("✅ Basic audio initialization OK")
        
        # Test sound creation
        try:
            test_sound = pygame.mixer.Sound(buffer=b'\x00\x00' * 1000)
            print("✅ Sound creation OK")
        except:
            print("⚠️  Sound creation limited")
        
        pygame.mixer.quit()
        
    except Exception as e:
        print(f"⚠️  Audio issues detected: {e}")
        print("   Game will use visual feedback mode")
    
    return True

def show_instructions():
    """Show game instructions"""
    print("\n🎮 How to Play")
    print("=" * 40)
    print("Controls:")
    print("  ← → Arrow Keys: Move pieces")
    print("  ↓ Arrow Key: Soft drop")
    print("  ↑ Arrow Key: Rotate piece")
    print("  P Key: Pause/Resume")
    print("  R Key: Restart (when game over)")
    print("  ESC: Quit")
    
    print("\nObjective:")
    print("  • Clear horizontal lines by filling them completely")
    print("  • Game speeds up as you progress")
    print("  • Don't let pieces reach the top!")
    
    print("\nAudio:")
    print("  • Game includes background music and sound effects")
    print("  • If audio doesn't work, visual feedback is provided")
    print("  • Compatible with most systems")

def main():
    """Main setup function"""
    if check_system():
        show_instructions()
        
        print("\n🚀 Ready to Play!")
        print("=" * 40)
        print("Run the game with:")
        print("  python3 retro_tetris_main.py")
        print("\nOr:")
        print("  python retro_tetris_main.py")
        
        print("\n🎵 Note: The game will automatically detect the best")
        print("audio method for your system and provide fallbacks")
        print("if needed. Enjoy!")
    else:
        print("\n❌ Setup incomplete. Please install pygame:")
        print("  pip install pygame")

if __name__ == "__main__":
    main()
