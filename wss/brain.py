from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

import logging
import math

from direction import Direction

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from player import Player

VERY_LOW_STAT_THRESHOLD = 10
LOW_STAT_THRESHOLD = 20
CLOSE_ITEM_THRESHOLD = 2


class Brain(ABC):
    def __init__(self, player: Player):
        self.player = player

    def calculate_move(self) -> Direction:
        very_low = self._check_very_low()
        if very_low:
            return self._calculate_direction((self.player.y, self.player.x), very_low)

        priority_item = self._check_priority_item()
        if priority_item:
            return self._calculate_direction(
                (self.player.y, self.player.x), priority_item
            )

        close_item = self._check_close_item()
        if close_item:
            return self._calculate_direction((self.player.y, self.player.x), close_item)

        return Direction.EAST  # Default move

    def _check_very_low(self) -> tuple[int, int] | None:
        """Check if the player is low on any stats and return the direction to move towards the nearest item."""
        if self.player.current_strength < VERY_LOW_STAT_THRESHOLD:
            return self.player.vision.easiest_path(self.player)
        if self.player.current_water < VERY_LOW_STAT_THRESHOLD:
            return self.player.vision.closest_water(self.player)
        if self.player.current_food < VERY_LOW_STAT_THRESHOLD:
            return self.player.vision.closest_food(self.player)
        return None

    def _check_close_item(self) -> tuple[int, int] | None:
        """Check if the player is close to any item and return the direction to move towards it."""
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
        """Check the player's prioritized items and return the direction to move towards it."""
        pass

    def _calculate_distance(
        self, player_pos: tuple[int, int], target_pos: tuple[int, int]
    ) -> float:
        dy = target_pos[0] - player_pos[0]
        dx = target_pos[1] - player_pos[1]
        return math.sqrt(dy * dy + dx * dx)

    def _calculate_direction(
        self, player_pos: tuple[int, int], target_pos: tuple[int, int]
    ) -> Direction:
        """Calculate the direction to move towards a target position."""

        dx = target_pos[1] - player_pos[1]
        dy = target_pos[0] - player_pos[0]
        angle = -math.atan2(dy, dx)

        rounded = round(angle / (math.pi / 4)) * (math.pi / 4)

        cardinal_directions = {
            0: Direction.EAST,
            math.pi / 4: Direction.NORTHEAST,
            math.pi / 2: Direction.NORTH,
            3 * math.pi / 4: Direction.NORTHWEST,
            math.pi: Direction.WEST,
            -3 * math.pi / 4: Direction.SOUTHWEST,
            -math.pi / 2: Direction.SOUTH,
            -math.pi / 4: Direction.SOUTHEAST,
        }

        logging.debug(
            f"Angle: {angle}, Rounded: {rounded}, Direction: {cardinal_directions.get(rounded, 'Broken')}"
        )

        assert rounded in cardinal_directions
        return cardinal_directions[rounded]


class FoodBrain(Brain):
    def _check_priority_item(self) -> tuple[int, int] | None:
        closest_food = self.player.vision.closest_food(self.player)
        if closest_food:
            logger.debug(
                f"Closest food for player {self.player.icon} at ({self.player.y}, {self.player.x}) is at {closest_food}"
            )
            return closest_food


class GoldBrain(Brain):
    def _check_priority_item(self) -> tuple[int, int] | None:
        closest_gold = self.player.vision.closest_gold(self.player)
        if closest_gold:
            logger.debug(
                f"Closest gold for player {self.player.icon} at ({self.player.y}, {self.player.x}) is at {closest_gold}"
            )
            return closest_gold


class WaterBrain(Brain):
    def _check_priority_item(self) -> tuple[int, int] | None:
        closest_water = self.player.vision.closest_water(self.player)
        if closest_water:
            logger.debug(
                f"Closest water for player {self.player.icon} at ({self.player.y}, {self.player.x}) is at {closest_water}"
            )
            return closest_water
