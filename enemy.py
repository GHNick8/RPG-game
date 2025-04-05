import pygame
import random

class Enemy:
    def __init__(self, name, sprite_sheet_path, sprite_coords, max_hp, attack, xp_reward, gold_reward):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward

        # Load and slice sprite
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        # TODO 
        if sprite_coords:
            self.sprite = self.load_sprite(sprite_coords)
        else:
            self.sprite = pygame.transform.scale(self.sprite_sheet, (96 * 3, 96 * 3))

    def load_sprite(self, coords):
        col, row, width, height = coords
        rect = pygame.Rect(col * width, row * height, width, height)
        return pygame.transform.scale(self.sprite_sheet.subsurface(rect), (width * 2, height * 2))

    def deal_damage(self):
        return random.randint(self.attack - 2, self.attack + 2)

    def is_defeated(self):
        return self.hp <= 0

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
