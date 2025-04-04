import pygame
from settings import TILE_SIZE

class Shopkeeper:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.frame_width = 32
        self.frame_height = 32
        self.image = pygame.image.load(image_path).convert_alpha()
        self.sprite = self.extract_sprite(1, 2)
        self.sprite = pygame.transform.scale(self.sprite, (self.frame_width * 1.5, self.frame_height * 1.5))
        self.rect = pygame.Rect(self.x * 32, self.y * 32, self.frame_width * 2, self.frame_height * 2)

    def extract_sprite(self, col, row):
        rect = pygame.Rect(col * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height)
        return self.image.subsurface(rect)
    
    def draw(self, surface):
        surface.blit(self.sprite, (self.x * 32, self.y * 32))