"""
Terrain module for the Wilderness Survival System.
This module defines different types of terrain that can appear on the map,
each with unique properties and effects on players.
"""

from abc import ABC, abstractmethod

from rich.text import Text

from wss_py.text_renderable import TextRenderable
from wss_py.player import Player

class Terrain(TextRenderable, ABC):
    """
    Abstract base class for all terrain types.
    Defines the interface that all terrain types must implement.
    """

    # Default properties for terrain
    ICON = "?"              # Character used to represent terrain on the map
    MOVEMENT_COST = -1       # Strength cost for moving through terrain
    WATER_COST = -1         # Water cost for moving through terrain
    FOOD_COST = -1          # Food cost for moving through terrain

    @abstractmethod
    def apply_cost(self, player: Player):
        """
        Apply the terrain's effects on a player.
        
        Args:
            player (Player): The player to apply effects to
        """
        pass


class Plains(Terrain):
    """
    Plains terrain type.
    Represents flat, open grasslands with moderate resource costs.
    """
    ICON = "~"              # Character used to represent plains on the map
    MOVEMENT_COST = 1       # Strength cost for moving through plains
    WATER_COST = 1         # Water cost for moving through plains
    FOOD_COST = 1          # Food cost for moving through plains

    def apply_cost(self, player: Player):
        """
        Apply plains terrain costs to the player.
        Reduces player's food, water, and strength.
        """
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def render(self, context: Text):
        """
        Render the plains terrain on the map.
        
        Args:
            context (Text): Rich text object to append the terrain icon to
        """
        context.append(self.ICON, style="wheat4 on dark_sea_green3")

    def __str__(self):
        return "plains"


class Desert(Terrain):
    """
    Desert terrain type.
    Represents arid, sandy areas with high water consumption.
    """
    ICON = "*"              # Character used to represent desert on the map
    MOVEMENT_COST = 1       # Strength cost for moving through desert
    WATER_COST = 2         # Higher water cost due to arid conditions
    FOOD_COST = 1          # Food cost for moving through desert

    def apply_cost(self, player: Player):
        """
        Apply desert terrain costs to the player.
        Reduces player's food, water, and strength.
        """
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def render(self, context: Text):
        """
        Render the desert terrain on the map.
        
        Args:
            context (Text): Rich text object to append the terrain icon to
        """
        context.append(self.ICON, style="grey53 on light_yellow3")

    def __str__(self):
        return "desert"


class Mountain(Terrain):
    """
    Mountain terrain type.
    Represents high elevation areas with challenging movement.
    """
    ICON = "^"              # Character used to represent mountains on the map
    MOVEMENT_COST = 1       # Strength cost for moving through mountains
    WATER_COST = 2         # Higher water cost due to elevation
    FOOD_COST = 1          # Food cost for moving through mountains

    def apply_cost(self, player: Player):
        """
        Apply mountain terrain costs to the player.
        Reduces player's food, water, and strength.
        """
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def render(self, context: Text):
        """
        Render the mountain terrain on the map.
        
        Args:
            context (Text): Rich text object to append the terrain icon to
        """
        context.append(self.ICON, style="grey37 on grey53")

    def __str__(self):
        return "mountain"


class Forest(Terrain):
    """
    Forest terrain type.
    Represents dense woodland areas with moderate resource costs.
    """
    ICON = "#"              # Character used to represent forest on the map
    MOVEMENT_COST = 1       # Strength cost for moving through forest
    WATER_COST = 2         # Higher water cost due to dense vegetation
    FOOD_COST = 1          # Food cost for moving through forest

    def apply_cost(self, player: Player):
        """
        Apply forest terrain costs to the player.
        Reduces player's food, water, and strength.
        """
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def render(self, context: Text):
        """
        Render the forest terrain on the map.
        
        Args:
            context (Text): Rich text object to append the terrain icon to
        """
        context.append(self.ICON, style="wheat4 on dark_sea_green4")

    def __str__(self):
        return "forest"


class Swamp(Terrain):
    """
    Swamp terrain type.
    Represents wet, marshy areas with challenging movement.
    """
    ICON = "="              # Character used to represent swamp on the map
    MOVEMENT_COST = 1       # Strength cost for moving through swamp
    WATER_COST = 2         # Higher water cost due to wet conditions
    FOOD_COST = 1          # Food cost for moving through swamp

    def apply_cost(self, player: Player):
        """
        Apply swamp terrain costs to the player.
        Reduces player's food, water, and strength.
        """
        player.current_food -= self.FOOD_COST
        player.current_water -= self.WATER_COST
        player.current_strength -= self.MOVEMENT_COST

    def render(self, context: Text):
        """
        Render the swamp terrain on the map.
        
        Args:
            context (Text): Rich text object to append the terrain icon to
        """
        context.append(self.ICON, style="dark_green on chartreuse4")

    def __str__(self):
        return "swamp"
