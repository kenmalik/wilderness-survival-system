from abc import ABC
from player import Player

import logging

logger = logging.getLogger(__name__)


class Brain(ABC):
    def __init__(self, player: Player):
        self.player = player

    def make_move(self) -> None:
        pass


class FoodBrain(Brain):
    pass


class GoldBrain(Brain):
    pass


class WaterBrain(Brain):
    pass
