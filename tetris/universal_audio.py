import pygame
import threading
import time
import os
import sys

class UniversalAudio:
    """Universal audio system that works across different environments"""
    
    def __init__(self):
        self.enabled = False
        self.music_playing = False
        self.music_thread = None
        self.stop_flag = False
        self.audio_method = None
        
        # Try different audio initialization methods
        self._initialize_audio()
        
        print(f"Universal audio system ready! Method: {self.audio_method}")
    
    def _initialize_audio(self):
        """Try different audio initialization approaches"""
        
        # Method 1: Conservative pygame mixer
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=4096)
            pygame.mixer.init()
            pygame.mixer.set_num_channels(8)
            self.audio_method = "pygame_conservative"
            self.enabled = True
            print("✅ Using conservative pygame audio")
            return
        except Exception as e:
            print(f"Conservative pygame failed: {e}")
        
        # Method 2: Basic pygame mixer
        try:
            pygame.mixer.init()
            self.audio_method = "pygame_basic"
            self.enabled = True
            print("✅ Using basic pygame audio")
            return
        except Exception as e:
            print(f"Basic pygame failed: {e}")
        
        # Method 3: Alternative audio (if available)
        try:
            import winsound
            self.audio_method = "winsound"
            self.enabled = True
            print("✅ Using Windows winsound")
            return
        except ImportError:
            pass
        
        # Method 4: Visual-only mode
        self.audio_method = "visual_only"
        self.enabled = True
        print("✅ Using visual-only mode (no audio conflicts)")
    
    def create_simple_music_data(self):
        """Create simple music data that should work universally"""
        if not self.enabled or self.audio_method == "visual_only":
            return None
        
        try:
            # Create a very simple, short music loop
            import math
            import struct
            
            sample_rate = 22050
            duration = 8.0  # 8 second loop
            frames = int(duration * sample_rate)
            
            # Simple Tetris melody - lowered by an octave for better sound
            notes = [
                (330, 1.0),  # E4 (was 659 E5)
                (247, 0.5),  # B3 (was 494 B4)
                (262, 0.5),  # C4 (was 523 C5)
                (294, 1.0),  # D4 (was 587 D5)
                (262, 0.5),  # C4 (was 523 C5)
                (247, 0.5),  # B3 (was 494 B4)
                (220, 2.0),  # A3 (was 440 A4) - long note
            ]
            
            wave_data = []
            current_time = 0
            
            for frequency, note_duration in notes:
                note_frames = int(note_duration * sample_rate)
                
                for i in range(note_frames):
                    t = current_time + (i / sample_rate)
                    
                    # Simple square wave
                    square_wave = 1 if (t * frequency) % 1 < 0.5 else -1
                    
                    # Very quiet and smooth
                    volume = 0.05
                    envelope = volume * min(1.0, i / (sample_rate * 0.1)) * min(1.0, (note_frames - i) / (sample_rate * 0.1))
                    
                    sample = int(square_wave * envelope * 32767)
                    wave_data.extend([sample, sample])  # Stereo
                
                current_time += note_duration
            
            # Convert to bytes
            packed_data = struct.pack('<' + 'h' * len(wave_data), *wave_data)
            
            # Create pygame sound
            if self.audio_method.startswith("pygame"):
                return pygame.mixer.Sound(buffer=packed_data)
            
        except Exception as e:
            print(f"Music creation failed: {e}")
            return None
    
    def start_music(self):
        """Start background music with fallback methods"""
        if not self.enabled or self.music_playing:
            return
        
        if self.audio_method == "visual_only":
            self._start_visual_music()
            return
        
        if self.audio_method.startswith("pygame"):
            self._start_pygame_music()
        elif self.audio_method == "winsound":
            self._start_winsound_music()
    
    def _start_pygame_music(self):
        """Start pygame-based music"""
        try:
            music_sound = self.create_simple_music_data()
            if music_sound:
                # Play on a dedicated channel with loop
                channel = pygame.mixer.Channel(7)
                channel.play(music_sound, loops=-1)
                self.music_playing = True
                print("🎵 Pygame music started")
            else:
                self._start_visual_music()
        except Exception as e:
            print(f"Pygame music failed: {e}")
            self._start_visual_music()
    
    def _start_winsound_music(self):
        """Start Windows beep-based music"""
        try:
            self.stop_flag = False
            self.music_thread = threading.Thread(target=self._winsound_music_loop, daemon=True)
            self.music_thread.start()
            self.music_playing = True
            print("🎵 Windows beep music started")
        except Exception as e:
            print(f"Winsound music failed: {e}")
            self._start_visual_music()
    
    def _winsound_music_loop(self):
        """Simple beep melody loop"""
        import winsound
        
        melody = [
            (330, 400), (247, 200), (262, 200), (294, 400),  # E4, B3, C4, D4
            (262, 200), (247, 200), (220, 800)               # C4, B3, A3
        ]
        
        while not self.stop_flag:
            for freq, duration in melody:
                if self.stop_flag:
                    break
                try:
                    winsound.Beep(int(freq), duration)
                except:
                    time.sleep(duration / 1000.0)
            time.sleep(1.0)
    
    def _start_visual_music(self):
        """Start visual music display"""
        try:
            self.stop_flag = False
            self.music_thread = threading.Thread(target=self._visual_music_loop, daemon=True)
            self.music_thread.start()
            self.music_playing = True
            print("🎵 Visual music started")
        except Exception as e:
            print(f"Visual music failed: {e}")
    
    def _visual_music_loop(self):
        """Visual music representation"""
        melody_symbols = ["♪", "♫", "♪♪", "♫♫", "♪♫", "♫♪", "♪♪♪"]
        index = 0
        
        while not self.stop_flag:
            if index % 4 == 0:  # Every 4th beat
                print(f"🎵 {melody_symbols[index % len(melody_symbols)]}", end=" ", flush=True)
            index += 1
            time.sleep(0.8)
    
    def stop_music(self):
        """Stop music regardless of method"""
        if not self.music_playing:
            return
        
        self.stop_flag = True
        self.music_playing = False
        
        if self.audio_method.startswith("pygame"):
            try:
                pygame.mixer.Channel(7).stop()
            except:
                pass
        
        print("\n🎵 Music stopped")
    
    def play_sound(self, sound_name):
        """Play notification sounds with fallbacks"""
        # Visual feedback always works
        feedback = {
            'line_clear': "✨ LINE CLEARED! ✨",
            'pause': "⏸️ GAME PAUSED ⏸️",
            'game_over': "💀 GAME OVER 💀"
        }
        
        if sound_name in feedback:
            print(f"\n{feedback[sound_name]}\n")
        
        # Try audio feedback
        if self.audio_method == "winsound":
            try:
                import winsound
                frequencies = {'line_clear': 262, 'pause': 220, 'game_over': 165}  # C4, A3, E3
                if sound_name in frequencies:
                    winsound.Beep(frequencies[sound_name], 300)
            except:
                pass
        elif self.audio_method.startswith("pygame"):
            try:
                # Simple beep using pygame
                pass  # Could implement pygame beeps here
            except:
                pass
    
    def pause_music(self):
        """Pause music"""
        self.stop_music()
        self.play_sound('pause')
    
    def resume_music(self):
        """Resume music"""
        self.start_music()
    
    def cleanup(self):
        """Clean shutdown"""
        self.stop_music()
        if self.music_thread:
            self.music_thread.join(timeout=1.0)
