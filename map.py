from item import FoodBonus, GoldBonus, Item, WaterBonus
from terrain import Plains, Desert, Mountain, Forest, Swamp, Terrain
from player import Player
import random
from rich.text import Text
from rich.panel import Panel
from rich.padding import Padding
import numpy as np
import noise

ITEM_TYPES = (GoldBonus, FoodBonus, WaterBonus)
ITEM_COUNT = 10

type Point = tuple[int, int]


class Map:
    # Procedural Generation Parameters
    scale = 0.1
    octaves = 6
    persistence = 0.6
    lacunarity = 1.5

    def __init__(self, height: int, width: int):
        self.generate_terrain(height, width)
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

    def add_player(self, location: Point, player: Player) -> None:
        self.players[location] = player

    def add_item(self, location: Point, item: Item) -> None:
        self.items[location] = item

    def populate_items(self) -> None:
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

    def generate_terrain(self, height: int, width: int) -> None:
        base = random.randrange(0, 500, 10)
        height_map = np.zeros((height, width))
        for y in range(height):
            for x in range(width):
                height_map[y][x] = noise.pnoise2(
                    x * self.scale,
                    y * self.scale,
                    octaves=self.octaves,
                    persistence=self.persistence,
                    lacunarity=self.lacunarity,
                    repeatx=width,
                    repeaty=height,
                    base=base,
                )

        # Normalize to 0-1
        height_map = (height_map - height_map.min()) / (
            height_map.max() - height_map.min()
        )

        self.terrain: list[list[Terrain]] = [
            [self.get_terrain(height_map[y][x])() for x in range(width)]
            for y in range(height)
        ]

    def get_terrain(self, elevation):
        if elevation < 0.3:
            return Swamp
        elif elevation < 0.5:
            return Plains
        elif elevation < 0.62:
            return Desert
        elif elevation < 0.8:
            return Forest
        else:
            return Mountain
