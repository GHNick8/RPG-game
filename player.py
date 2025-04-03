import pygame
import random
from settings import TILE_SIZE

class Player:
    def __init__(self, x, y):
        self.full_sheet = pygame.image.load("assets/sprites/rpgsprites1/warrior_m.png").convert_alpha()

        self.frame_width = 32
        self.frame_height = 36

        self.char_col = 0
        self.char_row = 0  

        self.direction = "down"
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.15  

        self.load_frames()
        self.image = self.frames[self.direction][1]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (int(self.x * TILE_SIZE), int(self.y * TILE_SIZE))

        self.steps_since_last_encounter = 0

    def load_frames(self):
        self.frames = {"down": [], "left": [], "right": [], "up": []}
        directions = ["down", "left", "right", "up"]

        for dir_index, direction in enumerate(directions):
            for frame in range(3):
                frame_x = frame * self.frame_width
                frame_y = dir_index * self.frame_height

                sprite = self.full_sheet.subsurface(
                    (frame_x, frame_y, self.frame_width, self.frame_height)
                )
                self.frames[direction].append(sprite)

    def handle_input(self, game_map):
        keys = pygame.key.get_pressed()
        moved = False

        new_x, new_y = self.x, self.y

        speed = 0.08

        if keys[pygame.K_UP]:
            self.direction = "down"
            new_y -= speed
            #self.y -= 0.1
            moved = True
        elif keys[pygame.K_DOWN]:
            self.direction = "right"
            new_y += speed
            #self.y += 0.1
            moved = True
        elif keys[pygame.K_LEFT]:
            self.direction = "up"
            new_x -= speed
            #self.x -= 0.1
            moved = True
        elif keys[pygame.K_RIGHT]:
            self.direction = "left"
            new_x += speed
            #self.x += 0.1
            moved = True

        # Predict future position rectangle
        future_rect = self.rect.copy()
        future_rect.topleft = (int(new_x * TILE_SIZE), int(new_y * TILE_SIZE))

        # Get the tile under the feet (center of bottom of sprite)
        tile_x = future_rect.centerx // TILE_SIZE
        tile_y = future_rect.centery // TILE_SIZE

        if not game_map.is_blocked(tile_x, tile_y):
            self.x = new_x
            self.y = new_y
            self.rect.topleft = (int(self.x * TILE_SIZE), int(self.y * TILE_SIZE))

            if moved:
                self.steps_since_last_encounter += 1

                if self.steps_since_last_encounter >= 10:  # Optional step cooldown
                    if random.randint(1, 100) <= 8:  # 8% chance
                        self.steps_since_last_encounter = 0
                        return "encounter"

                self.animate()
        else:
            self.frame_index = 1
            self.image = self.frames[self.direction][self.frame_index]

        return None 
            
    def animate(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % 3
            self.image = self.frames[self.direction][self.frame_index]

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        #surface.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE)) 