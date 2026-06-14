import pygame
import random

class Fruit:

    images = [
        "assets/fruits/apple.png",
        "assets/fruits/banana.png",
        "assets/fruits/strawberry.png",
        "assets/fruits/kiwi.png",
        "assets/fruits/mango.png",
        "assets/fruits/orange.png",
        "assets/fruits/pineapple.png",
        "assets/fruits/watermelon.png"
    ]

    def __init__(self, special=None):

        self.filename = random.choice(Fruit.images)

        self.image = pygame.image.load(
            self.filename
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

        self.special_type = special
        if self.special_type is None:
            r = random.randint(1, 15)
            if r == 1:
                self.special_type = 'FREEZE'
            elif r == 2:
                self.special_type = 'FRENZY'

        if self.special_type == 'FREEZE':
            tint = pygame.Surface((80, 80), pygame.SRCALPHA)
            tint.fill((0, 150, 255, 100))
            self.image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        elif self.special_type == 'FRENZY':
            tint = pygame.Surface((80, 80), pygame.SRCALPHA)
            tint.fill((255, 200, 0, 100))
            self.image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        self.radius = 40

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