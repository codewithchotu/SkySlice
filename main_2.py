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

# ======================

# SOUNDS

# ======================

bomb_sound = pygame.mixer.Sound(
"sounds/bomb.wav"
)

count_sound = pygame.mixer.Sound(
"sounds/countdown.wav"
)

slash_sound = pygame.mixer.Sound(
"sounds/slash.wav"
)

score_sound = pygame.mixer.Sound(
"sounds/score.wav"
)

game_over_sound = pygame.mixer.Sound(
"sounds/game_over.wav"
)

pygame.mixer.music.load(
"sounds/background.wav"
)

pygame.mixer.music.play(-1)

# ======================

# IMAGES

# ======================

sword_img = pygame.image.load(
"assets/effects/sword.png"
).convert_alpha()

sword_img = pygame.transform.scale(
sword_img,
(100,100)
)

explosion_img = pygame.image.load(
"assets/effects/explosion.png"
).convert_alpha()

explosion_img = pygame.transform.scale(
explosion_img,
(150,150)
)

slash_img = pygame.image.load(
"assets/effects/slash.png"
).convert_alpha()

slash_img = pygame.transform.scale(
slash_img,
(140,140)
)

red_splash = pygame.image.load(
"assets/effects/splash_red.png"
).convert_alpha()

red_splash = pygame.transform.scale(
red_splash,
(160,160)
)

yellow_splash = pygame.image.load(
"assets/effects/splash_yellow.png"
).convert_alpha()

yellow_splash = pygame.transform.scale(
yellow_splash,
(160,160)
)

# ======================

# SCREEN

# ======================

screen = pygame.display.set_mode(
(WIDTH, HEIGHT)
)

pygame.display.set_caption(
"SkySlice"
)

clock = pygame.time.Clock()

# ======================

# CAMERA

# ======================

cap = cv2.VideoCapture(
0,
cv2.CAP_DSHOW
)

if not cap.isOpened():

```
print("Camera not found!")
exit()
```

# ======================

# START MENU

# ======================

def show_start_screen():

```
font_big = pygame.font.SysFont(
    None,
    120
)

font_small = pygame.font.SysFont(
    None,
    50
)

while True:

    screen.fill(
        (20,20,30)
    )

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
        (
            WIDTH//2 - 220,
            200
        )
    )

    screen.blit(
        start,
        (
            WIDTH//2 - 200,
            380
        )
    )

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                return
```

# ======================

# COUNTDOWN

# ======================

def show_countdown():

```
font = pygame.font.SysFont(
    None,
    180
)

for count in [
    "3",
    "2",
    "1",
    "GO!"
]:

    count_sound.play()

    screen.fill(
        (0,0,0)
    )

    text = font.render(
        count,
        True,
        (255,255,255)
    )

    rect = text.get_rect(
        center=(
            WIDTH//2,
            HEIGHT//2
        )
    )

    screen.blit(
        text,
        rect
    )

    pygame.display.flip()

    pygame.time.delay(
        1000
    )
```

# ======================

# GAME OVER SCREEN

# ======================

def game_over_screen(final_score):

```
font_big = pygame.font.SysFont(
    None,
    100
)

font_small = pygame.font.SysFont(
    None,
    60
)

while True:

    screen.fill(
        (0,0,0)
    )

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

    screen.blit(
        game_over,
        (350,180)
    )

    screen.blit(
        score_text,
        (470,300)
    )

    screen.blit(
        restart,
        (350,420)
    )

    screen.blit(
        quit_text,
        (420,500)
    )

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

                return
```

# ======================

# START GAME

# ======================

show_start_screen()

while True:

```
show_countdown()

tracker = HandTracker()

score = Score()

fruits = []

bombs = []

SPAWN = pygame.USEREVENT + 1

pygame.time.set_timer(
    SPAWN,
    FRUIT_SPAWN_TIME
)

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            exit()

        if event.type == SPAWN:

            if random.randint(1,5) == 1:

                bombs.append(
                    Bomb()
                )

            else:

                fruits.append(
                    Fruit()
                )

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
            (
                WIDTH,
                HEIGHT
            )
        )

        frame_surface = pygame.surfarray.make_surface(
            frame_rgb.swapaxes(
                0,
                1
            )
        )

        screen.blit(
            frame_surface,
            (0,0)
        )

    else:

        screen.fill(
            (30,30,40)
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

        screen.blit(
            sword_img,
            (
                fx - 50,
                fy - 50
            )
        )
```

```
    # ======================
    # FRUITS
    # ======================

    for fruit in fruits[:]:

        fruit.update()
        fruit.draw(screen)

        if finger:

            if fruit.rect.collidepoint(
                fx,
                fy
            ):

                slash_sound.play()
                score_sound.play()

                screen.blit(
                    slash_img,
                    (
                        fruit.x - 70,
                        fruit.y - 70
                    )
                )

                splash = random.choice(
                    [
                        red_splash,
                        yellow_splash
                    ]
                )

                screen.blit(
                    splash,
                    (
                        fruit.x - 80,
                        fruit.y - 80
                    )
                )

                fruits.remove(
                    fruit
                )

                score.add()

    # ======================
    # BOMBS
    # ======================

    for bomb in bombs[:]:

        bomb.update()
        bomb.draw(screen)

        if finger:

            if bomb.rect.collidepoint(
                fx,
                fy
            ):

                bomb_sound.play()
                game_over_sound.play()

                screen.blit(
                    explosion_img,
                    (
                        bomb.x - 75,
                        bomb.y - 75
                    )
                )

                pygame.display.flip()

                pygame.time.delay(
                    1000
                )

                running = False

    # ======================
    # SCORE
    # ======================

    font = pygame.font.SysFont(
        None,
        60
    )

    score_text = font.render(
        f"Score: {score.value}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (
            20,
            20
        )
    )

    pygame.display.flip()

# ======================
# GAME OVER
# ======================

game_over_screen(
    score.value
)
```

# ======================

# CLEANUP

# ======================

cap.release()
pygame.quit()
