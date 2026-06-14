import cv2
import pygame
import random

from settings import *
from hand_tracker import HandTracker
from fruit import Fruit
from bomb import Bomb
from score import Score

pygame.init()
pygame.mixer.init()



bomb_sound = pygame.mixer.Sound(
    "sounds/bomb.wav"
)

count_sound = pygame.mixer.Sound(
    "sounds/countdown.wav"
)

explosion_img = pygame.image.load(
    "assets/effects/explosion.png"
).convert_alpha()

explosion_img = pygame.transform.scale(
    explosion_img,
    (120, 120)
)

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "SkySlice"
)

clock = pygame.time.Clock()

cap = cv2.VideoCapture(
    0,
    cv2.CAP_DSHOW
)

if not cap.isOpened():
    print("Camera not found!")
    exit()

tracker = HandTracker()
score = Score()

fruits = []
bombs = []

SPAWN = pygame.USEREVENT + 1

pygame.time.set_timer(
    SPAWN,
    FRUIT_SPAWN_TIME
)
font = pygame.font.SysFont(None, 180)

for count in ["3", "2", "1", "GO!"]:

    if ret:
        screen.blit(frame_surface, (0, 0))
    else:
        screen.fill((30,30,40))

    text = font.render(
        count,
        True,
        (255,255,255)
    )

    rect = text.get_rect(
        center=(WIDTH//2, HEIGHT//2)
    )

    screen.blit(text, rect)

    pygame.display.flip()

    pygame.time.delay(1000)

    tracker = HandTracker()
score = Score()

fruits = []
bombs = []

SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN, FRUIT_SPAWN_TIME)

pygame.init()

# load sounds
# load images
# create screen
# create camera

def show_start_screen():

    # start menu code here
    pass


def game_over_screen(final_score):

    font_big = pygame.font.SysFont(None, 100)
    font_small = pygame.font.SysFont(None, 60)

    while True:

        screen.fill((0,0,0))

        game_over = font_big.render(
            "GAME OVER",
            True,
            (255,0,0)
        )

        score_text = font_small.render(
            f"Score: {final_score}",
            True,
            (255,255,255)
        )

        restart = font_small.render(
            "Press R to Play Again",
            True,
            (0,255,0)
        )

        quit_text = font_small.render(
            "Press Q to Quit",
            True,
            (255,255,0)
        )

        screen.blit(game_over,(180,180))
        screen.blit(score_text,(280,300))
        screen.blit(restart,(180,400))
        screen.blit(quit_text,(220,480))

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

                if event.key == pygame.K_r:
                    return True


show_start_screen()

running = True

while running:

    # game code

# ======================
# COUNTDOWN START
# ======================

font = pygame.font.SysFont(None, 180)

for count in ["3", "2", "1", "GO!"]:

    count_sound.play()

    screen.fill((0,0,0))

    text = font.render(
        count,
        True,
        (255,255,255)
    )

    rect = text.get_rect(
        center=(WIDTH//2, HEIGHT//2)
    )

    screen.blit(text, rect)

    pygame.display.flip()

    pygame.time.delay(1000)

    show_start_screen()

# ======================
# COUNTDOWN END
# ======================

running = True

def show_start_screen():

    font_big = pygame.font.SysFont(None, 100)
    font_small = pygame.font.SysFont(None, 50)

    while True:

        screen.fill((20,20,30))

        title = font_big.render(
            "SkySlice",
            True,
            (255,255,255)
        )

        start = font_small.render(
            "Press SPACE to Start",
            True,
            (0,255,0)
        )

        screen.blit(
            title,
            (WIDTH//2 - 180, 200)
        )

        screen.blit(
            start,
            (WIDTH//2 - 200, 350)
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    return

while running:


    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_over_screen(score.value)
score = Score()
fruits = []
bombs = []

        if event.type == SPAWN:

            if random.randint(1, 5) == 1:
                bombs.append(Bomb())
            else:
                fruits.append(Fruit())

    ret, frame = cap.read()

    finger = None

    if ret:

        frame = cv2.flip(
            frame,
            1
        )

        finger = tracker.get_index_finger(
            frame
        )

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frame_rgb = cv2.resize(
            frame_rgb,
            (WIDTH, HEIGHT)
        )

        frame_surface = pygame.surfarray.make_surface(
            frame_rgb.swapaxes(0, 1)
        )

        screen.blit(
            frame_surface,
            (0, 0)
        )

    else:

        screen.fill(
            (30, 30, 40)
        )

    fx = None
    fy = None

    if finger:

        fx = int(
            finger[0] * WIDTH /
            frame.shape[1]
        )

        fy = int(
            finger[1] * HEIGHT /
            frame.shape[0]
        )

        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (fx, fy),
            12
        )

    # Fruits

    for fruit in fruits[:]:

        fruit.update()
        fruit.draw(screen)

        if finger:

            if fruit.rect.collidepoint(
                fx,
                fy
            ):

                fruits.remove(fruit)
                score.add()

    # Bombs

    for bomb in bombs[:]:

        bomb.update()
        bomb.draw(screen)

        if finger:

            if bomb.rect.collidepoint(
                fx,
                fy
            ):

                bomb_sound.play()

                screen.blit(
                    explosion_img,
                    (
                        bomb.x - 60,
                        bomb.y - 60
                    )
                )

                pygame.display.flip()

                pygame.time.delay(
                    700
                )

                running = False

    # Score

    font = pygame.font.SysFont(
        None,
        50
    )

    text = font.render(
        f"Score: {score.value}",
        True,
        WHITE
    )

    screen.blit(
        text,
        (20, 20)
    )

    pygame.display.flip()

cap.release()

# GAME OVER SCREEN

screen.fill(
    (0, 0, 0)
)

font = pygame.font.SysFont(
    None,
    80
)

game_over_text = font.render(
    "GAME OVER",
    True,
    (255, 0, 0)
)

score_text = font.render(
    f"Score: {score.value}",
    True,
    (255, 255, 255)
)

screen.blit(
    game_over_text,
    (180, 250)
)

screen.blit(
    score_text,
    (250, 350)
)

pygame.display.flip()

pygame.time.delay(
    3000
)

pygame.quit()