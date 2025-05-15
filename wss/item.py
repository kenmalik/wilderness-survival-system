"""
Item module for the Wilderness Survival System.
This module defines different types of items that can be found on the map,
including resource bonuses and traders.
"""

from abc import ABC, abstractmethod
from player import Player
from text_renderable import TextRenderable
from rich.text import Text
import random


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

    def __str__(self):
        """
        String representation of the gold bonus item.

        Returns:
            str: The string representation of the item
        """
        return f"Gold bonus"


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
        player.current_food = min(player.current_food + self.amount, Player.MAX_FOOD)

    def render(self, context: Text):
        """
        Render the food bonus on the map.

        Args:
            context (Text): Rich text object to append the item icon to
        """
        context.append(self.icon, style="bold white on dark_red")

    def __str__(self):
        """
        String representation of the food bonus item.

        Returns:
            str: The string representation of the item
        """
        return f"Food bonus"


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
        player.current_water = min(player.current_water + self.amount, Player.MAX_WATER)

    def render(self, context: Text):
        """
        Render the water bonus on the map.

        Args:
            context (Text): Rich text object to append the item icon to
        """
        context.append(self.icon, style="bold white on dodger_blue3")

    def __str__(self):
        """
        String representation of the water bonus item.

        Returns:
            str: The string representation of the item
        """
        return f"Water bonus"


class Trader(Item, ABC):
    """
    Trader item that represents a trading post on the map.
    """

    icon = "T"

    def __init__(self):
        self.num_trades = 0
        self.MAX_TRADES = 0

    @abstractmethod
    def trader_trade(self, player: Player):
        pass

    @abstractmethod
    def player_trade(self, player: Player):
        pass

    def trade(self, player_modifier: int, trader_modifier: int) -> bool:
        player_roll = random.randint(1, 20) + player_modifier
        trader_roll = random.randint(1, 20) + trader_modifier
        return player_roll >= trader_roll

    def apply_effect(self, player: Player):
        while self.num_trades <= self.MAX_TRADES:
            self.trader_trade(player)
            if self.num_trades <= self.MAX_TRADES:
                self.player_trade(player)
        self.num_trades = 0

    def render(self, context: Text):
        """
        Render the trader on the map.

        Args:
            context (Text): Rich text object to append the item icon to
        """
        context.append(self.icon, style="white on black")

    def __str__(self):
        """
        String representation of the trader item.

        Returns:
            str: The string representation of the item
        """
        return "Trader"


class FairTrader(Trader):
    def __init__(self):
        super().__init__()
        self.MAX_TRADES = 6

    def trader_trade(self, player: Player):
        give, take = random.sample(["gold", "water", "food"], 2)
        num_traded = random.randint(5, 15)
        # event offer

        # Trader giving gold
        if give == "gold":
            if take == "water":
                if player.current_water >= num_traded:
                    if self.trade(num_traded * -1, 0):
                        player.current_gold = player.current_gold + num_traded
                        player.current_water = player.current_water - num_traded
                        self.num_trades += 1
                        # accept
                    else:
                        # decline
                        self.num_trades += 1
            elif take == "food":
                if player.current_food >= num_traded:
                    if self.trade(num_traded * -1, 0):
                        player.current_gold = player.current_gold + num_traded
                        player.current_food = player.current_food - num_traded
                        self.num_trades += 1
                        # accept
                    else:
                        # decline
                        self.num_trades += 1

        # Trader giving water
        elif give == "water":
            if take == "food":
                if (
                    player.current_food >= num_traded
                    and player.current_food > player.current_water * 2
                ):
                    if self.trade(0, 0):
                        player.current_water = min(
                            player.current_water + num_traded, Player.MAX_WATER
                        )
                        player.current_food = player.current_food - num_traded
                        self.num_trades += 1
                        # accept
                    else:
                        # decline
                        self.num_trades += 1
            elif take == "gold":
                if player.current_gold >= num_traded:
                    if self.trade(0, 0):
                        player.current_water = min(
                            player.current_water + num_traded, Player.MAX_WATER
                        )
                        self.num_trades += 1
                    else:
                        # decline
                        self.num_trades += 1

        # Trader giving food
        elif give == "food":
            if take == "water":
                if (
                    player.current_water >= num_traded
                    and player.current_water > player.current_food * 2
                ):
                    if self.trade(0, 0):
                        player.current_food = min(
                            player.current_food + num_traded, Player.MAX_FOOD
                        )
                        player.current_water = player.current_water - num_traded
                        self.num_trades += 1
                    else:
                        # decline
                        self.num_trades += 1
            elif take == "gold":
                if player.current_gold >= num_traded:
                    if self.trade(0, 0):
                        player.current_food = min(
                            player.current_food + num_traded, Player.MAX_FOOD
                        )
                        player.current_gold = player.current_gold - num_traded
                        self.num_trades += 1
                    else:
                        # decline
                        self.num_trades += 1

    def player_trade(self, player: Player):
        if player.current_gold <= 0:
            return
        num_traded = min(player.current_gold, random.randint(5, 15))
        if player.current_food < player.current_water:
            if self.trade(0, 0):
                player.current_water = min(
                    player.current_food + num_traded, Player.MAX_FOOD
                )
                player.current_gold = player.current_gold - num_traded
                self.num_trades += 1
                # accept
            else:
                self.num_trades += 1
                # decline
        else:
            if self.trade(0, 0):
                player.current_water = min(
                    player.current_water + num_traded, Player.MAX_WATER
                )
                player.current_gold = player.current_gold - num_traded
                self.num_trades += 1
                # accept
            else:
                self.num_trades += 1
                # decline


