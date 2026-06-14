import pygame
import sys
import time

def test_sounds():
    pygame.init()
    pygame.mixer.init()

    sounds = [
        "sounds/slash.wav",
        "sounds/bomb.wav",
        "sounds/countdown.wav",
        "sounds/game_over.wav",
        "sounds/score.wav"
    ]
    
    print("Testing Sound Effects...")
    for s_path in sounds:
        try:
            sound = pygame.mixer.Sound(s_path)
            # Try to play it for a fraction of a second to test playability
            channel = sound.play()
            if channel:
                channel.stop()
            print(f"[OK] Successfully loaded and tested: {s_path}")
        except Exception as e:
            print(f"[FAILED] Could not load {s_path}: {e}")
            
    print("\nTesting Background Music...")
    try:
        pygame.mixer.music.load("sounds/background.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.stop()
        print("[OK] Successfully loaded background music.")
    except Exception as e:
        print(f"[FAILED] Could not load background.mp3: {e}")

    pygame.quit()
    print("\nAll tests completed.")

if __name__ == "__main__":
    test_sounds()
