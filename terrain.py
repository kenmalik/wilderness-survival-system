from drawable import Drawable
from abc import ABC, abstractmethod
from player import Player
from console import console

class Terrain(Drawable, ABC):
    @abstractmethod
    def apply_cost(self, player: Player):
        pass


class Plains(Terrain):
    ICON = "~"
    MOVEMENT_COST = 1
    WATER_COST = 1
    FOOD_COST = 1

    def apply_cost(self, player: Player):
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def draw(self):
        console.print(self.ICON, end="", style="wheat4 on dark_sea_green3")


class Desert(Terrain):
    ICON = "*"
    MOVEMENT_COST = 1
    WATER_COST = 2
    FOOD_COST = 1

    def apply_cost(self, player: Player):
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def draw(self):
        console.print(self.ICON, end="", style="grey53 on light_yellow3")


class Mountain(Terrain):
    ICON = "^"
    MOVEMENT_COST = 1
    WATER_COST = 2
    FOOD_COST = 1

    def apply_cost(self, player: Player):
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def draw(self):
        console.print(self.ICON, end="", style="grey37 on grey53")


class Forest(Terrain):
    ICON = "#"
    MOVEMENT_COST = 1
    WATER_COST = 2
    FOOD_COST = 1

    def apply_cost(self, player: Player):
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def draw(self):
        console.print(self.ICON, end="", style="wheat4 on dark_sea_green4")


class Swamp(Terrain):
    ICON = "="
    MOVEMENT_COST = 1
    WATER_COST = 2
    FOOD_COST = 1

    def apply_cost(self, player: Player):
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def draw(self):
        console.print(self.ICON, end="", style="dark_green on chartreuse4")
