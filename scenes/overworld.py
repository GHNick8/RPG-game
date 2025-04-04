import pygame
from settings import *
from shop_menu import ShopMenu
from save_menu import SaveMenu
from player_menu import PlayerMenu
from battle import BattleScene

class OverworldScene:
    def __init__(self, player, game_map, shopkeeper, inventory, scene_manager):
        self.player = player
        self.map = game_map
        self.shopkeeper = shopkeeper
        self.inventory = inventory
        self.scene_manager = scene_manager

        self.shop_menu = ShopMenu(player, inventory)
        self.save_menu = SaveMenu(player)
        self.player_menu = PlayerMenu(player, inventory)
        self.battle = None
        self.in_battle = False

    def handle_event(self, event):
        if self.in_battle and self.battle:
            self.battle.handle_event(event)
            return

        # Save menu
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.save_menu.toggle()

        if self.save_menu.active:
            self.save_menu.handle_event(event)
            return

        # Shop input
        if self.shop_menu.is_active():
            self.shop_menu.handle_event(event)
            return

        # Interact with shopkeeper
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self.player.rect.colliderect(self.shopkeeper.rect):
                self.shop_menu.open()

        # Debug / Inventory test keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                print(self.inventory.use_item("Potion", self.player))
            elif event.key == pygame.K_o:
                print(self.inventory.buy_item("Potion"))
            elif event.key == pygame.K_g:
                self.inventory.gold += 50
                print("Added 50 gold!")

        # Toggle player menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.player_menu.active = not self.player_menu.active
            elif self.player_menu.active and event.key in (pygame.K_z, pygame.K_RETURN):
                self.player_menu.active = False

        # Force start battle
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b and not self.in_battle:
            self.in_battle = True
            self.battle = BattleScene(self.player)

    def update(self):
        if self.in_battle and self.battle:
            self.battle.update()
            if self.battle.is_over():
                self.in_battle = False
                self.battle = None
        else:
            if not self.shop_menu.is_active() and not self.save_menu.active and not self.player_menu.active:
                encounter = self.player.handle_input(self.map)
                if encounter == "encounter":
                    self.in_battle = True
                    self.battle = BattleScene(self.player)

    def draw(self, screen):
        if self.in_battle and self.battle:
            self.battle.draw(screen)
        else:
            self.map.draw(screen)
            self.player.draw(screen)
            self.shopkeeper.draw(screen)

            if self.shop_menu.is_active():
                self.shop_menu.draw(screen)

            if self.save_menu.active:
                self.save_menu.draw(screen)

            if self.player_menu.active:
                self.player_menu.draw(screen)

            font = pygame.font.SysFont(FONT_NAME, 20)
            hud = font.render(f"Potions: {self.inventory.items.get('Potion', 0)} | Gold: {self.inventory.gold}", True, (255, 255, 255))
            screen.blit(hud, (10, 10))
