from __future__ import annotations
from typing import TYPE_CHECKING

from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from player import Player


class Vision(ABC):
    @abstractmethod
    def get_visible_positions(self, player: Player) -> list[tuple[int, int]]:
        pass

    def closestFood(self):
        pass

    def closestWater(self):
        pass

    def closestGold(self):
        pass

    def closestTrader(self):
        pass

    def easiestPath(self):
        pass


class FocusedVision(Vision):
    fov = [(-1, 1), (0, 1), (1, 1)]

    def get_visible_positions(self, player: Player) -> list[tuple[int, int]]:
        y_limit = len(player.map.terrain)
        x_limit = len(player.map.terrain[0])
        visible_positions = [(player.y, player.x)]

        for dy, dx in self.fov:
            if (
                player.y + dy >= 0
                and player.y + dy < y_limit
                and player.x + dx >= 0
                and player.x + dx < x_limit
            ):
                visible_positions.append((player.y + dy, player.x + dx))

        return visible_positions
