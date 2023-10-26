import pygame
import random

class Dona:
    def __init__(self, path, pos_x, pos_y, ancho, alto):
        self.imagen = pygame.image.load(path)
        self.imagen = pygame.transform.scale(self.imagen,(ancho,alto)) 
        self.rectangulo = self.imagen.get_rect()
        self.rectangulo.x = pos_x
        self.rectangulo.y = pos_y
        self.visible = True
        self.velocidad = random.randrange(10,20,1)
    
    def reciclar_dona(self):
        self.rectangulo.x = random.randrange (0,740,60)
        self.rectangulo.y = random.randrange (-1000,0,60)

    @staticmethod
    def update(lista_donas:list["Dona"], ventana_ppal):
        pass    
        

    @staticmethod
    def crear_lista_donas(cantidad):
        pass
