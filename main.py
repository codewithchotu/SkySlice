import cv2
import pygame
from bomb import Bomb
from settings import *
from hand_tracker import HandTracker
from fruit import Fruit
from score import Score
from effect import Effect, FloatingText, Particle
import random
from collections import deque




pygame.init()

pygame.mixer.init()

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        return pygame.mixer.Sound(buffer=bytearray(2)) # silent fallback

slash_sound = load_sound("sounds/slash.wav")
bomb_sound = load_sound("sounds/bomb.wav")
countdown_sound = load_sound("sounds/countdown.wav")
game_over_sound = load_sound("sounds/game_over.wav")
score_sound = load_sound("sounds/score.wav")

try:
    pygame.mixer.music.load("sounds/background.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    pass



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SkySlice")

sword_img = pygame.image.load(
    "assets/effects/sword.png"
).convert_alpha()

sword_img = pygame.transform.scale(
    sword_img,
    (100, 100)
)

red_splash = pygame.image.load(
    "assets/effects/splash_red.png"
).convert_alpha()
red_splash = pygame.transform.scale(red_splash, (150, 150))

yellow_splash = pygame.image.load(
    "assets/effects/splash_yellow.png"
).convert_alpha()
yellow_splash = pygame.transform.scale(yellow_splash, (150, 150))

explosion_img = pygame.image.load(
    "assets/effects/explosion.png"
).convert_alpha()
explosion_img = pygame.transform.scale(explosion_img, (150, 150))

clock = pygame.time.Clock()

try:
    sky_bg = pygame.image.load("assets/backgrounds/sky_bg.png").convert()
    sky_bg = pygame.transform.scale(sky_bg, (WIDTH, HEIGHT))
except pygame.error:
    sky_bg = pygame.Surface((WIDTH, HEIGHT))
    sky_bg.fill((30, 30, 40))

import os

try:
    if os.path.getsize("assets/fonts/game_font.ttf") > 0:
        game_font_large = pygame.font.Font("assets/fonts/game_font.ttf", 150)
        game_font_medium = pygame.font.Font("assets/fonts/game_font.ttf", 100)
        game_font_small = pygame.font.Font("assets/fonts/game_font.ttf", 50)
    else:
        raise ValueError("Empty font file")
except:
    game_font_large = pygame.font.SysFont(None, 150)
    game_font_medium = pygame.font.SysFont(None, 100)
    game_font_small = pygame.font.SysFont(None, 50)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera not found!")
    exit()

tracker = HandTracker()
score = Score()

fruits = []
bombs = []
effects = []

SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN, FRUIT_SPAWN_TIME)

state = "START_COUNTDOWN"
start_time = pygame.time.get_ticks()

last_slice_time = 0
combo_count = 0
sword_trail = deque(maxlen=15)
shake_time = 0
last_spawn_time = 0
freeze_timer = 0
lives = 3

