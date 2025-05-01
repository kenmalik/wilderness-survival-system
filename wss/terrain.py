from abc import ABC, abstractmethod
from player import Player
from text_renderable import TextRenderable
from rich.text import Text


class Terrain(TextRenderable, ABC):
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

    def render(self, context: Text):
        context.append(self.ICON, style="wheat4 on dark_sea_green3")

    def __str__(self):
        return "plains"


class Desert(Terrain):
    ICON = "*"
    MOVEMENT_COST = 1
    WATER_COST = 2
    FOOD_COST = 1

    def apply_cost(self, player: Player):
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def render(self, context: Text):
        context.append(self.ICON, style="grey53 on light_yellow3")

    def __str__(self):
        return "desert"


class Mountain(Terrain):
    ICON = "^"
    MOVEMENT_COST = 1
    WATER_COST = 2
    FOOD_COST = 1

    def apply_cost(self, player: Player):
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def render(self, context: Text):
        context.append(self.ICON, style="grey37 on grey53")

    def __str__(self):
        return "mountain"


class Forest(Terrain):
    ICON = "#"
    MOVEMENT_COST = 1
    WATER_COST = 2
    FOOD_COST = 1

    def apply_cost(self, player: Player):
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def render(self, context: Text):
        context.append(self.ICON, style="wheat4 on dark_sea_green4")

    def __str__(self):
        return "forest"


class Swamp(Terrain):
    ICON = "="
    MOVEMENT_COST = 1
    WATER_COST = 2
    FOOD_COST = 1

    def apply_cost(self, player: Player):
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def render(self, context: Text):
        context.append(self.ICON, style="dark_green on chartreuse4")

    def __str__(self):
        return "swamp"
