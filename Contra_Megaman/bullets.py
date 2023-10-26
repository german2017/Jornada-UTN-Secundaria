import pygame
from configurations import import_folder, volume

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos:tuple, shoot_right:bool, shoot_up:bool,
    img_path:str, size:tuple):
        super().__init__()
        self.image = import_folder(img_path, size)[0]
        self.rect = self.image.get_rect(center = pos)
        self.bullet_right = shoot_right
        self.bullet_up = shoot_up
        self.speed = 12
    
    def move(self):
        if self.bullet_up:
            self.rect.y -= self.speed
        else:
            if self.bullet_right:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed
    
    def check_collissions(self, tiles:pygame.sprite.Group, screen):
        for tile in tiles.sprites():
            if self.rect.colliderect(tile):
                self.kill()
        # Screen limits collision
            screen_width = screen.get_width()
            screen_height = screen.get_height()

            if self.rect.right > screen_width:
                self.kill()
            elif self.rect.left < 0:
                self.kill()
            
            if self.rect.bottom > screen_height:
                self.kill()
            elif self.rect.bottom < 0:
                self.kill()
        
    def update(self, tiles, screen):
        self.check_collissions(tiles, screen)
        self.move()

class GunVoltBullet(pygame.sprite.Sprite):
    def __init__(self, pos, move_right):
        super().__init__()
        self.animations = import_folder("resources/graphics/enemies/gunvolt/shot", (32,32))
        self.image = self.animations[0]
        self.rect = self.image.get_rect(center = pos)

        # Status
        self.move_right = move_right
        self.counter = 4
        self.frame_index = 0
        self.animation_speed = 0.5

        self.sfx = pygame.mixer.Sound("resources/sfx/zap.mp3")
        self.sfx.set_volume(volume.sfx_volume)
        self.sfx.play(0)

    def animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        
        image = self.animations[int(self.frame_index)]
        self.image = image

    def move(self):
        if self.counter:
            self.rect.y += 6
            self.counter -= 1
        if self.move_right:
            self.rect.x += 10
        else:
            self.rect.x -= 10
    
    def check_collissions(self, tiles:pygame.sprite.Group, screen, player):
        # Tiles collision
        for tile in tiles.sprites():
            if self.rect.colliderect(tile):
                self.kill()
        
        # Screen limits collision
        screen_width = screen.get_width()
        if self.rect.right > screen_width:
            self.kill()
        elif self.rect.left < 0:
            self.kill()
        
        # Player collision
        if not player.invulnerable:
            if self.rect.colliderect(player.hitbox):
                player.pain = True
                player.invulnerability_timer = pygame.time.get_ticks()
                player.speed = 1
    
    def update(self, tiles, screen, player:pygame.sprite.GroupSingle):
        self.move()
        self.animation()
        self.check_collissions(tiles, screen, player.sprite)

class RoboBigFuzzBullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.animations = import_folder("resources/graphics/enemies/boss/bullet", (90,90))
        self.image = self.animations[0]
        self.rect = self.image.get_rect(center = pos)

        # Status
        self.frame_index = 0
        self.animation_speed = 0.3

        # Direction
        self.direction = direction

        self.sfx = pygame.mixer.Sound("resources/sfx/flame.mp3")
        self.sfx.set_volume(volume.sfx_volume)
        self.sfx.play(0)

    def animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        
        image = self.animations[int(self.frame_index)]
        self.image = image

    def move(self):
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]
    
    def check_collissions(self, tiles:pygame.sprite.Group, player):
        # Tiles collision
        for tile in tiles.sprites():
            if self.rect.colliderect(tile):
                self.kill()
        
        # Player collision
        if not player.invulnerable:
            if self.rect.colliderect(player.hitbox):
                player.pain = True
                player.invulnerability_timer = pygame.time.get_ticks()
                player.speed = 1
    
    def update(self, tiles, player:pygame.sprite.GroupSingle):
        self.move()
        self.animation()
        self.check_collissions(tiles, player.sprite)