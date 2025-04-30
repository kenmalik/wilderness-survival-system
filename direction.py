from enum import Enum


class Direction(Enum):
    NORTH = (-1, 0)
    NORTHEAST = (-1, 1)
    EAST = (0, 1)
    SOUTHEAST = (1, 1)
    SOUTH = (1, 0)
    SOUTHWEST = (1, -1)
    WEST = (0, -1)
    NORTHWEST = (-1, -1)


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
