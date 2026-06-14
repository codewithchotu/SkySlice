import pygame
import random

class Effect:
    def __init__(self, image, x, y):
        self.original_image = image
        self.x = x
        self.y = y
        self.alpha = 255
        self.speed_y = -2 # drift up slightly

    def update(self):
        self.alpha -= 15
        self.y += self.speed_y

    def draw(self, screen):
        if self.alpha > 0:
            temp = self.original_image.copy()
            temp.set_alpha(self.alpha)
            rect = temp.get_rect(center=(self.x, self.y))
            screen.blit(temp, rect)

class FloatingText:
    def __init__(self, text, x, y, font, color=(255, 255, 255)):
        self.text_surf = font.render(text, True, color)
        self.x = x
        self.y = y
        self.alpha = 255
        self.speed_y = -3
        
    def update(self):
        self.alpha -= 8
        self.y += self.speed_y
        
    def draw(self, screen):
        if self.alpha > 0:
            temp = self.text_surf.copy()
            temp.set_alpha(self.alpha)
            rect = temp.get_rect(center=(self.x, self.y))
            screen.blit(temp, rect)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.randint(3, 6)
        self.speed_x = random.uniform(-8, 8)
        self.speed_y = random.uniform(-10, 2)
        self.alpha = 255

    def update(self):
        self.speed_y += 0.5 # gravity
        self.x += self.speed_x
        self.y += self.speed_y
        self.alpha -= 8
        self.radius -= 0.05

    def draw(self, screen):
        if self.alpha > 0 and self.radius > 0:
            surf = pygame.Surface((int(self.radius*2), int(self.radius*2)), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, int(self.alpha)), (int(self.radius), int(self.radius)), int(self.radius))
            screen.blit(surf, (int(self.x - self.radius), int(self.y - self.radius)))
