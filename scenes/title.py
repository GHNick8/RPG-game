import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_NAME, FONT_SIZE, BG_COLOR

class TitleScene:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE + 10)
        self.small_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE - 4)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_z, pygame.K_RETURN):
            self.manager.set("overworld")

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BG_COLOR)

        title = self.font.render("Tribute Demo", True, (255, 255, 255))
        prompt = self.small_font.render("Press Z to Start", True, (200, 200, 200))

        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))

        screen.blit(title, title_rect)
        screen.blit(prompt, prompt_rect)
