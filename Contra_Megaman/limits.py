import pygame

class ClimbLimit():
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 32, 8)

class EnemyLimit:
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)