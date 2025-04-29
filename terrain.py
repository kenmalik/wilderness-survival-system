from drawable import Drawable
from abc import ABC, abstractmethod
from player import Player

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
        print(self.ICON, end="")


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
        print(self.ICON, end="")


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
        print(self.ICON, end="")


class Forest(Terrain):
    ICON = "$"
    MOVEMENT_COST = 1
    WATER_COST = 2
    FOOD_COST = 1

    def apply_cost(self, player: Player):
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def draw(self):
        print(self.ICON, end="")


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
        print(self.ICON, end="")
