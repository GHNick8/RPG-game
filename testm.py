import pygame
from player import Player
from map import GameMap
from shop_keeper import Shopkeeper
from inventory import Inventory
from save_menu import SaveMenu
from shop_menu import ShopMenu
from scene_manager import SceneManager

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
FPS = 60

# Core game objects
player = Player(x=5, y=5)
inventory = Inventory()
game_map = GameMap()
shopkeeper = Shopkeeper(x=10, y=7, image_path="assets/npcs/dudeWutIsScratch.png")
save_menu = SaveMenu(player)
shop_menu = ShopMenu(player, inventory)
scene_manager = SceneManager()

# === Overworld Scene ===
class OverworldScene:
    def __init__(self, player, game_map, shopkeeper, inventory):
        self.player = player
        self.map = game_map
        self.shopkeeper = shopkeeper
        self.inventory = inventory

    def handle_event(self, event):
        if not shop_menu.active and not save_menu.active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.player.rect.colliderect(self.shopkeeper.rect):
                    shop_menu.open()

        if not shop_menu.active and not save_menu.active:
            self.player.handle_input(self.map)

    def update(self):
        pass

    def draw(self, screen):
        self.map.draw(screen)
        self.player.draw(screen)
        self.shopkeeper.draw(screen)

        # HUD: Inventory
        font = pygame.font.SysFont("arial", 20)
        hud = font.render(f"Potions: {self.inventory.items.get('Potion', 0)} | Gold: {self.inventory.gold}", True, (255, 255, 255))
        screen.blit(hud, (10, 10))

# Register scene
overworld = OverworldScene(player, game_map, shopkeeper, inventory)
scene_manager.add("overworld", overworld)
scene_manager.set("overworld")

# === Game Loop ===
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Toggle save menu
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            save_menu.toggle()

        # Priority order: menus > scene
        if save_menu.active:
            save_menu.handle_event(event)
        elif shop_menu.active:
            shop_menu.handle_event(event)
        else:
            scene_manager.handle_event(event)

    # Update and draw everything
    scene_manager.update()
    scene_manager.draw(screen)

    if shop_menu.active:
        shop_menu.update()
        shop_menu.draw(screen)

    if save_menu.active:
        save_menu.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
