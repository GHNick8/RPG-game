# Pygame
import pygame

# Imports
from settings import *
from map import Map
from player import Player
from battle import *

# Initialize pygame & Screen setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("New Game")
clock = pygame.time.Clock()

# Game map & Player
game_map = Map("data/world_map.csv")
player = Player(5, 5) # Start position (tile based)

# Battle
in_battle = False
battle = None 

# Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            in_battle = True
            battle = BattleScene()

    if in_battle:
        battle.update()
        battle.draw(screen)

        if battle.ready_to_exit:
            in_battle = False
            battle = None

    else:
        encounter = player.handle_input(game_map)
        if encounter == "encounter":
            in_battle = True
            battle = BattleScene()

        screen.fill((0, 0, 0))
        game_map.draw(screen)
        player.draw(screen)        

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()