from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player

import logging

logger = logging.getLogger(__name__)


class Vision():
    fov = [(0, 0)]

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

        logger.debug(f"Player {player.icon} at ({player.y}, {player.x}), sees {visible_positions}")

        return visible_positions

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


class CautiousVision(Vision):
    fov = [(-1, 0), (0, 1), (1, 1)]


class KeenEyedVision(Vision):
    fov = [(-1, 0), (-1, 1), (0, 1), (0, 2), (1, 0), (1, 1)]


class FarSightVision(Vision):
    fov = [(-2, 0), (-2, 1), (-1, 0), (-1, 1), (-1, 2), (0, 1), (0,2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)]
