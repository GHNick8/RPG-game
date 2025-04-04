class Inventory:
    def __init__(self):
        self.items = {"Potion": 2}
        self.gold = 50

    def add_item(self, name, amount=1):
        self.items[name] = self.items.get(name, 0) + amount

    def use_item(self, name, player):
        if name == "Potion" and self.items.get("Potion", 0) > 0:
            if player.hp < player.max_hp:
                player.hp = min(player.hp + 50, player.max_hp)
                self.items["Potion"] -= 1
                return "Healed for 50 HP!"
            else:
                return "Already at full HP!"
        return "No potions left."

    def buy_item(self, name, price=10):
        if self.gold >= price:
            self.gold -= price
            self.add_item(name)
            return f"Bought {name}!"
        return "Not enough gold!"