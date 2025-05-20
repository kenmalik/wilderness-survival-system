"""
Player module for the Wilderness Survival System.
This module defines the Player class which represents a player in the game,
including their stats, movement, and decision-making capabilities.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from rich.text import Text

from wss_py.text_renderable import TextRenderable
from wss_py.direction import Direction
from wss_py.vision import Vision
from wss_py.brain import Brain

import logging


if TYPE_CHECKING:
    from wss_py.map import Map


logger = logging.getLogger(__name__)


class Player(TextRenderable):
    """
    Represents a player in the wilderness survival game.

    Each player has:
    - Resource stats (strength, water, food, gold)
    - Position and orientation
    - Vision system for perceiving the environment
    - Brain for decision making
    """

    # Maximum values for player resources
    MAX_STRENGTH = 100
    MAX_WATER = 100
    MAX_FOOD = 100

    def __init__(self, icon: str, map: Map, vision: Vision):
        """
        Initialize a new player.

        Args:
            icon (str): Character used to represent the player on the map
            map (Map): The game map instance
            vision (Vision): The player's vision system
            brain_type (str): Type of AI brain to use ("food", "water", or "gold")
        """
        # Initialize resources at 1/3 of maximum
        self.current_strength = self.MAX_STRENGTH // 3
        self.current_water = self.MAX_WATER // 3
        self.current_food = self.MAX_FOOD // 3
        self.current_gold = 0

        # Initial position (will be set by map)
        self.x = -1
        self.y = -1

        self.icon = icon
        self.dead = False

        self.map = map
        self.vision = vision

        # Initialize the appropriate brain based on brain_type
        self.brain = None

        # Player starts facing east
        self.orientation = Direction.EAST

    def set_brain(self, brain: Brain) -> None:
        """
        Set the brain for the player.

        Args:
            brain (Brain): The brain instance to be assigned to the player
        """
        self.brain = brain

    def print_stats(self) -> Text:
        """
        Generate a formatted text representation of the player's stats.

        Returns:
            Text: Rich text object containing player statistics
        """
        stats = Text()

        # Color stats red if they're critically low (≤ 10)
        strength_style = "red" if self.current_strength <= 10 else "default"
        stats.append(f"Strength: {self.current_strength}\n", style=strength_style)

        water_style = "red" if self.current_water <= 10 else "default"
        stats.append(f"Water: {self.current_water}\n", style=water_style)

        food_style = "red" if self.current_food <= 10 else "default"
        stats.append(f"Food: {self.current_food}\n", style=food_style)

        stats.append(f"Gold: {self.current_gold}\n")

        stats.append(f"\nLocation: ({self.x}, {len(self.map.terrain) - self.y})\n")

        progress = self.x / len(self.map.terrain[0])
        stats.append(f"Eastward Progress: {progress:.1%}\n")

        return stats

    def render(self, context: Text):
        """
        Render the player's icon on the map.

        Args:
            context (Text): Rich text object to append the player's icon to
        """
        context.append(
            self.icon,
            style=(
                "bold white on indian_red"
                if not self.dead
                else "bold black on bright_black"
            ),
        )

    def move_direction(self, direction: Direction):
        """
        Move the player in the specified direction.

        Args:
            direction (Direction): The direction to move in
        """
        # Update orientation based on movement direction
        if direction == Direction.NORTH:
            self.orientation = Direction.NORTH
        elif direction == Direction.SOUTH:
            self.orientation = Direction.SOUTH
        elif (
            direction == Direction.EAST
            or direction == Direction.NORTHEAST
            or direction == Direction.SOUTHEAST
        ):
            self.orientation = Direction.EAST
        elif (
            direction == Direction.WEST
            or direction == Direction.NORTHWEST
            or direction == Direction.SOUTHWEST
        ):
            self.orientation = Direction.WEST

        self.map.move_player_direction(self, direction)

    def rest(self) -> None:
        self.current_strength = min(self.current_strength + 5, self.MAX_STRENGTH)
        self.map.apply_terrain_effects(
            self,
            self.map.terrain[self.y][self.x],
            self.map.terrain[self.y][self.x],
        )

    def _move_is_valid(self, direction: Direction) -> bool:
        """
        Check if a move in the given direction is valid.

        Args:
            direction (Direction): The direction to check

        Returns:
            bool: True if the move is valid, False otherwise
        """
        new_y = self.y + direction.value[0]
        new_x = self.x + direction.value[1]

        # Check if the target position is occupied by another player
        if self.map.players.get((new_y, new_x)) is not None:
            logger.debug(
                f"Invalid move for player {self.icon} to occupied position ({new_y}, {new_x})"
            )
            return False

        # Check if the target position is within map bounds
        if 0 <= new_y < len(self.map.terrain) and 0 <= new_x < len(self.map.terrain[0]):
            return True
        else:
            logger.debug(
                f"Invalid move for player {self.icon} out of bounds to ({new_y}, {new_x})"
            )
            return False

    def update(self) -> None:
        """
        Update player state for one turn.
        Calculates and executes the next move based on the player's brain.
        """

        assert self.brain is not None, "Brain must be set before updating player"

        action = self.brain.choose_action()

        match action.type:
            case "rest":
                self.rest()
            case "move":
                direction = action.data["direction"]

                # If the preferred move is invalid, try other directions
                other_directions = {
                    direction for direction in Direction if direction != action
                }
                if not self._move_is_valid(direction):
                    valid_move_found = False
                    for alternative in other_directions:
                        if self._move_is_valid(direction):
                            valid_move_found = True
                            direction = alternative
                            break
                    if not valid_move_found:
                        logger.debug(
                            f"Player {self.icon} cannot move in any direction. Resting."
                        )
                        self.rest()
                        return

                self.move_direction(direction)
            case _:
                raise ValueError(f"Unknown action type: {action.type}")

    def __repr__(self) -> str:
        """
        String representation of the player.

        Returns:
            str: Player object information
        """
        return f"Player(icon={self.icon}, strength={self.current_strength}, water={self.current_water}, food={self.current_food}, gold={self.current_gold}, position=({self.y}, {self.x}), dead={self.dead})"
