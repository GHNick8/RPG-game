import pygame
import csv
from settings import TILE_SIZE

class Map:
    def __init__(self, filename):
        self.tileset = pygame.image.load("assets/tiles/magecity.png").convert_alpha()
        self.tiles = self.load_tiles()
        self.tile_map = []

        # Solid tile indexes
        self.solid_tiles = {4, 5, 6, 15, 20, 25, 33}

        with open(filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                self.tile_map.append([int(tile) for tile in row])

    def is_blocked(self, x, y):
        if 0 <= y < len(self.tile_map) and 0 <= x < len(self.tile_map[0]):
            tile_index = self.tile_map[int(y)][int(x)]
            return tile_index in self.solid_tiles
        return True 

    def load_tiles(self):
        tiles = []
        tileset_width = self.tileset.get_width()
        tileset_height = self.tileset.get_height()

        cols = tileset_width // TILE_SIZE
        rows = tileset_height // TILE_SIZE

        for y in range(rows):
            for x in range(cols):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                image = self.tileset.subsurface(rect)
                tiles.append(image)
        return tiles

    def draw(self, surface):
        for y, row in enumerate(self.tile_map):
            for x, tile in enumerate(row):
                if 0 <= tile < len(self.tiles):
                    surface.blit(self.tiles[tile], (x * TILE_SIZE, y * TILE_SIZE)) 