import pygame
from configurations import import_folder, volume
from bullets import GunVoltBullet, RoboBigFuzzBullet

sfx_explosion = pygame.mixer.Sound("resources/sfx/explosion.mp3")
sfx_hit = pygame.mixer.Sound("resources/sfx/enemy hit.wav")


class BallDeVoux(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # Animation
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image:pygame.surface.Surface = self.animations['walk'][self.frame_index]

        # Hitbox
        self.rect = self.image.get_rect(bottomleft = pos)
        self.hitbox = pygame.Rect(self.rect.x+28, self.rect.y+2, 40, 40)

        # Movement
        self.direction = -1
        self.speed = 1

        # Status
        self.status = 'walk'
        self.facing_left = True
        self.health = 6
        self.dead = False
        self.score_value = 500
    
    def import_assets(self):
        character_path = "resources/graphics/enemies/balldevoux/"
        
        self.animations = {'walk':[], 'turn':[], 'explosion':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path,
                                                    (108, 104))
    
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.status == 'turn':
                self.status = 'walk'
            if self.status == 'explosion':
                self.kill()

        image = animation[int(self.frame_index)]

        if self.status != 'turn':
            if self.facing_left:
                self.image = image
                self.rect.x, self.rect.y = self.hitbox.x-28, self.hitbox.y-2
                self.direction = -1
            else:
                self.image = pygame.transform.flip(image, True, False)
                self.rect.x, self.rect.y = self.hitbox.x-40, self.hitbox.y-2
                self.direction = 1
        else:
            if self.facing_left:
                self.image = pygame.transform.flip(image, True, False)
            else:
                self.image = image
    
    def get_status(self):
        if self.dead:
            self.frame_index = 0
            self.animation_speed = 0.2
            self.status = 'explosion'
            self.hitbox.y -= 20
        elif self.direction != 0:
            self.status = 'walk'
        else:
            self.status = 'turn'
    
    def check_collisions(self, limits:list, bullets:pygame.sprite.Group, player, player_stats):
        # Horizontal collision
        if self.direction != 0:
            self.hitbox.x += self.speed * self.direction

            for limit in limits:
                if limit.rect.colliderect(self.hitbox):
                    if self.facing_left:
                        self.hitbox.left = limit.rect.right
                        self.facing_left = False
                    else:
                        self.hitbox.right = limit.rect.left
                        self.facing_left = True
                    self.frame_index = 0
                    self.direction = 0
        
        # Bullets collision
        if len(bullets):
            for bullet in bullets.sprites():
                if self.hitbox.colliderect(bullet):
                    sfx_hit.set_volume(volume.sfx_volume)
                    sfx_hit.play(0)
                    self.health -= player.damage
                    if self.health <= 0:
                        self.dead = True
                        sfx_explosion.set_volume(volume.sfx_volume)
                        sfx_explosion.play(0)
                        player_stats.score += self.score_value
                    bullet.kill()

        # Player collision
        if not player.invulnerable:
            if self.hitbox.colliderect(player.hitbox):
                player.pain = True
                player.invulnerability_timer = pygame.time.get_ticks()
                player.speed = 1

    def update(self, limits, bullets, player:pygame.sprite.GroupSingle, tiles, screen, current_time, player_stats):
        if not self.dead:
            self.check_collisions(limits, bullets, player.sprite, player_stats)
            self.get_status()
        self.animate()

class Spiky(pygame.sprite.Sprite):
    def __init__(self, pos, score):
        super().__init__()

        # Animation
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 0.4
        self.image:pygame.surface.Surface = self.animations['spin'][self.frame_index]

        # Hitbox
        self.rect = self.image.get_rect(bottomleft = pos)
        self.hitbox = pygame.Rect(self.rect.x+6, self.rect.y+6, 64, 64)

        # Movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 3
        self.gravity = 0.6
        self.fall_speed_limit = 15
        self.on_ground = False
        self.on_ceiling = False

        # Status
        self.status = 'spin'
        self.facing_left = True
        self.health = 5
        self.dead = False
        self.score_value = score
    
    def import_assets(self):
        character_path = "resources/graphics/enemies/spiky/"
        
        self.animations = {'spin':[], 'death':[], 'explosion':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path,
                                                    (76, 76))

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.status == 'explosion':
                self.kill()
            if self.status == 'death':
                self.hitbox.y -= 20
                self.status = 'explosion'

        image = animation[int(self.frame_index)]

        if self.facing_left:
            self.image = image
            self.rect.x, self.rect.y = self.hitbox.x-6, self.hitbox.y-6
            self.direction.x = -1
        else:
            self.image = pygame.transform.flip(image, True, False)
            self.rect.x, self.rect.y = self.hitbox.x-6, self.hitbox.y-6
            self.direction.x = 1
    
    def get_status(self):
        if self.dead:
            self.frame_index = 0
            self.animation_speed = 0.2
            self.status = 'death'
        elif self.direction.x != 0:
            self.status = 'spin'
    
    def apply_gravity(self):
        if self.direction.y + self.gravity <= self.fall_speed_limit:
            self.direction.y += self.gravity
        self.hitbox.y += self.direction.y

    def check_collisions(self, tiles:pygame.sprite.Group, bullets, player, screen, player_stats):
        # Horizontal collision
        if self.direction.x != 0:
            self.hitbox.x += self.direction.x * self.speed

            for tile in tiles.sprites():
                if self.hitbox.colliderect(tile.rect):
                    if self.direction.x < 0:
                        self.hitbox.left = tile.rect.right
                        self.facing_left = False
                    elif self.direction.x > 0:
                        self.hitbox.right = tile.rect.left
                        self.facing_left = True
        
        # Vertical collision
        self.apply_gravity()

        for tile in tiles.sprites():
            if self.hitbox.colliderect(tile.rect):
                if self.direction.y > 0:
                    self.hitbox.bottom = tile.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:
                    self.hitbox.top = tile.rect.bottom
                    self.direction.y = 0
                    self.on_ceiling = True
        
        if self.on_ground and self.direction.y != 0:
            self.on_ground = False
        if self.on_ceiling and self.direction.y > 0:
            self.on_ceiling = False
        
        # Screen limits collision
        height = screen.get_height()
        if self.rect.top > height:
            self.kill()
        
        # Bullet collision
        if len(bullets):
            for bullet in bullets.sprites():
                if self.hitbox.colliderect(bullet):
                    sfx_hit.set_volume(volume.sfx_volume)
                    sfx_hit.play(0)
                    self.health -= player.damage
                    if self.health <= 0:
                        self.dead = True
                        sfx_explosion.set_volume(volume.sfx_volume)
                        sfx_explosion.play(0)
                        player_stats.score += self.score_value
                    bullet.kill()

        # Player collision
        if not player.invulnerable:
            if self.hitbox.colliderect(player.hitbox):
                player.pain = True
                player.invulnerability_timer = pygame.time.get_ticks()
                player.speed = 1
    
    def update(self, limits, bullets, player, tiles:pygame.sprite.Group, screen, current_time, player_stats):
        if not self.dead:
            self.check_collisions(tiles, bullets, player.sprite, screen, player_stats)
            self.get_status()
        self.animate()

class GunVolt(pygame.sprite.Sprite):
    def __init__(self, pos, facing_right):
        super().__init__()

        # Animation
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 0.2
        self.image:pygame.surface.Surface = self.animations['idle'][self.frame_index]

        # Hitbox
        self.rect = self.image.get_rect(bottomleft = pos)
        self.hitbox = pygame.Rect(self.rect.x+22, self.rect.y+14, 72, 110)

        # Status
        self.facing_right = facing_right
        self.status = 'idle'
        self.attack = False
        self.health = 20
        self.dead = False
        self.score_value = 1000
        self.shot_timer = 0

        # Bullet
        self.bullets = pygame.sprite.Group()
    
    def import_assets(self):
        character_path = "resources/graphics/enemies/gunvolt/"
        
        self.animations = {'idle':[], 'start':[], 'stop':[], 'explosion':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path,
                                                    (116, 128))
    
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.status == 'explosion':
                self.kill()
        image = animation[int(self.frame_index)]

        if self.facing_right:
            image = pygame.transform.flip(image,True,False)

        self.image = image
        self.rect.x, self.rect.y = self.hitbox.x-22, self.hitbox.y-14
        self.direction = -1
    
    def get_status(self, player, current_time):
        if self.dead:
            self.frame_index = 0
            self.status = 'explosion'
            self.hitbox.y -= 20
        else:
            if not self.facing_right:
                if self.hitbox.centerx > player.hitbox.centerx > self.hitbox.centerx-350\
                    and self.hitbox.top < player.hitbox.centery < self.hitbox.top+110\
                    and not self.attack and current_time - self.shot_timer > 2000:
                    self.status = 'start'
                    self.attack = True
                    self.frame_index = 0
                    self.shot_timer = pygame.time.get_ticks()
            else:
                if self.hitbox.centerx < player.hitbox.centerx < self.hitbox.centerx+350\
                    and self.hitbox.top < player.hitbox.centery < self.hitbox.top+110\
                    and not self.attack and current_time - self.shot_timer > 2000:
                    self.status = 'start'
                    self.attack = True
                    self.frame_index = 0
                    self.shot_timer = pygame.time.get_ticks()
            
            if self.status == 'start' and self.frame_index + self.animation_speed > len(self.animations['start']):
                self.generate_bullets()
                self.status = 'stop'
            elif self.status == 'stop' and self.frame_index + self.animation_speed > len(self.animations['stop']):
                self.attack = False
                self.status = 'idle'
            elif not self.attack:
                self.status = 'idle'
    
    def generate_bullets(self):
        x = self.hitbox.centerx - 30
        y = self.hitbox.centery + 14
        self.bullets.add(GunVoltBullet((x,y),self.facing_right))
        self.bullets.add(GunVoltBullet((x+38,y),self.facing_right))
    
    def check_collisions(self, bullets:pygame.sprite.Group, player, player_stats):
        # Bullets collision
        if len(bullets) and self.attack:
            for bullet in bullets.sprites():
                if self.hitbox.colliderect(bullet):
                    sfx_hit.set_volume(volume.sfx_volume)
                    sfx_hit.play(0)
                    self.health -= player.damage
                    if self.health <= 0:
                        self.dead = True
                        sfx_explosion.set_volume(volume.sfx_volume)
                        sfx_explosion.play(0)
                        player_stats.score += self.score_value
                    bullet.kill()

        # Player collision
        if not player.invulnerable:
            if self.hitbox.colliderect(player.hitbox):
                player.pain = True
                player.invulnerability_timer = pygame.time.get_ticks()
                player.speed = 1

    def update(self, limits, bullets, player:pygame.sprite.GroupSingle, tiles, screen, current_time, player_stats):
        if not self.dead:
            self.check_collisions(bullets, player.sprite, player_stats)
            self.get_status(player.sprite, current_time)
        self.animate()
        self.bullets.update(tiles, screen, player)
        self.bullets.draw(screen)

class RoboBigFuzz(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # Animation
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image:pygame.surface.Surface = self.animations['idle'][self.frame_index]

        # Hitbox
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(self.rect.x+228, self.rect.y+20, 120, 150)

        # Status
        self.status = 'idle'
        self.health = 100
        self.dead = False
        self.score_value = 10000
        self.bullet_delay = 0
        self.attack_delay = pygame.time.get_ticks() - 5000
        self.attack = False
        self.cover_blocks = False
        self.second_phase = False

        # Bullet
        self.bullets = pygame.sprite.Group()
        self.bullet_x = 0
        self.bullet_y = 0
        self.y_pos_limit = False
        self.y_neg_limit = False
        self.x_limit = False
        self.bullet_flag = True
    
    def import_assets(self):
        character_path = "resources/graphics/enemies/boss/"
        
        self.animations = {'idle':[], 'attack 1':[], 'explosion':[], 'laugh':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path,(576, 432))
    
    def get_status(self, player_stats):
        if self.dead:
            self.frame_index = 0
            self.animation_speed = 0.1
            self.status = 'explosion'
            self.rect.y -= 50
        elif player_stats.health <= 0:
            if self.status != 'laugh':
                self.frame_index = 0
            self.animation_speed = 0.15
            self.status = 'laugh'
        else:
            if self.attack:
                self.animation_speed = 0.008
                if self.status != 'attack 1':
                    self.frame_index = 0
                self.status = 'attack 1'
            else:
                self.animation_speed = 0.15
                if self.status != 'idle':
                    self.frame_index = 0
                self.status = 'idle'
    
    def attack_1(self):
        if pygame.time.get_ticks() - self.bullet_delay > 120:
            if self.bullet_flag:
                self.y_pos_limit = False
                self.y_neg_limit = False
                self.x_limit = False
                self.bullet_x = 8
                self.bullet_y = 0
                self.bullet_flag = False

            self.bullets.add(RoboBigFuzzBullet((self.hitbox.centerx, self.hitbox.centery+50),
                                                (self.bullet_x, self.bullet_y)))
            self.bullet_delay = pygame.time.get_ticks()

            if self.bullet_y == 8:
                self.y_pos_limit = True
            elif self.y_pos_limit and self.bullet_y == 0:
                self.y_neg_limit = True

            if not self.y_pos_limit:
                self.bullet_y += 1
            elif not self.y_neg_limit:
                self.bullet_y -= 1
            
            if self.bullet_x == -8:
                self.x_limit = True
                self.y_pos_limit = False
                self.y_neg_limit = False
            
            if self.bullet_x > -8 and not self.x_limit:
                self.bullet_x -= 1
            elif self.bullet_x < 8:
                self.bullet_x += 1
            
            if self.x_limit and self.y_neg_limit:
                self.attack = False
                self.bullet_flag = True
    
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.status == 'explosion':
                self.kill()

        self.image = animation[int(self.frame_index)]
    
    def check_collisions(self, bullets:pygame.sprite.Group, player, player_stats):
        # Bullets collision
        if len(bullets):
            for bullet in bullets.sprites():
                if self.hitbox.colliderect(bullet):
                    sfx_hit.set_volume(volume.sfx_volume)
                    sfx_hit.play(0)
                    self.health -= player.damage
                    if self.health <= 0:
                        self.dead = True
                        sfx_explosion.set_volume(volume.sfx_volume)
                        sfx_explosion.play(0)
                        player_stats.score += self.score_value
                    bullet.kill()
    
    def update(self, screen, tiles, player, update, bullets, player_stats):
        if not self.dead:
            if pygame.time.get_ticks() - self.attack_delay > 7500:
                self.attack = True
                self.attack_delay = pygame.time.get_ticks()
            elif 7000 < pygame.time.get_ticks() - self.attack_delay < 7020:
                self.cover_blocks = True
            else:
                self.cover_blocks = False
            
            if update == 'bullets':
                if self.attack:
                    self.attack_1()
                self.bullets.update(tiles, player)
                self.bullets.draw(screen)
                pygame.draw.rect(screen, 'red',(440,180,400,30))
                pygame.draw.rect(screen, 'green',(440,180,self.health*4,30))
                pygame.draw.rect(screen, 'black',(440,180,400,30),4)
            elif not self.dead:
                self.check_collisions(bullets, player.sprite, player_stats)
                self.get_status(player_stats)
        self.animate()
        