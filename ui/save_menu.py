import pygame

class SaveMenu:
    def __init__(self, player):
        self.font = pygame.font.SysFont("arial", 24)
        self.player = player
        self.options = ["Save Game", "Load Game", "Return"]
        self.selected = 0
        self.active = False

    def toggle(self):
        self.active = not self.active
        self.selected = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key in (pygame.K_RETURN, pygame.K_z):
                    return self.select_option()
            return None
        
    def select_option(self):
        choice = self.options[self.selected]
        if choice == "Save Game":
            self.player.save_to_file()
            return "saved"
        elif choice == "Load Game":
            self.player.load_from_file()
            return "loaded"
        elif choice == "Return":
            self.toggle()
        return None

    def draw(self, surface):
        width, height = surface.get_size()
        box_width = 300
        box_height = 200
        x = (width - box_width) // 2
        y = (height - box_height) // 2

        pygame.draw.rect(surface, (0, 0, 0), (x, y, box_width, box_height))
        pygame.draw.rect(surface, (255, 255, 255), (x, y, box_width, box_height), 2)

        title = self.font.render("Game Menu", True, (255, 255, 0))
        surface.blit(title, (x + 90, y + 20))

        for idx, option in enumerate(self.options):
            color = (255, 255, 0) if idx == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            surface.blit(text, (x + 40, y + 60 + idx * 30))
