#character.py
from Inventory import Inventory


class Character:
    def init(self, name, health=100):
        self.name = name
        self.health = health
        self.inventory = Inventory()

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"{self.name} took {damage} damage. Health: {self.health}")

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100
        print(f"{self.name} healed for {amount} health. Health: {self.health}")

    def add_item(self, item, description):
        self.inventory.add_item(item, description)

    def remove_item(self, item):
        self.inventory.remove_item(item)

    def view_inventory(self):
        self.inventory.view_inventory()

    def use_item(self, item):
        self.inventory.use_item(item)

    def str(self):
        return f"{self.name} - Health: {self.health}"


class Enemy(Character):
    def __init__(self, name, health):
        super().init(name, health)

class Goons(Enemy):
    def __init__(self):
        super().init("Goon", 100)

class Bullseye(Enemy):
    def __init__(self):
        super().init("Bullseye", 300)

class Fisk(Enemy):
    def __init__(self):
        super().init("Fisk", 400)

class Daredevil(Character):
    def __init__(self):
        super().init("Daredevil", 250) 


