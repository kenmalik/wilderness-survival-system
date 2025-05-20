"""
Map module for the Wilderness Survival System.
This module handles the game map, including terrain generation, item placement,
and player movement mechanics.
"""

from wss_py.direction import Direction
from wss_py.item import FoodBonus, GoldBonus, Item, WaterBonus, Trader, FairTrader, HagglingTrader
from wss_py.terrain import Plains, Desert, Mountain, Forest, Swamp, Terrain
from wss_py.player import Player
from wss_py.event import Event
from wss_py.listener import Listener

from rich.text import Text
from rich.panel import Panel
from rich.padding import Padding
import numpy as np
import noise

import random

# Types of items that can be placed on the map
ITEM_TYPES = (GoldBonus, FoodBonus, WaterBonus)

# Type alias for map coordinates
type Point = tuple[int, int]


class Map:
    """
    Represents the game map, handling terrain generation, item placement,
    and player movement.
    
    The map uses procedural generation to create varied terrain and
    manages the placement of items and players.
    """
    
    # Parameters for procedural terrain generation using Perlin noise
    scale = 0.1        # Scale of the noise
    octaves = 6        # Number of noise layers
    persistence = 0.6  # How much each octave contributes to overall shape
    lacunarity = 1.5   # How much detail is added at each octave

    def __init__(self, height: int, width: int, item_count: int, difficulty: str):
        """
        Initialize a new game map.
        
        Args:
            height (int): Height of the map in tiles
            width (int): Width of the map in tiles
            item_count (int): Number of items to place on the map
            difficulty (str): Game difficulty level
        """
        self.generate_terrain(height, width)
        self.players: dict[Point, Player] = {}  # Maps coordinates to players
        self.items: dict[Point, Item] = {}      # Maps coordinates to items
        self.populate_items(item_count)
        self.populate_traders(difficulty)
        self.listeners = []  # Event listeners for map events

    def draw(self) -> Panel:
        """
        Generate a visual representation of the map.
        
        Returns:
            Panel: Rich panel containing the rendered map
        """
        context = Text(justify="center")
        for i, row in enumerate(self.terrain):
            for j, square in enumerate(row):
                # Render players, items, or terrain in order of priority
                if (i, j) in self.players:
                    self.players[(i, j)].render(context)
                elif (i, j) in self.items:
                    self.items[(i, j)].render(context)
                else:
                    square.render(context)
            context.append("\n")
        context.remove_suffix("\n")
        return Panel(Padding(context, (1, 2)), title="World Map")

    def register_listener(self, listener: Listener):
        """
        Register an event listener for map events.
        
        Args:
            listener (Listener): The listener to register
        """
        self.listeners.append(listener)

    def notify(self, event: Event):
        """
        Notify all registered listeners of an event.
        
        Args:
            event (Event): The event to notify listeners about
        """
        for listener in self.listeners:
            listener.on_event(event)

    def add_player(self, location: Point, player: Player) -> None:
        """
        Add a player to the map at the specified location.
        
        Args:
            location (Point): The coordinates to place the player
            player (Player): The player to add
        """
        self.players[location] = player
        player.y = location[0]
        player.x = location[1]

    def add_item(self, location: Point, item: Item) -> None:
        """
        Add an item to the map at the specified location.
        
        Args:
            location (Point): The coordinates to place the item
            item (Item): The item to add
        """
        self.items[location] = item

    def populate_items(self, item_count) -> None:
        """
        Populate the map with a specified number of items.
        Items are distributed between food, water, and gold bonuses.
        
        Args:
            item_count (int): Total number of items to place
        """
        self.items.clear()

        # Calculate distribution of items
        total_parts = 5
        food_count = (item_count * 2) // total_parts
        water_count = (item_count * 2) // total_parts
        gold_count = item_count - food_count - water_count

        # Generate food items
        food_items = []
        for _ in range(food_count):
            amount = random.randrange(10, 50)
            food_item = FoodBonus(amount)
            food_items.append(food_item)

        # Generate water items
        water_items = []
        for _ in range(water_count):
            amount = random.randrange(10, 50)
            water_item = WaterBonus(amount)
            water_items.append(water_item)

        # Generate gold items
        gold_items = []
        for _ in range(gold_count):
            amount = random.randrange(10, 50)
            gold_item = GoldBonus(amount)
            gold_items.append(gold_item)

        # Place all items on the map
        all_items = food_items + water_items + gold_items
        for item in all_items:
            location: Point = (
                random.randrange(len(self.terrain)),
                random.randrange(len(self.terrain[0])),
            )
            # Ensure no two items are placed at the same location
            while location in self.items:
                location = (
                    random.randrange(len(self.terrain)),
                    random.randrange(len(self.terrain[0])),
                )
            self.items[location] = item

    def place_players(self, players: list[Player]) -> None:
        """
        Place players at random positions along the left edge of the map.
        
        Args:
            players (list[Player]): List of players to place
        """
        for player in players:
            location = (random.randrange(len(self.terrain)), 0)
            # Ensure no two players are placed at the same location
            while location in self.players:
                location = (random.randrange(len(self.terrain)), 0)
            self.players[location] = player
            player.y = location[0]
            player.x = location[1]

    def generate_terrain(self, height: int, width: int) -> None:
        """
        Generate terrain using Perlin noise for natural-looking landscapes.
        
        Args:
            height (int): Height of the map in tiles
            width (int): Width of the map in tiles
        """
        base = random.randrange(0, 500, 10)
        height_map = np.zeros((height, width))
        
        # Generate height map using Perlin noise
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

        # Normalize height values to 0-1 range
        height_map = (height_map - height_map.min()) / (
            height_map.max() - height_map.min()
        )

        # Convert height map to terrain types
        self.terrain: list[list[Terrain]] = [
            [self.get_terrain(height_map[y][x])() for x in range(width)]
            for y in range(height)
        ]

    def get_terrain(self, elevation):
        """
        Convert elevation value to appropriate terrain type.
        
        Args:
            elevation (float): Normalized elevation value (0-1)
            
        Returns:
            Terrain: The terrain type for the given elevation
        """
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

    def move_player_direction(self, player: Player, direction: Direction) -> None:
        """
        Move a player in the specified direction.
        
        Args:
            player (Player): The player to move
            direction (Direction): The direction to move in
        """
        self.notify(Event("moved", {"player": player, "direction": direction}))
        (dy, dx) = direction.value
        self.move_player(player, player.y + dy, player.x + dx)

    def move_player(self, player: Player, y: int, x: int) -> None:
        """
        Move a player to the specified coordinates.
        
        Args:
            player (Player): The player to move
            y (int): Target y-coordinate
            x (int): Target x-coordinate
        """
        # Validate coordinates
        assert y >= 0 and y < len(self.terrain) and x >= 0 and x < len(self.terrain[0])
        assert player in self.players.values()

        # Remove player from old position
        old_position = (player.y, player.x)
        assert old_position in self.players
        del self.players[old_position]

        # Place player at new position
        new_position = (y, x)
        player.y = y
        player.x = x
        self.players[new_position] = player

        # Apply terrain effects
        old_terrain = self.terrain[old_position[0]][old_position[1]]
        new_terrain = self.terrain[new_position[0]][new_position[1]]
        self.apply_terrain_effects(player, old_terrain, new_terrain)

        # Check for and apply item effects
        if (y, x) in self.items:
            self.apply_item_effects(player, new_position)

    def apply_terrain_effects(
        self, player: Player, old_terrain: Terrain, new_terrain: Terrain
    ) -> None:
        """
        Apply effects of terrain on player movement.
        
        Args:
            player (Player): The player to apply effects to
            old_terrain (Terrain): The terrain the player is leaving
            new_terrain (Terrain): The terrain the player is entering
        """
        new_terrain.apply_cost(player)
        if type(old_terrain) != type(new_terrain):
            self.notify(
                Event(
                    "terrain_entered",
                    {
                        "player": player,
                        "new_terrain": new_terrain,
                    },
                )
            )

    def apply_item_effects(self, player: Player, position: Point):
        """
        Apply effects of an item when a player picks it up.
        
        Args:
            player (Player): The player picking up the item
            position (Point): The position of the item
        """
        item = self.items[position]
        item.apply_effect(player)
        self.notify(Event("item_picked_up", {"player": player, "item": item}))
        if not isinstance(item, Trader):
            del self.items[position]  # Delete the item after it's picked up

    # Number of traders to place based on difficulty
    DIFFICULTY_TRADERS = {
        "Easy": 10,
        "Medium": 20,
        "Hard": 30,
    }

    def populate_traders(self, difficulty: str) -> None:
        """
        Populate the map with traders based on the difficulty level.
        
        Args:
            difficulty (str): The game difficulty level
        """
        trader_count = self.DIFFICULTY_TRADERS.get(difficulty, 3)
        map_height = len(self.terrain)
        map_width = len(self.terrain[0])

        for _ in range(trader_count):
            location = (
                random.randrange(map_height),
                random.randrange(map_width),
            )

            # Ensure traders don't overlap with items or players
            while location in self.items or location in self.players:
                location = (
                    random.randrange(map_height),
                    random.randrange(map_width),
                )

            
            self.items[location] = random.choice([FairTrader(), HagglingTrader()])
            
    
