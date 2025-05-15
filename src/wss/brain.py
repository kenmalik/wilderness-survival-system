"""
Brain module for the Wilderness Survival System.
This module defines the AI decision-making system for players,
including different types of brains with varying priorities.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

import logging
import math

from direction import Direction, angle_to_direction
from event import Event

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from player import Player

# Thresholds for resource management
VERY_LOW_STAT_THRESHOLD = 10  # Critical level for resources
LOW_STAT_THRESHOLD = 20  # Warning level for resources
CLOSE_ITEM_THRESHOLD = 2  # Distance at which items are considered "close"


class Brain(ABC):
    """
    Abstract base class for player AI brains.
    Defines the decision-making logic for player movement and resource gathering.
    """

    def __init__(self, player: Player):
        """
        Initialize a brain for a player.

        Args:
            player (Player): The player this brain controls
        """
        self.player = player

    def choose_action(self) -> Event:
        """
        Calculate the next action for the player based on current conditions.

        Priority order:
        1. Rest if strength is very low
        2. Move towards resources if any stat is very low
        3. Move towards priority items based on brain type
        4. Move towards any close items
        5. Default to moving east

        Returns:
            Direction: The direction to move in
        """

        # Check if need to rest
        if self.player.current_strength < VERY_LOW_STAT_THRESHOLD:
            return Event("rest", None)

        # Check for critically low stats first
        very_low = self._check_very_low()
        if very_low:
            return Event(
                "move",
                {
                    "direction": self._calculate_direction(
                        (self.player.y, self.player.x), very_low
                    )
                },
            )

        # Check for priority items based on brain type
        priority_item = self._check_priority_item()
        if priority_item:
            return Event(
                "move",
                {
                    "direction": self._calculate_direction(
                        (self.player.y, self.player.x), priority_item
                    )
                },
            )

        # Check for any close items
        close_item = self._check_close_item()
        if close_item:
            return Event(
                "move",
                {
                    "direction": self._calculate_direction(
                        (self.player.y, self.player.x), close_item
                    )
                },
            )

        return Event("move", {"direction": Direction.EAST})  # Default to moving east

    def _check_very_low(self) -> tuple[int, int] | None:
        """
        Check if the player is low on any stats and return the direction to move
        towards the nearest item of the needed type.

        Returns:
            tuple[int, int] | None: Coordinates of the nearest needed item, or None
        """
        if self.player.current_water < VERY_LOW_STAT_THRESHOLD:
            return self.player.vision.closest_water(self.player)
        if self.player.current_food < VERY_LOW_STAT_THRESHOLD:
            return self.player.vision.closest_food(self.player)
        if self.player.current_gold > LOW_STAT_THRESHOLD:
            return self.player.vision.closest_trader(self.player)
        return None

    def _check_close_item(self) -> tuple[int, int] | None:
        """
        Check if the player is close to any item and return its location.

        Returns:
            tuple[int, int] | None: Coordinates of the closest item, or None
        """
        close_items = [
            self.player.vision.closest_gold(self.player),
            self.player.vision.closest_water(self.player),
            self.player.vision.closest_food(self.player),
        ]

        for item in close_items:
            if (
                item
                and self._calculate_distance((self.player.y, self.player.x), item)
                < CLOSE_ITEM_THRESHOLD
            ):
                return item
        return None

    @abstractmethod
    def _check_priority_item(self) -> tuple[int, int] | None:
        """
        Check the player's prioritized items and return the direction to move towards it.
        This method is implemented differently by each brain type.

        Returns:
            tuple[int, int] | None: Coordinates of the priority item, or None
        """
        pass

    def _calculate_distance(
        self, player_pos: tuple[int, int], target_pos: tuple[int, int]
    ) -> float:
        """
        Calculate the Euclidean distance between two points.

        Args:
            player_pos (tuple[int, int]): Player's current position
            target_pos (tuple[int, int]): Target position

        Returns:
            float: Distance between the points
        """
        dy = target_pos[0] - player_pos[0]
        dx = target_pos[1] - player_pos[1]
        return math.sqrt(dy * dy + dx * dx)

    def _calculate_direction(
        self, player_pos: tuple[int, int], target_pos: tuple[int, int]
    ) -> Direction:
        """
        Calculate the direction to move towards a target position.
        Uses angle calculations to determine the closest cardinal or diagonal direction.

        Args:
            player_pos (tuple[int, int]): Player's current position
            target_pos (tuple[int, int]): Target position

        Returns:
            Direction: The direction to move in
        """
        dx = target_pos[1] - player_pos[1]
        dy = target_pos[0] - player_pos[0]
        angle = -math.atan2(dy, dx)

        direction = angle_to_direction(angle)

        return direction


class FoodBrain(Brain):
    """
    Brain type that prioritizes finding food.
    Players with this brain will focus on gathering food resources.
    """

    def _check_priority_item(self) -> tuple[int, int] | None:
        """
        Find the closest food item to the player.

        Returns:
            tuple[int, int] | None: Coordinates of the closest food, or None
        """
        closest_food = self.player.vision.closest_food(self.player)
        if closest_food:
            logger.debug(
                f"Closest food for player {self.player.icon} at ({self.player.y}, {self.player.x}) is at {closest_food}"
            )
            return closest_food

    def __str__(self) -> str:
        """
        String representation of the FoodBrain class.

        Returns:
            str: Class name
        """
        return "Food Brain"


class GoldBrain(Brain):
    """
    Brain type that prioritizes finding gold.
    Players with this brain will focus on gathering gold resources.
    """

    def _check_priority_item(self) -> tuple[int, int] | None:
        """
        Find the closest gold item to the player.

        Returns:
            tuple[int, int] | None: Coordinates of the closest gold, or None
        """
        closest_gold = self.player.vision.closest_gold(self.player)
        if closest_gold:
            logger.debug(
                f"Closest gold for player {self.player.icon} at ({self.player.y}, {self.player.x}) is at {closest_gold}"
            )
            return closest_gold

    def __str__(self) -> str:
        """
        String representation of the GoldBrain class.

        Returns:
            str: Class name
        """
        return "Gold Brain"


class WaterBrain(Brain):
    """
    Brain type that prioritizes finding water.
    Players with this brain will focus on gathering water resources.
    """

    def _check_priority_item(self) -> tuple[int, int] | None:
        """
        Find the closest water item to the player.

        Returns:
            tuple[int, int] | None: Coordinates of the closest water, or None
        """
        closest_water = self.player.vision.closest_water(self.player)
        if closest_water:
            logger.debug(
                f"Closest water for player {self.player.icon} at ({self.player.y}, {self.player.x}) is at {closest_water}"
            )
            return closest_water

    def __str__(self) -> str:
        """
        String representation of the WaterBrain class.

        Returns:
            str: Class name
        """
        return "Water Brain"
