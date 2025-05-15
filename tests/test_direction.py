from wss.direction import Direction, angle_to_direction

import math


def test_angle_to_direction():
    """
    Test the angle_to_direction function to ensure it correctly maps angles
    to the corresponding Direction enum values.
    """

    test_cases = [
        (0, Direction.EAST),
        (math.pi / 4, Direction.NORTHEAST),
        (math.pi / 2, Direction.NORTH),
        (3 * math.pi / 4, Direction.NORTHWEST),
        (math.pi, Direction.WEST),
        (-math.pi, Direction.WEST),
        (-3 * math.pi / 4, Direction.SOUTHWEST),
        (-math.pi / 2, Direction.SOUTH),
        (-math.pi / 4, Direction.SOUTHEAST),
    ]

    for angle, expected_direction in test_cases:
        result = angle_to_direction(angle)
        assert (
            result == expected_direction
        ), f"Expected {expected_direction}, but got {result} for angle {angle}"
