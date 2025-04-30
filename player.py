from __future__ import annotations
from typing import TYPE_CHECKING

from text_renderable import TextRenderable
from rich.text import Text


if TYPE_CHECKING:
    from map import Map


class Player(TextRenderable):
    MAX_STRENGTH = 100
    MAX_WATER = 100
    MAX_FOOD = 100

    def __init__(self, icon: str, map: Map):
        self.current_strength = self.MAX_STRENGTH // 2
        self.current_water = self.MAX_WATER // 2 
        self.current_food = self.MAX_FOOD // 2 
        self.current_gold = 0
        self.x = -1
        self.y = -1
        self.icon = icon
        self.map = map

    def print_stats(self) -> Text:
        stats = Text()
        stats.append(f"Strength: {self.current_strength}\n")
        stats.append(f"Water: {self.current_water}\n")
        stats.append(f"Food: {self.current_food}\n")
        stats.append(f"Gold: {self.current_gold}\n")
        return stats

    def render(self, context: Text):
        context.append(self.icon, style="bold white on indian_red")

    def move(self, dy: int, dx: int):
        self.map.move_player(self, self.y + dy, self.x + dx)
