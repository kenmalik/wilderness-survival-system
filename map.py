from item import FoodBonus, GoldBonus, Item, WaterBonus
from terrain import Plains, Desert, Mountain, Forest, Swamp, Terrain
from player import Player
import random
from rich.text import Text
from rich.panel import Panel
from rich.padding import Padding

TERRAIN_TYPES = (Plains, Desert, Mountain, Forest, Swamp)
ITEM_TYPES = (GoldBonus, FoodBonus, WaterBonus)
ITEM_COUNT = 10

type Point = tuple[int, int]


class Map:
    def __init__(self, x: int, y: int):
        self.terrain: list[list[Terrain]] = [
            [random.choice(TERRAIN_TYPES)() for _ in range(y)] for _ in range(x)
        ]
        self.players: dict[Point, Player] = {}
        self.items: dict[Point, Item] = {}

    def draw(self) -> Panel:
        context = Text(justify="center")
        for i, row in enumerate(self.terrain):
            for j, square in enumerate(row):
                if (i, j) in self.players:
                    self.players[(i, j)].render(context)
                elif (i, j) in self.items:
                    self.items[(i, j)].render(context)
                else:
                    square.render(context)
            context.append("\n")
        context.remove_suffix("\n")
        return Panel(Padding(context, (1, 2)), title="World Map")

    def add_player(self, location: Point, player: Player):
        self.players[location] = player

    def add_item(self, location: Point, item: Item):
        self.items[location] = item

    def populate_items(self):
        self.items.clear()
        for _ in range(ITEM_COUNT):
            location: Point = (
                random.randrange(len(self.terrain)),
                random.randrange(len(self.terrain[0])),
            )
            while location in self.items:
                location = (
                    random.randrange(len(self.terrain)),
                    random.randrange(len(self.terrain[0])),
                )
            self.items[location] = random.choice(ITEM_TYPES)(random.randrange(1, 4))
