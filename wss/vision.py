"""
Vision module for the Wilderness Survival System.
This module defines different types of vision systems that determine
what players can see on the map and how they perceive their surroundings.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from direction import Direction, direction_strings

if TYPE_CHECKING:
    from player import Player

import logging

logger = logging.getLogger(__name__)


class Vision():
    """
    Base vision class that defines how players perceive the game world.
    The field of view (FOV) determines which tiles a player can see.
    """
    # Default field of view - only sees current position
    fov = [(0, 0)]

    def get_visible_positions(self, player: Player) -> list[tuple[int, int]]:
        """
        Calculate all positions visible to the player based on their FOV and orientation.
        
        Args:
            player (Player): The player whose vision to calculate
            
        Returns:
            list[tuple[int, int]]: List of (y, x) coordinates visible to the player
        """
        y_limit = len(player.map.terrain)
        x_limit = len(player.map.terrain[0])
        visible_positions = [(player.y, player.x)]  # Player can always see their position

        # Transform FOV coordinates based on player orientation
        for dy, dx in self.fov:
            if player.orientation == Direction.WEST:
                dx = -dx
            elif player.orientation == Direction.SOUTH:
                temp = dy
                dy = dx
                dx = temp
            elif player.orientation == Direction.NORTH:
                temp = dy
                dy = -dx
                dx = temp

            # Check if position is within map bounds
            if (
                player.y + dy >= 0
                and player.y + dy < y_limit
                and player.x + dx >= 0
                and player.x + dx < x_limit
            ):
                visible_positions.append((player.y + dy, player.x + dx))

        logger.debug(f"Player {player.icon} at ({player.y}, {player.x}), facing {direction_strings[player.orientation]}, sees {visible_positions}")

        return visible_positions

    def _closest_item(self, player: Player, item_type):
        """
        Find the closest item of a specific type within the player's field of view.
        
        Args:
            player (Player): The player looking for the item
            item_type: The type of item to look for
            
        Returns:
            tuple[int, int] | None: Coordinates of the closest item, or None if not found
        """
        visible_positions = self.get_visible_positions(player)
        candidates = []

        # Check each visible position for the target item type
        for y, x in visible_positions:
            pos = (y, x)
            if pos in player.map.items and isinstance(player.map.items[pos], item_type):
                    terrain = player.map.terrain[y][x]
                    movement_cost = terrain.MOVEMENT_COST
                    distance = abs(y - player.y) + abs(x - player.x)
                    candidates.append((pos, distance, movement_cost, x))  # x => eastward value

        if not candidates:
            return None

        # Sort by (1) shortest distance (2) lowest movement cost (3) furthest east
        candidates.sort(key=lambda tup: (tup[1], tup[2], -tup[3]))
        return candidates[0][0]  # returns (y, x)

    def closest_food(self, player): 
        """
        Find the closest food item to the player.
        
        Args:
            player (Player): The player looking for food
            
        Returns:
            tuple[int, int] | None: Coordinates of the closest food, or None
        """
        from item import FoodBonus   # To avoid circular import issue
        return self._closest_item(player, FoodBonus)

    def closest_water(self, player):
        """
        Find the closest water item to the player.
        
        Args:
            player (Player): The player looking for water
            
        Returns:
            tuple[int, int] | None: Coordinates of the closest water, or None
        """
        from item import WaterBonus
        return self._closest_item(player, WaterBonus)

    def closest_gold(self, player): 
        """
        Find the closest gold item to the player.
        
        Args:
            player (Player): The player looking for gold
            
        Returns:
            tuple[int, int] | None: Coordinates of the closest gold, or None
        """
        from item import GoldBonus  
        return self._closest_item(player, GoldBonus)

    def closest_trader(self, player): 
        """
        Find the closest trader to the player.
        
        Args:
            player (Player): The player looking for a trader
            
        Returns:
            tuple[int, int] | None: Coordinates of the closest trader, or None
        """
        from item import Trader
        return self._closest_item(player, Trader)
        
    def easiest_path(self, player):
        """
        Find the easiest path to move through based on terrain movement costs.
        
        Args:
            player (Player): The player looking for a path
            
        Returns:
            tuple[int, int] | None: Coordinates of the easiest path, or None
        """
        visible_positions = self.get_visible_positions(player)
        candidates = []

        # Evaluate each visible position based on movement cost
        for y, x in visible_positions:
            terrain = player.map.terrain[y][x]
            movement_cost = terrain.MOVEMENT_COST
            candidates.append(((y, x), movement_cost, x))  # x = eastward bias  

        if not candidates:
            return None

        # Sort by (1) lowest movement cost, then (2) furthest east (highest x)
        candidates.sort(key=lambda tup: (tup[1], -tup[2]))
        return candidates[0][0]


class FocusedVision(Vision):
    """
    Vision type that focuses on the forward direction.
    Can see three tiles ahead in a forward-facing pattern.
    """
    fov = [(-1, 1), (0, 1), (1, 1)]  # Forward-facing triangle pattern


class CautiousVision(Vision):
    """
    Vision type that prioritizes safety.
    Can see forward and slightly to the side, avoiding blind spots.
    """
    fov = [(-1, 0), (0, 1), (1, 1)]  # Forward and side vision


class KeenEyedVision(Vision):
    """
    Vision type with enhanced perception.
    Can see further ahead and to the sides in a wider pattern.
    """
    fov = [(-1, 0), (-1, 1), (0, 1), (0, 2), (1, 0), (1, 1)]  # Wider forward vision


class FarSightVision(Vision):
    """
    Vision type with the longest range.
    Can see far ahead and to the sides in a wide pattern.
    """
    fov = [(-2, 0), (-2, 1), (-1, 0), (-1, 1), (-1, 2), (0, 1), (0,2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)]  # Long-range vision
