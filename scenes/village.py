import pygame
import csv

from settings import *
from map import Map
# TODO

class VillageScene:
    def __init__(self, player, scene_manager):
        self.player = player
        self.scene_manager = scene_manager
        # TODO
        self.map = Map()

        # Player setup when entering the village
        self.player.rect.topleft = (5 * TILE_SIZE, 10 * TILE_SIZE)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self.at_exit_tile():
                self.scene_manager.set("overworld")

    def update(self):
        self.player.handle_input(self.map)

    def draw(self, screen):
        self.map.draw(screen)
        self.player.draw(screen)

    def at_exit_tile(self):
        tile_x = self.player.rect.centerx // TILE_SIZE
        tile_y = self.player.rect.centery // TILE_SIZE
        # Settings village exit
        return tile_x == 5 and tile_y == 1