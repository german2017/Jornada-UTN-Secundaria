import pygame
from configurations import import_folder, volume

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = import_folder("resources/graphics/coin", (16, 16))
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.score_value = 100
        self.sfx = pygame.mixer.Sound("resources/sfx/objects/coin.mp3")
        self.sfx.set_volume(volume.sfx_volume)
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        
        self.image = self.animations[int(self.frame_index)]
    
    def collisions(self, player, player_stats):
        if self.rect.colliderect(player.hitbox):
            player_stats.score += self.score_value
            self.sfx.play(0)
            self.kill()
    
    def update(self, player:pygame.sprite.GroupSingle, player_stats):
        self.collisions(player.sprite, player_stats)
        self.animate()
        if self.sfx.get_volume() != volume.sfx_volume:
            self.sfx.set_volume(volume.sfx_volume)

class Door(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_assets()
        self.status = 'static'
        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(bottomleft = pos)
        self.hitbox = pygame.Rect(self.rect.x+16, self.rect.y, 32, 96)
        self.frame_index = 0
        self.animation_speed = 0.1
        self.sfx = pygame.mixer.Sound("resources/sfx/objects/door.mp3")
        self.sfx.set_volume(volume.sfx_volume)
        self.sfx_flag = True

    def import_assets(self):
        character_path = "resources/graphics/door/"
        
        self.animations = {'static':[], 'open':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path,(64, 96))
            
    def check_key_grabbed(self, player_stats):
        if player_stats.key_grabbed:
            if self.sfx_flag:
                self.sfx.play(0)
                self.sfx_flag = False
            self.status = 'open'
    
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'open':
                self.kill()
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
    
    def update(self, player_stats):
        self.check_key_grabbed(player_stats)
        self.animate()
        if self.sfx.get_volume() != volume.sfx_volume:
            self.sfx.set_volume(volume.sfx_volume)

class Key(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = import_folder("resources/graphics/key", (32, 32))
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        
        self.image = self.animations[int(self.frame_index)]
    
    def collisions(self, player, player_stats):
        if self.rect.colliderect(player.hitbox):
            player_stats.key_grabbed = True
            self.kill()
    
    def update(self, player:pygame.sprite.GroupSingle, player_stats):
        self.collisions(player.sprite, player_stats)
        self.animate()
    
class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, status):
        super().__init__()
        self.import_assets()
        self.status = status
        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(bottomleft = pos)
        if self.status == 'on':
            height = 94
        else:
            height = 0
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 32, height)
        self.frame_index = 0
        self.animation_speed = 0.2

    def import_assets(self):
        character_path = "resources/graphics/laser/"
        
        self.animations = {'on':[], 'off':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path,(32, 96))
            
    def check_button_pressed(self, buttons):
        for button in buttons.sprites():
            if button.status == 'on':
                if self.status == 'on':
                    self.status = 'off'
                    self.hitbox.height = 0
                else:
                    self.status = 'on'
                    self.hitbox.height = 94
                break

    def check_collisions(self, player, bullets):
        if player.hitbox.colliderect(self.hitbox):
            if player.direction.x < 0:
                player.hitbox.left = self.hitbox.right
            elif player.direction.x > 0:
                player.hitbox.right = self.hitbox.left
            if not player.invulnerable:
                player.pain = True
                player.invulnerability_timer = pygame.time.get_ticks()
                player.speed = 1
        
        for bullet in bullets.sprites():
            if bullet.rect.colliderect(self.hitbox):
                bullet.kill()
    
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
    
    def update(self, player, bullets, button):
        self.check_collisions(player.sprite, bullets)
        self.check_button_pressed(button)
        self.animate()

class Button(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_assets()
        self.status = 'off'
        self.frame_index = 0
        self.delay = 0
        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(topleft = pos)

    def import_assets(self):
        character_path = "resources/graphics/button/"
        
        self.animations = {'on':[], 'off':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path,(16, 32))
    
    def animate(self):
        if pygame.time.get_ticks() - self.delay > 500:
            self.image = self.animations[self.status][0]
            if self.status == 'on':
                self.delay = pygame.time.get_ticks()
    
    def collisions(self, bullets):
        self.status = 'off'
        for bullet in bullets.sprites():
            if self.rect.colliderect(bullet.rect) and\
                pygame.time.get_ticks() - self.delay > 500:
                self.status = 'on'
                bullet.kill()
    
    def update(self, bullets):
        self.collisions(bullets)
        self.animate()

class Goal(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("resources/graphics/goal/1.png")
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(topleft = pos)
    
    def check_player(self, player, player_stats):
        if self.rect.colliderect(player.hitbox):
            player_stats.end_level = True

    def update(self, player, player_stats):
        self.check_player(player.sprite, player_stats)

class Health(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = import_folder("resources/graphics/heart", (32,32))
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frame_index = 0
        self.animation_speed = 0.1
        self.sfx = pygame.mixer.Sound("resources/sfx/objects/live.mp3")
        self.sfx.set_volume(volume.sfx_volume)

    def animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        
        image = self.animations[int(self.frame_index)]
        self.image = image
    
    def check_collissions(self, player, player_stats):
        # Player collision
        if self.rect.colliderect(player.hitbox):
            if player_stats.health < 3:
                player_stats.health += 1
                self.sfx.play(0)
                self.kill()
    
    def update(self, player:pygame.sprite.GroupSingle, player_stats):
        self.animation()
        self.check_collissions(player.sprite, player_stats)
        if self.sfx.get_volume() != volume.sfx_volume:
            self.sfx.set_volume(volume.sfx_volume)

class Spike(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = import_folder("resources/graphics/spike", (30,32))[0]
        self.rect = self.image.get_rect(topleft = pos)
    
    def check_collissions(self, player, player_stats):
        # Player collision
        if not player.invulnerable:
            if self.rect.colliderect(player.hitbox):
                player.pain = True
                player.invulnerability_timer = pygame.time.get_ticks()
                player.speed = 1
    
    def update(self, player:pygame.sprite.GroupSingle, player_stats):
        self.check_collissions(player.sprite, player_stats)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, climbable):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.climbable = climbable

class UnderConstructionSign(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("resources/graphics/under construction.png")
        self.rect = self.image.get_rect(bottomleft = pos)