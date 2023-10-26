import pygame
from configurations import import_folder, volume

class CharacterX(pygame.sprite.Sprite):
    def __init__(self, pos:tuple, facing_right):
        super().__init__()

        # Animation
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.25
        self.image = self.animations['d_walk'][self.frame_index]

        # Hitbox
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = pygame.Rect(self.rect.x+40, self.rect.y+36, 28, 60)

        # Movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 5
        self.gravity = 0.8
        self.jump_speed = -12
        self.fall_speed_limit = 15

        # Status
        self.status = 'd_idle'
        self.prev_status = ''
        self.facing_right = facing_right
        self.on_ground = False
        self.on_ceiling = False
        self.shooting = False
        self.pain = False
        self.invulnerability_timer = 0
        self.invulnerable = False
        self.damage = 2
        self.fire_rate = 250
        self.dead = False

        # SFX
        self.sfx_pain = pygame.mixer.Sound("resources/sfx/characters/x/hurt.wav")
        self.sfx_death = pygame.mixer.Sound("resources/sfx/characters/x/death.wav")
        self.sfx_death_flag = True

    def import_character_assets(self):
        character_path =\
            "resources/graphics/characters/x/"
        
        self.animations = {'d_idle':[], 'd_walk':[], 'd_jump':[], 'd_fall':[],
                           's_idle':[], 's_walk':[], 's_jump':[], 's_fall':[],
                           'pain':[],'death':[],'victory':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path,
                                                    (100, 100))

    def get_input(self):
        if not self.pain and not self.dead and self.status != 'victory':
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.facing_right = True
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.facing_right = False
            else:
                self.direction.x = 0
            
            if keys[pygame.K_z] and self.on_ground:
                self.direction.y = self.jump_speed
            
            if keys[pygame.K_x]:
                self.shooting = True
            else:
                self.shooting = False

    def get_status(self, current_time, player_stats):
        
        if self.shooting:
            prefix = 's_'
        else:
            prefix = 'd_'
        
        if player_stats.health <= 0:
            if self.sfx_death_flag:
                self.sfx_death.set_volume(volume.sfx_volume)
                self.sfx_death.play(0)
                self.sfx_death_flag = False
            self.status = 'death'
            self.shooting = False
            self.animation_speed = 0.06
            self.direction.x = 0
        elif self.pain:
            self.shooting = False
            self.status = 'pain'
            if self.prev_status != 'pain':
                player_stats.hits += 1
                player_stats.health -= 1
                self.sfx_pain.set_volume(volume.sfx_volume)
                self.sfx_pain.play(0)
            if self.facing_right:
                self.direction.x = -1
            else:
                self.direction.x = 1
            self.invulnerable = True
        elif self.direction.y < 0:
            self.status = prefix + 'jump'
        elif self.direction.y > 0:
            self.status = prefix + 'fall'
        else:
            if self.direction.x != 0:
                self.status = prefix + 'walk'
            else:
                self.status = prefix + 'idle'
        
        if current_time - self.invulnerability_timer > 1500:
            self.invulnerable = False
        
        if player_stats.end_level:
            self.status = 'victory'
            self.direction.x = 0
        
        if self.status != self.prev_status:
            self.frame_index = 0
            self.prev_status = self.status

    def animate(self, player_stats):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if player_stats.health <= 0:
                self.dead = True
                self.frame_index = -1
            elif self.pain:
                self.pain = False
                self.speed = 5

        image = animation[int(self.frame_index)]
        
        if self.facing_right:
            self.image = image
            self.rect.x, self.rect.y = self.hitbox.x-40, self.hitbox.y-36
        else:
            self.image = pygame.transform.flip(image, True, False)
            self.rect.x, self.rect.y = self.hitbox.x-32, self.hitbox.y-36

    def apply_gravity(self):
        if self.direction.y + self.gravity <= self.fall_speed_limit:
            self.direction.y += self.gravity
        self.hitbox.y += self.direction.y

    def check_collisions(self, tiles:pygame.sprite.Group, doors, screen, player_stats):
        # Adjustments
        if self.status == 'pain':
            if self.facing_right:
                self.direction.x = -1
            else:
                self.direction.x = 1
        elif self.status == 'd_jump' or self.status == 'd_fall' or\
            self.status == 's_jump' or self.status == 's_fall':
            self.rect.y += 14

        # Horizontal collision
        if self.direction.x != 0:
            self.hitbox.x += self.direction.x * self.speed

            # Tiles collision
            for tile in tiles.sprites():
                if self.hitbox.colliderect(tile.rect):
                    if self.direction.x < 0:
                        self.hitbox.left = tile.rect.right
                    elif self.direction.x > 0:
                        self.hitbox.right = tile.rect.left
                    break
            
            # Doors collisions
            for door in doors.sprites():
                if self.hitbox.colliderect(door.hitbox):
                    if self.direction.x < 0:
                        self.hitbox.left = door.hitbox.right
                    elif self.direction.x > 0:
                        self.hitbox.right = door.hitbox.left
            
            # Screen limits collision
            screen_width = screen.get_width()
            if self.hitbox.right > screen_width:
                self.hitbox.right = screen_width
            elif self.hitbox.left < 0:
                self.hitbox.left = 0

        # Vertical collision
        self.apply_gravity()

        # Tiles collision
        for tile in tiles.sprites():
            if self.hitbox.colliderect(tile.rect):
                if self.direction.y > 0:
                    self.hitbox.bottom = tile.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:
                    self.hitbox.top = tile.rect.bottom
                    self.direction.y = 0.1
                    self.on_ceiling = True
                break
        
        # Doors collisions
        for door in doors.sprites():
            if self.hitbox.colliderect(door.hitbox):
                if self.direction.y > 0:
                    self.hitbox.bottom = door.hitbox.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:
                    self.hitbox.top = door.hitbox.bottom
                    self.direction.y = 0.1
                    self.on_ceiling = True
        
        # Screen limits collision
        screen_height = screen.get_height()
        if self.rect.top > screen_height:
            player_stats.health = 0
            self.dead = True
        elif self.hitbox.top < 64:
            self.hitbox.top = 64
            self.direction.y = 0.1
            self.on_ceiling = True
        
        if self.on_ground and self.direction.y != 0:
            self.on_ground = False
        if self.on_ceiling and self.direction.y > 0:
            self.on_ceiling = False
    
    def update(self, current_time, tiles, doors, screen, player_stats):
        self.get_input()
        self.get_status(current_time, player_stats)
        self.animate(player_stats)
        self.check_collisions(tiles, doors, screen, player_stats)

