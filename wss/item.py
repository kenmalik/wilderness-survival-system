"""
Item module for the Wilderness Survival System.
This module defines different types of items that can be found on the map,
including resource bonuses and traders.
"""

from abc import ABC, abstractmethod
from player import Player
from text_renderable import TextRenderable
from rich.text import Text


class Item(TextRenderable, ABC):
    """
    Abstract base class for all items in the game.
    Defines the interface that all items must implement.
    """
    @abstractmethod
    def apply_effect(self, player: Player):
        """
        Apply the item's effect on a player.
        
        Args:
            player (Player): The player to apply the effect to
        """
        pass


class GoldBonus(Item):
    """
    Gold bonus item that increases the player's gold count.
    """
    icon = "G"  # Character used to represent gold on the map

    def __init__(self, amount: int):
        """
        Initialize a gold bonus item.
        
        Args:
            amount (int): The amount of gold to give to the player
        """
        self.amount = amount

    def apply_effect(self, player: Player):
        """
        Add gold to the player's current gold count.
        
        Args:
            player (Player): The player to give gold to
        """
        player.current_gold += self.amount

    def render(self, context: Text):
        """
        Render the gold bonus on the map.
        
        Args:
            context (Text): Rich text object to append the item icon to
        """
        context.append(self.icon, style="bold black on yellow")


class FoodBonus(Item):
    """
    Food bonus item that increases the player's food level.
    """
    icon = "F"  # Character used to represent food on the map

    def __init__(self, amount: int):
        """
        Initialize a food bonus item.
        
        Args:
            amount (int): The amount of food to give to the player
        """
        self.amount = amount

    def apply_effect(self, player: Player):
        """
        Add food to the player's current food level, capped at maximum.
        
        Args:
            player (Player): The player to give food to
        """
        player.current_food = min(
            player.current_food + self.amount, Player.MAX_FOOD
        )

    def render(self, context: Text):
        """
        Render the food bonus on the map.
        
        Args:
            context (Text): Rich text object to append the item icon to
        """
        context.append(self.icon, style="bold white on dark_red")


class WaterBonus(Item):
    """
    Water bonus item that increases the player's water level.
    """
    icon = "W"  # Character used to represent water on the map

    def __init__(self, amount: int):
        """
        Initialize a water bonus item.
        
        Args:
            amount (int): The amount of water to give to the player
        """
        self.amount = amount

    def apply_effect(self, player: Player):
        """
        Add water to the player's current water level, capped at maximum.
        
        Args:
            player (Player): The player to give water to
        """
        player.current_water = min(
            player.current_water + self.amount, Player.MAX_WATER
        )

    def render(self, context: Text):
        """
        Render the water bonus on the map.
        
        Args:
            context (Text): Rich text object to append the item icon to
        """
        context.append(self.icon, style="bold white on dodger_blue3")


class Trader(Item):
    """
    Trader item that represents a trading post on the map.
    Currently a placeholder for future trading functionality.
    """
    icon = "T"  # Character used to represent traders on the map

    def __init__(self, amount: int):
        """
        Initialize a trader item.
        
        Args:
            amount (int): Currently unused, placeholder for future trading mechanics
        """
        self.amount = amount

    def apply_effect(self, player: Player):
        """
        Placeholder for future trading functionality.
        Currently does nothing when a player interacts with a trader.
        
        Args:
            player (Player): The player interacting with the trader
        """
        pass

    def render(self, context: Text):
        """
        Render the trader on the map.
        
        Args:
            context (Text): Rich text object to append the item icon to
        """
        context.append(self.icon, style="white on black")
