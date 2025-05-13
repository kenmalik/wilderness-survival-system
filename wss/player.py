from __future__ import annotations
from typing import TYPE_CHECKING

from text_renderable import TextRenderable
from rich.text import Text

from direction import Direction
from vision import Vision
from brain import FoodBrain


if TYPE_CHECKING:
    from map import Map


class Player(TextRenderable):
    MAX_STRENGTH = 100
    MAX_WATER = 100
    MAX_FOOD = 100

    def __init__(self, icon: str, map: Map, vision: Vision):
        self.current_strength = self.MAX_STRENGTH // 3
        self.current_water = self.MAX_WATER // 3 
        self.current_food = self.MAX_FOOD // 3 
        self.current_gold = 0

        self.x = -1
        self.y = -1

        self.icon = icon
        self.dead = False

        self.map = map
        self.vision = vision
        self.brain = FoodBrain(self)

        self.orientation = Direction.EAST

    def print_stats(self) -> Text:
        stats = Text()
        
        strength_style = "red" if self.current_strength <= 10 else "default"
        stats.append(f"Strength: {self.current_strength}\n", style=strength_style)

        water_style = "red" if self.current_water <= 10 else "default"
        stats.append(f"Water: {self.current_water}\n", style=water_style)
        
        food_style = "red" if self.current_food <= 10 else "default"
        stats.append(f"Food: {self.current_food}\n", style=food_style)
        
        stats.append(f"Gold: {self.current_gold}\n")
        return stats

    def render(self, context: Text):
        context.append(self.icon, style="bold white on indian_red" if not self.dead else "bold black on bright_black")

    def move_direction(self, direction: Direction):
        if direction == Direction.NORTH:
            self.orientation = Direction.NORTH
        elif direction == Direction.SOUTH:
            self.orientation = Direction.SOUTH
        elif direction == Direction.EAST or direction == Direction.NORTHEAST or direction == Direction.SOUTHEAST:
            self.orientation = Direction.EAST
        elif direction == Direction.WEST or direction == Direction.NORTHWEST or direction == Direction.SOUTHWEST:
            self.orientation = Direction.WEST

        self.map.move_player_direction(self, direction)

    def update(self) -> None:
        move = self.brain.calculate_move()
        self.move_direction(move)
        self.vision.get_visible_positions(self) # TODO: Use visible positions in brain
