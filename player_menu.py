import pygame

class PlayerMenu:
    def __init__(self, player, inventory):
        self.player = player
        self.inventory = inventory
        self.font = pygame.font.SysFont("arial", 18)
        self.rect = pygame.Rect(200, 150, 400, 200)
        self.active = False

    def draw(self, surface):
        if not self.active:
            return

        pygame.draw.rect(surface, (0, 0, 0), self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)

        potions = self.inventory.items.get('Potion', 0)
        gold = self.inventory.gold

        surface.blit(self.font.render(f"Potions: {potions}", True, (255, 255, 255)), (self.rect.x + 20, self.rect.y + 30))
        surface.blit(self.font.render(f"Gold: {gold}", True, (255, 215, 0)), (self.rect.x + 20, self.rect.y + 60))

        prompt = self.font.render("Press Z or P to close", True, (180, 180, 180))
        surface.blit(prompt, (self.rect.x + 20, self.rect.y + 140))

