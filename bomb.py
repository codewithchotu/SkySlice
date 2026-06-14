import pygame
import random

class Bomb:

    def __init__(self):

        self.image = pygame.image.load(
            "assets/bombs/bomb.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (80, 80)
        )

        self.x = random.randint(200, 1080)
        self.y = 800

        self.speed_x = random.randint(-5, 5)
        self.speed_y = random.randint(-25, -18)

        self.rect = self.image.get_rect(
            center=(self.x, self.y)
        )

    def update(self, gravity_mult=1.0):

        self.speed_y += 0.5 * gravity_mult # gravity
        self.x += self.speed_x * gravity_mult
        self.y += self.speed_y

        self.rect.center = (
            self.x,
            self.y
        )
        return self.y > 1000 and self.speed_y > 0

    def draw(self, screen):

        screen.blit(
            self.image,
            self.rect
        )