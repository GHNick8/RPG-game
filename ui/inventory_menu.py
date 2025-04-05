import pygame
from settings import FONT_NAME, FONT_SIZE, BG_COLOR, BORDER_COLOR

class InventoryMenu:
    def __init__(self, inventory):
        self.inventory = inventory
        self.active = False
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.selection = 0
        self.message = None

    def toggle(self):
        if self.active or self.message:
            self.active = False
            self.message = None
        else:
            self.active = True
            self.selection = 0
            self.message = None

    def handle_event(self, event, player):
        if not self.active:
            return

        if self.message:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_z, pygame.K_RETURN):
                self.message = None
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selection = (self.selection - 1) % len(self.inventory.items)
            elif event.key == pygame.K_DOWN:
                self.selection = (self.selection + 1) % len(self.inventory.items)
            elif event.key in (pygame.K_z, pygame.K_RETURN):
                item_name = list(self.inventory.items.keys())[self.selection]
                self.message = self.inventory.use_item(item_name, player)

    def draw(self, screen):
        if not self.active:
            return

        box = pygame.Rect(100, 120, 600, 360)
        pygame.draw.rect(screen, BG_COLOR, box)
        pygame.draw.rect(screen, BORDER_COLOR, box, 2)

        title = self.font.render("Inventory", True, (255, 255, 255))
        screen.blit(title, (box.x + 20, box.y + 20))

        if self.message:
            msg = self.font.render(self.message, True, (255, 255, 0))
            screen.blit(msg, (box.x + 20, box.y + 300))
            prompt = self.font.render("Press Z to continue", True, (200, 200, 200))
            screen.blit(prompt, (box.x + 20, box.y + 330))
            return

        for i, (item, amount) in enumerate(self.inventory.items.items()):
            prefix = "" if i == self.selection else "   "
            text = self.font.render(f"{prefix}{item} x{amount}", True, (255, 255, 255))
            screen.blit(text, (box.x + 40, box.y + 60 + i * 30))

    def is_active(self):
        return self.active or self.message is not None
