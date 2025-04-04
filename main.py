# Pygame
import pygame

# Imports
from settings import *
from map import Map
from player import Player
from battle import *
from inventory import Inventory
from shop_keeper import Shopkeeper
from save_menu import SaveMenu
from hud import PLayerMenu

# Initialize pygame & Screen setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tribute")
clock = pygame.time.Clock()

# Game artifacts 
game_map = Map("data/world_map.csv")
player = Player(5, 5) 
inventory = Inventory()
shopkeeper = Shopkeeper(x=5, y=2, image_path="assets/npc's/dudeWutIsScratch.png")
shop_mode = False
shop_selection = 0
shop_message = None
shop_message_timer = 0
dialogue_message = None
dialogue_timer = 0  
save_menu = SaveMenu(player)

# Player menu
player_menu = PLayerMenu(player, inventory)

# Battle
in_battle = False
battle = None 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Toggle save menu
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            save_menu.toggle()

        # Pass event to save menu if it's open
        if save_menu.active:
            result = save_menu.handle_event(event)
            if result == "saved":
                print("Game saved!")
            elif result == "loaded":
                print("Game loaded!")
            continue 

        # Shop input 
        if not in_battle and (shop_mode or shop_message):
            if event.type == pygame.KEYDOWN:
                if shop_message:  # Message is showing, wait for confirmation
                    if event.key in (pygame.K_RETURN, pygame.K_z):
                        shop_message = None  # Player dismissed the message
                elif shop_mode:  # Menu is open, allow navigation
                    if event.key == pygame.K_UP:
                        shop_selection = (shop_selection - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        shop_selection = (shop_selection + 1) % 2
                    elif event.key in (pygame.K_RETURN, pygame.K_z):
                        if shop_selection == 0:
                            shop_message = inventory.buy_item("Potion")
                        else:
                            shop_message = "Maybe next time!"
                        shop_mode = False
            continue

        # Interact with shopkeeper
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if player.rect.colliderect(shopkeeper.rect):
                shop_mode = True
                shop_selection = 0

        # Inventory test keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                print(inventory.use_item("Potion", player))
            elif event.key == pygame.K_o:
                print(inventory.buy_item("Potion"))
            elif event.key == pygame.K_g:
                inventory.gold += 50
                print("Added 50 gold!")

        # Battle input
        if in_battle and battle:
            battle.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_b and not in_battle:
            in_battle = True
            battle = BattleScene(player)

        # Player menu 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player_menu.active = not player_menu.active
            elif player_menu.active and event.key in (pygame.K_z, pygame.K_RETURN):
                player_menu.active = False

    # Update + Draw
    screen.fill((0, 0, 0))

    if in_battle and battle:
        battle.update()
        battle.draw(screen)

        if battle.ready_to_exit:
            in_battle = False
            battle = None

    else:
        if not shop_mode and not save_menu.active and not player_menu.active:
            encounter = player.handle_input(game_map)
            if encounter == "encounter":
                in_battle = True
                battle = BattleScene(player)

        game_map.draw(screen)
        player.draw(screen)
        shopkeeper.draw(screen)
        player_menu.draw(screen)

        # Shop dialog box
        if shop_mode:
            box = pygame.Rect(100, 420, 600, 140)
            pygame.draw.rect(screen, (0, 0, 0), box)
            pygame.draw.rect(screen, (255, 255, 255), box, 2)

            font = pygame.font.SysFont("arial", 22)
            question = font.render("Buy a potion for 10 gold?", True, (255, 255, 255))
            screen.blit(question, (box.x + 30, box.y + 20))

            yes_color = (255, 255, 0) if shop_selection == 0 else (255, 255, 255)
            no_color = (255, 255, 0) if shop_selection == 1 else (255, 255, 255)

            yes_text = font.render("Yes" if shop_selection == 0 else "   Yes", True, yes_color)
            no_text = font.render("No" if shop_selection == 1 else "   No", True, no_color)

            screen.blit(yes_text, (box.x + 50, box.y + 60))
            screen.blit(no_text, (box.x + 50, box.y + 90))

        if shop_message:
            msg_box = pygame.Rect(250, 500, 300, 60)
            pygame.draw.rect(screen, (0, 0, 0), msg_box)
            pygame.draw.rect(screen, (255, 255, 255), msg_box, 2)
            msg = pygame.font.SysFont("arial", 20).render(shop_message, True, (255, 255, 255))
            screen.blit(msg, (msg_box.x + 20, msg_box.y + 20))

        # Save menu
        if save_menu.active:
            save_menu.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()