class CharacterBill(pygame.sprite.Sprite):
    def __init__(self, pos, facing_right):
        super().__init__()

        # Animation
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['d_idle'][self.frame_index]

        # Hitbox
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = pygame.Rect(self.rect.x+56, self.rect.y+50, 12, 74)
        
        # Movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 5
        self.gravity = 0.8
        self.jump_speed = -14
        self.fall_speed_limit = 13

        # Status
        self.status = 'd_idle'
        self.prev_status = ''
        self.facing_right = facing_right
        self.on_ground = False
        self.on_ceiling = False
        self.shooting = False
        self.pain = False
        self.invulnerability_timer = 0
        self.invulnerable = False
        self.damage = 0.5
        self.crouch = False
        self.look_up = False
        self.fire_rate = 100
        self.dead = False
        self.climb = False

        # SFX
        self.sfx_pain = pygame.mixer.Sound("resources/sfx/characters/bill/hurt.wav")
        self.sfx_death = pygame.mixer.Sound("resources/sfx/characters/bill/death.wav")
        self.sfx_death_flag = True

    def import_character_assets(self):
        character_path =\
            "resources/graphics/characters/bill/"
        
        self.animations =\
        {
            'd_idle':[], 'd_walk':[], 'd_crouch':[], 'd_up':[],
            's_idle':[], 's_walk':[], 's_crouch':[], 's_up':[],
            'jump':[], 'climb_idle':[], 'climb':[], 'victory':[],
            'pain':[], 'death':[]
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path,
                                                    (122, 128))

    def get_input(self):
        if not self.pain and not self.dead and self.status != 'victory':
            keys = pygame.key.get_pressed()
            
            # Movement
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.facing_right = True
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.facing_right = False
            else:
                self.direction.x = 0

            # Extra
            if keys[pygame.K_DOWN] and self.direction.x == 0:
                if self.climb:
                    self.hitbox.y += 2
                self.crouch = True
            elif keys[pygame.K_UP] and self.direction.x == 0:
                if self.climb:
                    self.hitbox.y -= 2
                self.look_up = True
            else:
                self.crouch = False
                self.look_up = False
            
            # Jump
            if keys[pygame.K_z] and self.on_ground:
                self.direction.y = self.jump_speed
            
            # Shot
            if keys[pygame.K_x]:
                self.shooting = True
            else:
                self.shooting = False

    def get_status(self, current_time, player_stats):
        if self.shooting:
            prefix = 's_'
        else:
            prefix = 'd_'
        
        if player_stats.health <= 0:
            if self.sfx_death_flag:
                self.sfx_death.set_volume(volume.sfx_volume)
                self.sfx_death.play(0)
                self.sfx_death_flag = False
            self.status = 'death'
            self.shooting = False
            self.animation_speed = 0.04
            self.direction.x = 0
        elif self.pain:
            self.shooting = False
            self.status = 'pain'
            if self.prev_status != 'pain':
                player_stats.hits += 1
                player_stats.health -= 1
                self.sfx_pain.set_volume(volume.sfx_volume)
                self.sfx_pain.play(0)
            if self.facing_right:
                self.direction.x = -1
            else:
                self.direction.x = 1
            self.invulnerable = True
        elif self.climb:
            self.status = 'climb_idle'  
            if self.look_up or self.crouch:
                self.status = 'climb'  
        elif self.direction.y != 0:
            self.status = 'jump'
            self.hitbox.height = 40
        elif self.crouch:
            self.status = prefix + 'crouch'
        elif self.look_up:
            self.status = prefix + 'up'
        else:
            if self.direction.x != 0:
                self.status = prefix + 'walk'
            else:
                self.status = prefix + 'idle'
        
        if current_time - self.invulnerability_timer > 1200:
            self.invulnerable = False
        
        # Adjustments
        if (self.prev_status == 'jump' and self.status != 'jump') or\
            (self.prev_status == 'pain' and self.status != 'pain'):
                self.hitbox.height = 74
                if self.prev_status == 'jump':
                    self.hitbox.y -= 34
        
        if player_stats.end_level:
            self.status = 'victory'
            self.direction.x = 0
        
        if self.status != self.prev_status:
            self.prev_status = self.status
            self.frame_index = 0

    def animate(self, player_stats):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if player_stats.health <= 0:
                self.dead = True
                self.frame_index = -1
            elif self.pain:
                self.pain = False
                self.speed = 5

        image = animation[int(self.frame_index)]
        
        if self.facing_right:
            self.image = image
            self.rect.x, self.rect.y = self.hitbox.x-56, self.hitbox.y-50
        else:
            self.image = pygame.transform.flip(image, True, False)
            self.rect.x, self.rect.y = self.hitbox.x-54, self.hitbox.y-50

    def apply_gravity(self):
        if self.direction.y + self.gravity <= self.fall_speed_limit:
            self.direction.y += self.gravity
        self.hitbox.y += self.direction.y

    def check_collisions(self, tiles:pygame.sprite.Group, doors, screen, climb_limits, player_stats):
        # Horizontal collision
        if self.direction.x != 0:
            self.hitbox.x += self.direction.x * self.speed

            # Tiles collision
            for tile in tiles.sprites():
                if self.hitbox.colliderect(tile.rect):
                    if self.direction.x < 0:
                        self.hitbox.left = tile.rect.right
                    elif self.direction.x > 0:
                        self.hitbox.right = tile.rect.left
                    
                    if not self.on_ground and tile.climbable:
                        self.climb = True
                        self.direction.x = 0
                        self.direction.y = 0
                        self.animation_speed = 0.08
                    else:
                        self.climb = False
                        self.animation_speed = 0.15

            # Doors collisions
            for door in doors.sprites():
                if self.hitbox.colliderect(door.hitbox):
                    if self.direction.x < 0:
                        self.hitbox.left = door.hitbox.right
                    elif self.direction.x > 0:
                        self.hitbox.right = door.hitbox.left
            
            # Screen limits collision
            screen_width = screen.get_width()
            if self.hitbox.right > screen_width:
                self.hitbox.right = screen_width
            elif self.hitbox.left < 0:
                self.hitbox.left = 0

        # Climbing limits    
        if self.climb:
            for limit in climb_limits:
                if self.hitbox.colliderect(limit.rect):
                    self.climb = False
            if self.direction.x != 0:
                self.climb = False

        # Vertical collision
        if not self.climb:
            self.apply_gravity()

        # Tiles collision
        for tile in tiles.sprites():
            if self.hitbox.colliderect(tile.rect):
                if self.direction.y > 0:
                    self.hitbox.bottom = tile.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:
                    self.hitbox.top = tile.rect.bottom
                    self.direction.y = 0.1
                    self.on_ceiling = True
        
        # Doors collisions
        for door in doors.sprites():
            if self.hitbox.colliderect(door.hitbox):
                if self.direction.y > 0:
                    self.hitbox.bottom = door.hitbox.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0:
                    self.hitbox.top = door.hitbox.bottom
                    self.direction.y = 0.1
                    self.on_ceiling = True
        
        # Screen limits collision
        screen_height = screen.get_height()
        if self.rect.top > screen_height:
            player_stats.health = 0
            self.dead = True
        elif self.hitbox.top < 64:
            self.hitbox.top = 64
            self.direction.y = 0.1
            self.on_ceiling = True
        
        if self.on_ground and self.direction.y != 0:
            self.on_ground = False
        if self.on_ceiling and self.direction.y > 0:
            self.on_ceiling = False

    def update(self, current_time, tiles, doors, screen, climb_limits, player_stats):
        self.get_input()
        self.get_status(current_time, player_stats)
        self.animate(player_stats)
        self.check_collisions(tiles, doors, screen, climb_limits, player_stats)