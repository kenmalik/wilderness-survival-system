from direction import Direction
from item import FoodBonus, GoldBonus, Item, WaterBonus
from message_board import MessageBoard
from terrain import Plains, Desert, Mountain, Forest, Swamp, Terrain
from player import Player
import random
from rich.text import Text
from rich.panel import Panel
from rich.padding import Padding
import numpy as np
import noise
from event import Event

ITEM_TYPES = (GoldBonus, FoodBonus, WaterBonus)

type Point = tuple[int, int]


class Map:
    # Procedural Generation Parameters
    scale = 0.1
    octaves = 6
    persistence = 0.6
    lacunarity = 1.5

    def __init__(self, height: int, width: int, item_count: int):
        self.generate_terrain(height, width)
        self.players: dict[Point, Player] = {}
        self.items: dict[Point, Item] = {}
        self.populate_items(item_count)
        self.listeners = []

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

    def register_listener(self, listener: MessageBoard):
        self.listeners.append(listener)

    def notify(self, event):
        for listener in self.listeners:
            listener.on_event(event)

    def add_player(self, location: Point, player: Player) -> None:
        self.players[location] = player
        player.y = location[0]
        player.x = location[1]

    def add_item(self, location: Point, item: Item) -> None:
        self.items[location] = item

    def populate_items(self, item_count) -> None:
        self.items.clear()
        for _ in range(item_count):
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

    def update(self) -> None:
        pass

    def move_player_direction(self, player: Player, direction: Direction) -> None:
        self.notify(Event("moved", {"player": player, "direction": direction}))
        (dy, dx) = direction.value
        self.move_player(player, player.y + dy, player.x + dx)

    def move_player(self, player: Player, y: int, x: int) -> None:
        assert y >= 0 and y < len(self.terrain) and x >= 0 and x < len(self.terrain[0])
        assert player in self.players.values()

        old_position = (player.y, player.x)
        assert old_position in self.players
        del self.players[old_position]
        old_environment = self.terrain[player.y][player.x]

        new_position = (y, x)
        player.y = y
        player.x = x
        self.players[new_position] = player

        new_environment = self.terrain[y][x]
        new_environment.apply_cost(player)
        if (type(old_environment) != type(new_environment)):
            self.notify(
                Event(
                    "environment_entered",
                    {
                        "player": player,
                        "new_environment": new_environment,
                    },
                )
            )

        if (y, x) in self.items:
            item = self.items[new_position]
            item.apply_effect(player)
            self.notify(Event("item_picked_up", {"player": player, "item": item}))
