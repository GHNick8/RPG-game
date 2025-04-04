import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from enemy import Enemy

class BattleScene:
    def __init__(self, player):
        # Battle settings
        self.font = pygame.font.SysFont("arial", 20)
        self.ready_to_exit = False
        self.battle_over = False
        self.fading = False
        self.fade_alpha = 0
        self.fade_delay = 60
        self.input_cooldown = 0
        self.turn = "player"
        self.enemy_attack_delay = 60
        self.game_over_screen = False

        # Load player & enemy
        self.player = player
        self.enemy = Enemy(
            name="Slime",
            sprite_sheet_path="assets/enemies/slime.png",
            sprite_coords=(0, 0, 48, 48),
            max_hp=90,
            attack=10,
            xp_reward=30,
            gold_reward=10
        )

        # Battle UI
        self.menu_options = ["Attack", "Magic", "Item", "Run"]
        self.selected_option = 0
        self.message = f"A wild {self.enemy.name} appears!"

        # Sprites
        self.player_sprite = pygame.image.load("assets/sprites/ai_generated_player.png").convert_alpha()
        self.player_sprite = pygame.transform.scale(
            self.player_sprite, (self.player_sprite.get_width() / 6, self.player_sprite.get_height() / 6)
        )

        self.bg_image = pygame.image.load("assets/backgrounds/moon.jpg").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def handle_event(self, event):
        if self.game_over_screen:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_z):
                self.ready_to_exit = True
            return

        if not self.battle_over and self.turn == "player":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key in (pygame.K_RETURN, pygame.K_z):
                    selected = self.menu_options[self.selected_option]
                    if selected == "Attack":
                        damage = self.player.attack
                        self.enemy.take_damage(damage)
                        self.message = f"You hit the {self.enemy.name} for {damage} damage!"
                        if self.enemy.is_defeated():
                            self.handle_victory()
                        else:
                            self.turn = "enemy"
                            self.enemy_attack_delay = 60
                    else:
                        self.message = f"You selected {selected}."
                        self.turn = "enemy"
                        self.enemy_attack_delay = 60

    def update(self):
        if self.turn == "enemy" and not self.battle_over:
            if self.enemy_attack_delay > 0:
                self.enemy_attack_delay -= 1
            else:
                damage = self.enemy.deal_damage()
                self.player.hp -= damage
                self.message = f"The {self.enemy.name} attacks you for {damage} damage!"
                self.turn = "player"

                if self.player.hp <= 0:
                    self.player.hp = 0
                    self.message = "You were defeated..."
                    self.game_over_screen = True

        if self.battle_over and not self.game_over_screen:
            if self.fade_delay > 0:
                self.fade_delay -= 1
            else:
                self.ready_to_exit = True

    def handle_victory(self):
        self.message = f"You gained {self.enemy.xp_reward} XP and {self.enemy.gold_reward} gold!"
        self.player.xp += self.enemy.xp_reward
        self.player.check_level_up()
        self.battle_over = True
        self.fade_delay = 120

    def draw_hp_bar(self, surface, x, y, width, height, current, maximum, label, bar_color):
        pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)
        ratio = max(current / maximum, 0)
        fill_width = int((width - 4) * ratio)
        pygame.draw.rect(surface, bar_color, (x + 2, y + 2, fill_width, height - 4))
        text_margin = 8
        text_y = y - self.font.get_height() - text_margin
        hp_text = self.font.render(f"{label} HP: {current}/{maximum}", True, (255, 255, 255))
        surface.blit(hp_text, (x, text_y))

    def draw(self, surface):
        if self.game_over_screen:
            surface.fill((0, 0, 0))
            game_over_text = self.font.render("You were defeated...", True, (200, 50, 50))
            tip_text = self.font.render("Press Z or Enter to continue", True, (200, 200, 200))
            surface.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
            surface.blit(tip_text, tip_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))
            return

        surface.blit(self.bg_image, (0, 0))

        sprite_rect = self.enemy.sprite.get_rect(center=(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 80))
        surface.blit(self.enemy.sprite, sprite_rect.topleft)

        player_rect = self.player_sprite.get_rect()
        player_rect.midbottom = (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120)
        surface.blit(self.player_sprite, player_rect.topleft)

        if not self.fading:
            self.draw_hp_bar(surface, x=50, y=40, width=200, height=20,
                             current=self.enemy.hp, maximum=self.enemy.max_hp, label=self.enemy.name, bar_color=(200, 0, 0))
            self.draw_hp_bar(surface, x=50, y=100, width=200, height=20,
                             current=self.player.hp, maximum=self.player.max_hp, label="Player", bar_color=(0, 200, 0))

            level_text = self.font.render(f"Lv {self.player.level} | XP: {self.player.xp}/{self.player.xp_to_next_level}", True, (255, 255, 255))
            surface.blit(level_text, (50, 140))

        text = self.font.render(self.message, True, (255, 255, 255))
        surface.blit(text, (50, SCREEN_HEIGHT - 80))

        if not self.battle_over and not self.game_over_screen:
            menu_x = SCREEN_WIDTH - 200
            menu_y = SCREEN_HEIGHT - 150
            menu_width = 150
            menu_height = 120

            pygame.draw.rect(surface, (0, 0, 0), (menu_x, menu_y, menu_width, menu_height))
            pygame.draw.rect(surface, (255, 255, 255), (menu_x, menu_y, menu_width, menu_height), 2)

            for index, option in enumerate(self.menu_options):
                color = (255, 255, 0) if index == self.selected_option else (255, 255, 255)
                option_text = self.font.render(option, True, color)
                surface.blit(option_text, (menu_x + 10, menu_y + 10 + index * 25))

    def is_over(self):
        return self.ready_to_exit
