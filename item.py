from abc import ABC, abstractmethod
from drawable import Drawable
from player import Player


class Item(Drawable, ABC):
    @abstractmethod
    def apply_effect(self, player: Player):
        pass


class GoldBonus(Item):
    icon = "G"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        player.current_gold += self.amount

    def draw(self):
        print(self.icon, end="")


class FoodBonus(Item):
    icon = "F"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        player.current_food += self.amount

    def draw(self):
        print(self.icon, end="")


class WaterBonus(Item):
    icon = "W"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        player.current_water += self.amount

    def draw(self):
        print(self.icon, end="")


class Trader(Item):
    icon = "T"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        pass

    def draw(self):
        print(self.icon, end="")
