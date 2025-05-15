"""
Direction module for the Wilderness Survival System.
This module defines the possible movement directions in the game
and provides string representations for each direction.
"""

from enum import Enum


class Direction(Enum):
    """
    Enumeration of possible movement directions in the game.
    Each direction is represented by a tuple of (y, x) coordinates
    that indicate the relative movement from the current position.
    
    The coordinates follow a standard 2D grid system where:
    - First value (y): -1 for up, 0 for same level, 1 for down
    - Second value (x): -1 for left, 0 for same level, 1 for right
    """
    NORTH = (-1, 0)      # Move up
    NORTHEAST = (-1, 1)  # Move up and right
    EAST = (0, 1)        # Move right
    SOUTHEAST = (1, 1)   # Move down and right
    SOUTH = (1, 0)       # Move down
    SOUTHWEST = (1, -1)  # Move down and left
    WEST = (0, -1)       # Move left
    NORTHWEST = (-1, -1) # Move up and left


# Dictionary mapping Direction enum values to their string representations
# Used for displaying direction names in messages and UI
direction_strings = {
    Direction.NORTH: "North",
    Direction.NORTHEAST: "Northeast",
    Direction.EAST: "East",
    Direction.SOUTHEAST: "Southeast",
    Direction.SOUTH: "South",
    Direction.SOUTHWEST: "Southwest",
    Direction.WEST: "West",
    Direction.NORTHWEST: "Northwest",
}
