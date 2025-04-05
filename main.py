# Pygame
import pygame

# Imports
from settings import *
from map import Map
from player import Player
from inventory import Inventory
from shop_keeper import Shopkeeper
from ui.save_menu import SaveMenu
from ui.player_menu import PlayerMenu
from scene_manager import SceneManager
from scenes.title import TitleScene
from scenes.overworld import OverworldScene
from scenes.village import VillageScene

# Initialize pygame & Screen setup
pygame.init()
scene_manager = SceneManager()
scene_manager.add("title", TitleScene(scene_manager))
scene_manager.set("title")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tribute")
clock = pygame.time.Clock()

# Game artifacts 
game_map = Map("data/world_map.csv")
player = Player(5, 5) 
inventory = Inventory()
shopkeeper = Shopkeeper(x=5, y=2, image_path="assets/npc's/dudeWutIsScratch.png")
dialogue_message = None
dialogue_timer = 0  
save_menu = SaveMenu(player)
player_menu = PlayerMenu(player, inventory)
in_battle = False
battle = None 
scene_manager.add("overworld", OverworldScene(player, game_map, shopkeeper, inventory, scene_manager))
#scene_manager.add("village", VillageScene(player, scene_manager))
#scene_manager.set("village")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        scene_manager.handle_event(event)

    scene_manager.update()
    scene_manager.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()