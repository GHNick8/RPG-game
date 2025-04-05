import pygame
from settings import FONT_NAME, FONT_SIZE, BORDER_COLOR, BG_COLOR, SHOP_BOX_POS, SHOP_BOX_SIZE, SHOP_MSG_BOX_POS, SHOP_MSG_BOX_SIZE, YES_HIGHLIGHT, DEFAULT_TEXT_COLOR

class ShopMenu:
    def __init__(self, player, inventory):
        self.player = player
        self.inventory = inventory
        self.active = False
        self.selection = 0
        self.message = None
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    def open(self):
        self.active = True
        self.selection = 0
        self.message = None

    def handle_event(self, event):
        if self.message:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_z):
                self.message = None
            return

        if not self.active:
            return

        # Shop interaction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selection = (self.selection - 1) % 2
            elif event.key == pygame.K_DOWN:
                self.selection = (self.selection + 1) % 2
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if self.selection == 0:
                    self.message = self.inventory.buy_item("Potion")
                else:
                    self.message = "Maybe next time!"
                self.active = False

    def draw(self, surface):
        if self.active:
            box = pygame.Rect(*SHOP_BOX_POS, *SHOP_BOX_SIZE)
            pygame.draw.rect(surface, BG_COLOR, box)
            pygame.draw.rect(surface, BORDER_COLOR, box, 2)

            question = self.font.render("Buy a potion for 10 gold?", True, (255, 255, 255))
            surface.blit(question, (box.x + 30, box.y + 20))

            options = ["Yes", "No"]
            for i, option in enumerate(options):
                color = YES_HIGHLIGHT if i == self.selection else DEFAULT_TEXT_COLOR
                prefix = "" if i == self.selection else "   "
                text = self.font.render(prefix + option, True, color)
                surface.blit(text, (box.x + 50, box.y + 60 + i * 30))

        elif self.message:
            msg_box = pygame.Rect(*SHOP_MSG_BOX_POS, *SHOP_MSG_BOX_SIZE)
            pygame.draw.rect(surface, BG_COLOR, msg_box)
            pygame.draw.rect(surface, BORDER_COLOR, msg_box, 2)
            text = pygame.font.SysFont(FONT_NAME, 20).render(self.message, True, (255, 255, 255))
            surface.blit(text, (msg_box.x + 20, msg_box.y + 10))
            prompt = pygame.font.SysFont(FONT_NAME, 14).render("Press Z to continue", True, (180, 180, 180))
            surface.blit(prompt, (msg_box.x + 20, msg_box.y + 35))

    def is_active(self):
        return self.active or self.message is not None