import pygame
import random
from colores import *
from class_dona import Dona
from class_homero import Homero


FPS = 60
ancho = 200
alto = 250
tamaño_pantalla = (800, 800)

score = 0
running = True

pygame.init()
RELOJ = pygame.time.Clock()

#config inicial
screen = pygame.display.set_mode(tamaño_pantalla)
pygame.display.set_caption("HOMER DONUTS")
icono = pygame.image.load("Recursos\ico.png")
pygame.display.set_icon(icono)


tick = pygame.USEREVENT + 0
pygame.time.set_timer(tick, 100)

#homero
paths = {}
paths["Derecha"] = "Recursos\derecha.png"
paths["Izquierda"] = "Recursos\izquierda.png"
mi_homero = Homero(paths, ancho, alto, 50, tamaño_pantalla[1])

#donas
lista_donas = Dona.crear_lista_donas(30)

#La musica de fondo
pygame.mixer.init()
sonido_fondo = pygame.mixer.Sound("Recursos\musica.mp3")
sonido_fondo.set_volume(0.2)
sonido_fondo.play()
#fondo
fondo = pygame.image.load("Recursos\\fondo.png")
fondo_final = pygame.transform.scale(fondo,tamaño_pantalla)


while running:
    screen.blit(fondo,(0,0))
    screen.blit(mi_homero.imagen,mi_homero.rectangulo)
    RELOJ.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == tick:
            Dona.update(lista_donas, screen)
    
    lista_teclas = pygame.key.get_pressed()

    if lista_teclas[pygame.K_LEFT] :
        mi_homero.moverse("Izquierda", -10, screen)
    elif lista_teclas[pygame.K_RIGHT] :
        mi_homero.moverse("Derecha", 10, screen)

            
        
    mi_homero.comer_dona(lista_donas, screen)
    
    
    pygame.draw.rect(screen, AZUL, mi_homero.rectangulo, 3)
    pygame.draw.rect(screen, VERDE, mi_homero.rect_boca, 3)
    
    pygame.display.flip()
    
pygame.quit()




