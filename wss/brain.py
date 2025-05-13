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

    @abstractmethod
    def calculate_move(self) -> Direction:
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
    def calculate_move(self) -> Direction:
        closest_food = self.player.vision.closest_food(self.player)
        if closest_food:
            logger.debug(
                f"Closest food for player {self.player.icon} at ({self.player.y}, {self.player.x}) is at {closest_food}"
            )
            return self._calculate_direction(
                (self.player.y, self.player.x), closest_food
            )

        closest_water = self.player.vision.closest_water(self.player)
        if (
            self.player.current_water < LOW_STAT_THRESHOLD
            or closest_water
            and self._calculate_distance((self.player.y, self.player.x), closest_water)
            < CLOSE_ITEM_THRESHOLD
        ):
            if closest_water:
                logger.debug(
                    f"Closest water for player {self.player.icon} at ({self.player.y}, {self.player.x}) is at {closest_water}"
                )
                return self._calculate_direction(
                    (self.player.y, self.player.x), closest_water
                )

        closest_gold = self.player.vision.closest_gold(self.player)
        if (
            closest_gold
            and self._calculate_distance((self.player.y, self.player.x), closest_gold)
            < CLOSE_ITEM_THRESHOLD
        ):
            if closest_gold:
                logger.debug(
                    f"Closest water for player {self.player.icon} at ({self.player.y}, {self.player.x}) is at {closest_water}"
                )
                return self._calculate_direction(
                    (self.player.y, self.player.x), closest_gold
                )

        if self.player.current_strength < VERY_LOW_STAT_THRESHOLD:
            easiest_path = self.player.vision.easiest_path(self.player)
            if easiest_path:
                logger.debug(
                    f"Easiest path for player {self.player.icon} at ({self.player.y}, {self.player.x}) is at {easiest_path}"
                )
                return self._calculate_direction(
                    (self.player.y, self.player.x), easiest_path
                )

        return Direction.EAST  # Default move


class GoldBrain(Brain):
    def calculate_move(self) -> Direction:
        # Placeholder logic for gold-seeking behavior
        return Direction.EAST


class WaterBrain(Brain):
    def calculate_move(self) -> Direction:
        # Placeholder logic for water-seeking behavior
        return Direction.EAST
