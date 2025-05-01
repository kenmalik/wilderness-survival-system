from abc import ABC, abstractmethod
from player import Player
from text_renderable import TextRenderable
from rich.text import Text


class Item(TextRenderable, ABC):
    @abstractmethod
    def apply_effect(self, player: Player):
        pass


class GoldBonus(Item):
    icon = "G"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        player.current_gold += self.amount

    def render(self, context: Text):
        context.append(self.icon, style="bold black on yellow")


class FoodBonus(Item):
    icon = "F"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        player.current_food += self.amount

    def render(self, context: Text):
        context.append(self.icon, style="bold white on dark_red")


class WaterBonus(Item):
    icon = "W"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        player.current_water += self.amount

    def render(self, context: Text):
        context.append(self.icon, style="bold white on dodger_blue3")


class Trader(Item):
    icon = "T"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        pass

    def render(self, context: Text):
        context.append(self.icon, style="white on black")
