from abc import ABC, abstractmethod
from drawable import Drawable
from player import Player
from console import console


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
        console.print(self.icon, end="", style="bold black on yellow")


class FoodBonus(Item):
    icon = "F"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        player.current_food += self.amount

    def draw(self):
        console.print(self.icon, end="", style="bold white on dark_red")


class WaterBonus(Item):
    icon = "W"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        player.current_water += self.amount

    def draw(self):
        console.print(self.icon, end="", style="bold white on dodger_blue3")


class Trader(Item):
    icon = "T"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        pass

    def draw(self):
        print(self.icon, end="")