class HagglingTrader(Trader):
    def __init__(self):
        super().__init__()
        self.MAX_TRADES = 10

    def trader_trade(self, player: Player):
        give, take = random.sample(["gold", "water", "food"], 2)
        num_traded = random.randint(5, 15)
        # event offer

        # Trader giving gold
        if give == "gold":
            if take == "water":
                if player.current_water >= num_traded:
                    if self.trade(num_traded * -1, self.num_trades):
                        player.current_gold = (
                            player.current_gold + num_traded - self.num_trades
                        )
                        player.current_water = player.current_water - num_traded
                        self.num_trades += 1
                        # accept
                    else:
                        # decline
                        self.num_trades += 1
            elif take == "food":
                if player.current_food >= num_traded:
                    if self.trade(num_traded * -1, self.num_trades):
                        player.current_gold = (
                            player.current_gold + num_traded - self.num_trades
                        )
                        player.current_food = player.current_food - num_traded
                        self.num_trades += 1
                        # accept
                    else:
                        # decline
                        self.num_trades += 1

        # Trader giving water
        elif give == "water":
            if take == "food":
                if (
                    player.current_food >= num_traded
                    and player.current_food > player.current_water * 2
                ):
                    if self.trade(0, self.num_trades):
                        player.current_water = min(
                            player.current_water + num_traded - self.num_trades,
                            Player.MAX_WATER,
                        )
                        player.current_food = player.current_food - num_traded
                        self.num_trades += 1
                        # accept
                    else:
                        # decline
                        self.num_trades += 1
            elif take == "gold":
                if player.current_gold >= num_traded:
                    if self.trade(0, 0):
                        player.current_water = min(
                            player.current_water + num_traded - self.num_trades,
                            Player.MAX_WATER,
                        )
                        self.num_trades += 1
                    else:
                        # decline
                        self.num_trades += 1

        # Trader giving food
        elif give == "food":
            if take == "water":
                if (
                    player.current_water >= num_traded
                    and player.current_water > player.current_food * 2
                ):
                    if self.trade(0, self.num_trades):
                        player.current_food = min(
                            player.current_food + num_traded - self.num_trades,
                            Player.MAX_FOOD,
                        )
                        player.current_water = player.current_water - num_traded
                        self.num_trades += 1
                    else:
                        # decline
                        self.num_trades += 1
            elif take == "gold":
                if player.current_gold >= num_traded:
                    if self.trade(0, 0):
                        player.current_food = min(
                            player.current_food + num_traded - self.num_trades,
                            Player.MAX_FOOD,
                        )
                        player.current_gold = player.current_gold - num_traded
                        self.num_trades += 1
                    else:
                        # decline
                        self.num_trades += 1

    def player_trade(self, player: Player):
        if player.current_gold == 0:
            return
        num_traded = min(player.current_gold, random.randint(5, 15))
        if player.current_food < player.current_water:
            if self.trade(0, self.num_trades):
                player.current_water = min(
                    player.current_food + num_traded - self.num_trades, Player.MAX_FOOD
                )
                player.current_gold = player.current_gold - num_traded
                self.num_trades += 1
                # accept
            else:
                self.num_trades += 1
                # decline
        else:
            if self.trade(0, self.num_trades):
                player.current_water = min(
                    player.current_water + num_traded - self.num_trades,
                    Player.MAX_WATER,
                )
                player.current_gold = player.current_gold - num_traded
                self.num_trades += 1
                # accept
            else:
                self.num_trades += 1
                # decline