countdown_sound.play()
running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        if state == "GAME_OVER":
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                state = "START_COUNTDOWN"
                start_time = pygame.time.get_ticks()
                score.value = 0
                fruits.clear()
                bombs.clear()
                effects.clear()
                sword_trail.clear()
                combo_count = 0
                freeze_timer = 0
                lives = 3
                countdown_sound.play()

        if state == "PLAYING":
            current_spawn_time = max(300, 1000 - (score.value * 20))
            if pygame.time.get_ticks() - last_spawn_time > current_spawn_time:
                last_spawn_time = pygame.time.get_ticks()
                if random.randint(1, 5) == 1:
                    bombs.append(Bomb())
                else:
                    fruits.append(Fruit())

    ret, frame = cap.read()

    finger = None
    fx, fy = 0, 0

    shake_offset = (0, 0)
    current_time = pygame.time.get_ticks()
    if state == "GAME_OVER" and current_time - shake_time < 500:
        shake_offset = (random.randint(-20, 20), random.randint(-20, 20))

    if ret:
        frame = cv2.flip(frame, 1)
        finger = tracker.get_index_finger(frame)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (WIDTH, HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
        screen.blit(frame_surface, shake_offset)
        
        if finger:
            fx = int(finger[0] * WIDTH / frame.shape[1])
            fy = int(finger[1] * HEIGHT / frame.shape[0])
            sword_trail.append((fx, fy))
        else:
            if len(sword_trail) > 0:
                sword_trail.popleft()

    else:
        screen.blit(sky_bg, shake_offset)
        if len(sword_trail) > 0:
            sword_trail.popleft()

    if state == "START_COUNTDOWN":
        elapsed = pygame.time.get_ticks() - start_time
        seconds_left = 3 - (elapsed // 1000)
        
        if seconds_left <= 0:
            state = "PLAYING"
        else:
            text = game_font_large.render(str(seconds_left), True, WHITE)
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text, text_rect)
            
    elif state == "PLAYING":
        gravity_mult = 0.3 if pygame.time.get_ticks() < freeze_timer else 1.0
        for fruit in fruits[:]:
            out_of_bounds = fruit.update(gravity_mult)
            if out_of_bounds:
                fruits.remove(fruit)
                lives -= 1
                if lives <= 0:
                    state = "GAME_OVER"
                    game_over_sound.play()
                continue
                
            fruit.draw(screen)
            
            if finger:
                hit = fruit.rect.collidepoint(fx, fy)
                if not hit and len(sword_trail) >= 2:
                    hit = fruit.rect.clipline(sword_trail[-2], sword_trail[-1])
                
                if hit:
                    slash_sound.play()
                    score_sound.play()
                    
                    p_color = (255, 0, 0)
                    if any(color in fruit.filename for color in ["apple", "strawberry", "watermelon"]):
                        splash_img = red_splash
                        p_color = (255, 50, 50)
                    else:
                        splash_img = yellow_splash
                        p_color = (255, 255, 50)
                    
                    effects.append(Effect(splash_img, fruit.x, fruit.y))
                    for _ in range(15):
                        effects.append(Particle(fruit.x, fruit.y, p_color))
                        
                    if fruit.special_type == 'FREEZE':
                        freeze_timer = pygame.time.get_ticks() + 5000
                    elif fruit.special_type == 'FRENZY':
                        for _ in range(15):
                            fruits.append(Fruit())
                            
                    fruits.remove(fruit)
                    
                    if current_time - last_slice_time < 500:
                        combo_count += 1
                    else:
                        combo_count = 1
                    last_slice_time = current_time
                    
                    if combo_count > 1:
                        score.add(combo_count)
                        effects.append(FloatingText(f"{combo_count}x COMBO!", fruit.x, fruit.y - 40, game_font_small, (255, 255, 0)))
                    else:
                        score.add(1)
                        effects.append(FloatingText("+1", fruit.x, fruit.y - 40, game_font_small, (255, 255, 255)))

        for bomb in bombs[:]:
            out_of_bounds = bomb.update(gravity_mult)
            if out_of_bounds:
                bombs.remove(bomb)
                continue
                
            bomb.draw(screen)
            
            if finger:
                hit = bomb.rect.collidepoint(fx, fy)
                if not hit and len(sword_trail) >= 2:
                    hit = bomb.rect.clipline(sword_trail[-2], sword_trail[-1])
                    
                if hit:
                    bomb_sound.play()
                    game_over_sound.play()
                    effects.append(Effect(explosion_img, bomb.x, bomb.y))
                    state = "GAME_OVER"
                    shake_time = pygame.time.get_ticks()

        if len(sword_trail) > 1:
            pygame.draw.lines(screen, (200, 200, 255), False, list(sword_trail), 8)
        if finger:
            screen.blit(sword_img, (fx - 50, fy - 50))

        text = game_font_small.render(f"Score: {score.value}  Best: {score.high_score}", True, WHITE)
        screen.blit(text, (20, 20))
        lives_text = game_font_small.render(f"Lives: {lives}", True, RED)
        screen.blit(lives_text, (WIDTH - 200, 20))
        
        if pygame.time.get_ticks() < freeze_timer:
            freeze_text = game_font_small.render("FREEZE!", True, (0, 200, 255))
            screen.blit(freeze_text, (WIDTH // 2 - 50, 20))
        
    elif state == "GAME_OVER":
        text_over = game_font_medium.render("GAME OVER", True, RED)
        over_rect = text_over.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(text_over, over_rect)

        text_score = game_font_small.render(f"Final Score: {score.value}   Best: {score.high_score}", True, WHITE)
        score_rect = text_score.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
        screen.blit(text_score, score_rect)
        
        text_play = game_font_small.render("Press any key or click to Play Again", True, WHITE)
        play_rect = text_play.get_rect(center=(WIDTH//2, HEIGHT//2 + 80))
        screen.blit(text_play, play_rect)

    for effect in effects[:]:
        effect.update()
        effect.draw(screen)
        if effect.alpha <= 0:
            effects.remove(effect)

    pygame.display.flip()

cap.release()
pygame.quit()