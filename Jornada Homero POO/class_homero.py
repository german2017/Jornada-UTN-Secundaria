import pygame
from class_dona import Dona

class Homero:
    def __init__(self, paths, ancho, alto, tamaño_boca, alto_ventana):
        self.ancho = ancho
        self.alto = alto
        
        self.imagen_derecha = pygame.image.load(paths["Derecha"])
        self.imagen_derecha = pygame.transform.scale(self.imagen_derecha,(ancho,alto))
        self.imagen_izquierda = pygame.image.load(paths["Izquierda"])
        self.imagen_izquierda = pygame.transform.scale(self.imagen_izquierda,(ancho,alto))
        
        self.orientacion = "Derecha"
        self.imagen = self.imagen_derecha
        
        self.rectangulo = self.imagen.get_rect()
        self.rectangulo.y = alto_ventana - alto
        self.rect_boca = pygame.Rect(0,0,tamaño_boca,tamaño_boca)
        self.rect_boca.center = self.rectangulo.center
        self.puntaje = 0

    def set_orientacion(self, orientacion):
        self.orientacion = orientacion
        if orientacion == "Derecha":
            self.imagen = self.imagen_derecha
        else:
            self.imagen = self.imagen_izquierda
    
    def masticar(self):
        pygame.mixer.init()
        sonido_fondo = pygame.mixer.Sound("Recursos\eat2.mp3")
        sonido_fondo.set_volume(0.7)
        sonido_fondo.play()


    def comer_dona(self, lista_donas:list["Dona"],ventana_ppal:pygame.surface):
        pass

    def moverse(self, orientacion, desplazamiento, pantalla:pygame.surface):
        pass
        
    
