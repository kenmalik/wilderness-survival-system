from __future__ import annotations
from typing import TYPE_CHECKING

from direction import Direction, direction_strings

if TYPE_CHECKING:
    from player import Player

import logging

logger = logging.getLogger(__name__)


class Vision():
    fov = [(0, 0)]

    def get_visible_positions(self, player: Player) -> list[tuple[int, int]]:
        """Return valid positions on the map that a player can see"""

        y_limit = len(player.map.terrain)
        x_limit = len(player.map.terrain[0])
        visible_positions = [(player.y, player.x)]

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
        visible_positions = self.get_visible_positions(player)
        candidates = []

        for y, x in visible_positions:
            pos = (y, x)
            if pos in player.map.items and isinstance(player.map.items[pos], item_type):
                    terrain = player.map.terrain[y][x]
                    movement_cost = terrain.MOVEMENT_COST
                    distance = abs(y - player.y) + abs(x - player.x)
                    candidates.append((pos, distance, movement_cost, x))  #x => eastward value

        if not candidates:
            return None

        # Sort by (1) shortest distance (2) lowest movement cost (3) furthest east
        candidates.sort(key=lambda tup: (tup[1], tup[2], -tup[3]))
        return candidates[0][0]  # returns (y, x)

    def closest_food(self, player): 
        from item import FoodBonus   # To avoid circular import issue
        return self._closest_item(player, FoodBonus)

    def closest_water(self, player):
        from item import WaterBonus
        return self._closest_item(player, WaterBonus)

    def closest_gold(self, player): 
        from item import GoldBonus  
        return self._closest_item(player, GoldBonus)

    def closest_trader(self, player): 
        from item import Trader
        return self._closest_item(player, Trader)
        
    def easiest_path(self, player):
        visible_positions = self.get_visible_positions(player)
        candidates = []

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
    fov = [(-1, 1), (0, 1), (1, 1)]


class CautiousVision(Vision):
    fov = [(-1, 0), (0, 1), (1, 1)]


class KeenEyedVision(Vision):
    fov = [(-1, 0), (-1, 1), (0, 1), (0, 2), (1, 0), (1, 1)]


class FarSightVision(Vision):
    fov = [(-2, 0), (-2, 1), (-1, 0), (-1, 1), (-1, 2), (0, 1), (0,2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)]
