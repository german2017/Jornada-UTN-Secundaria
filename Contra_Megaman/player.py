import pygame
from characters import CharacterX, CharacterBill

class Player():
    def __init__(self):
        self.score = 0
        self.health = 3
        self.hits = 0
        self.facing_right = True
        self.key_grabbed = False
        self.end_level = False
        self.rank = ""