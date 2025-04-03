import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class BattleScene:
    def __init__(self):
        # Background image display
        self.bg_image = pygame.image.load("assets/backgrounds/moon.jpg").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Battle settings
        self.battle_over = False
        self.ready_to_exit = False
        self.fade_delay = 60
        self.battle_stage = None  
        self.game_over_screen = False
        
        # Battle UI
        self.font = pygame.font.SysFont("arial", 20)
        self.bg_color = (0, 0, 0)
        self.enemy_hp = 100
        self.player_hp = 100
        self.message = "A wild Slime appears!"

        # Player turn
        self.turn = "player"
        self.enemy_attack_delay = 60
        self.game_over = False

        # Load enemy sprite
        full_sheet = pygame.image.load("assets/enemies/slime.png").convert_alpha()
        sprite_width = 48.5
        sprite_height = 46.4

        # Selected enemy sprite
        col = 0
        row = 0
        sprite_rect = pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height)
        self.enemy_sprite = full_sheet.subsurface(sprite_rect)

        # Scale enemy sprite
        self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (sprite_width * 2, sprite_height * 2))

        # Load player sprite 
        self.player_sprite = pygame.image.load("assets/sprites/ai_generated_player.png").convert_alpha()

        # Scale player sprite
        scale_factor = 8
        width = self.player_sprite.get_width() / scale_factor
        height = self.player_sprite.get_height() / scale_factor
        self.player_sprite = pygame.transform.scale(self.player_sprite, (width, height))

        # Battle command menu
        self.menu_options = ["Attack", "Magic", "Item", "Run"]
        self.selected_option = 0
        self.input_cooldown = 0  # Prevent rapid scroll

        # Fade effect
        self.fade_alpha = 0
        self.fading = False
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_surface.fill((0, 0, 0))

    # Health bar UI
    def draw_hp_bar(self, surface, x, y, width, height, current, maximum, label, bar_color=(0, 200, 0)):
        # Border
        pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)

        # Full bar
        ratio = max(current / maximum, 0)
        fill_width = int((width - 4) * ratio) # Subract border
        pygame.draw.rect(surface, bar_color, (x + 2, y + 2, fill_width, height - 4))

        # Label and HP text
        hp_text = self.font.render(f"{label} HP: {current}/{maximum}", True, (255, 255, 255))
        surface.blit(hp_text, (x, y - 27))

    def update(self):
        keys = pygame.key.get_pressed()

        # Prevent scrolling too fast
        if self.input_cooldown > 0:
            self.input_cooldown -= 1

        # Input handling only allowed if not battle_over
        if not self.battle_over and self.turn == "player":
            if keys[pygame.K_UP] and self.input_cooldown == 0:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                self.input_cooldown = 10

            elif keys[pygame.K_DOWN] and self.input_cooldown == 0:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                self.input_cooldown = 10

            elif (keys[pygame.K_RETURN] or keys[pygame.K_z]) and self.input_cooldown == 0:
                selected = self.menu_options[self.selected_option]
                if selected == "Attack":
                    damage = 10
                    self.enemy_hp -= damage
                    self.message = f"You hit the enemy for {damage} damage!"
                    if self.enemy_hp <= 0:
                        self.battle_over = True
                        self.battle_stage = None  # Start post-battle sequence
                        self.input_cooldown = 30
                    else:
                        self.turn = "enemy"
                        self.enemy_attack_delay = 60
                else:
                    self.message = f"You selected {selected}."
                    self.turn = "enemy"
                    self.enemy_attack_delay = 60
                    self.input_cooldown = 15

        elif self.turn == "enemy" and not self.battle_over:
            if self.enemy_attack_delay > 0:
                self.enemy_attack_delay -= 1

            else:
                damage = random.randint(5, 10)
                self.player_hp -= damage
                self.message = f"The enemy attacks you for {damage} damage!"
                self.turn = "player"
                self.input_cooldown = 30

                if self.player_hp <= 0:
                    self.player_hp = 0
                    self.message = "You were defeated..."
                    self.game_over_screen = True
                    self.input_cooldown = 30

        # If enemy defeated, step through staged messages and fade
        elif self.battle_over and not self.fading:
            if self.battle_stage is None:
                self.battle_stage = "defeated"
                self.message = "Enemy defeated!"
                self.fade_delay = 70

            elif self.battle_stage == "defeated":
                if self.fade_delay > 0:
                    self.fade_delay -= 1
                else:
                    self.battle_stage = "victory"
                    self.message = "Victory!"
                    self.fade_delay = 40

            elif self.battle_stage == "victory":
                if self.fade_delay > 0:
                    self.fade_delay -= 1
                else:
                    self.battle_stage = "fade"
                    self.fading = True

        # Fade effect
        if self.fading:
            self.fade_alpha += 5
            if self.fade_alpha >= 255:
                self.ready_to_exit = True

        # Game over
        if self.game_over_screen and self.input_cooldown <= 0:
            if keys[pygame.K_RETURN] or keys[pygame.K_z]:
                self.ready_to_exit = True

    def draw(self, surface):
        # Draw game over screen 
        if self.game_over_screen:
            surface.fill((0, 0, 0))
            game_over_text = self.font.render("You were defeated...", True, (200, 50, 50))
            tip_text = self.font.render("Press Z or Enter to continue", True, (200, 200, 200))

            surface.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
            surface.blit(tip_text, tip_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))
            return
        
        # Background color
        '''surface.fill(self.bg_color)'''
        surface.blit(self.bg_image, (0, 0))

        # Draw enemy sprite
        sprite_rect = self.enemy_sprite.get_rect(center=(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 80))
        surface.blit(self.enemy_sprite, sprite_rect.topleft)

        # Better HP bars (only if not fading out)
        if not self.fading:
            self.draw_hp_bar(surface, x=50, y=40, width=200, height=20,
                            current=self.enemy_hp, maximum=100, label="Slime", bar_color=(200, 0, 0))

            self.draw_hp_bar(surface, x=50, y=95, width=200, height=20,
                            current=self.player_hp, maximum=100, label="Player", bar_color=(0, 200, 0))

        # Draw player sprite (bottom left)
        player_rect = self.player_sprite.get_rect()
        player_rect.midbottom = (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120)
        surface.blit(self.player_sprite, player_rect.topleft)

        # Draw message if not fading
        if not self.fading:
            text = self.font.render(self.message, True, (255, 255, 255))
            surface.blit(text, (50, SCREEN_HEIGHT - 80))

            # Draw battle command menu
            menu_x = SCREEN_WIDTH - 200
            menu_y = SCREEN_HEIGHT - 150
            menu_width = 150
            menu_height = 120

            pygame.draw.rect(surface, (0, 0, 0), (menu_x, menu_y, menu_width, menu_height))
            pygame.draw.rect(surface, (255, 255, 255), (menu_x, menu_y, menu_width, menu_height), 2)

            for index, option in enumerate(self.menu_options):
                color = (255, 255, 0) if index == self.selected_option else (255, 255, 255)
                text = self.font.render(option, True, color)
                surface.blit(text, (menu_x + 10, menu_y + 10 + index * 25))

        # Fade overlay
        if self.fading:
            self.fade_surface.set_alpha(self.fade_alpha)
            surface.blit(self.fade_surface, (0, 0))
