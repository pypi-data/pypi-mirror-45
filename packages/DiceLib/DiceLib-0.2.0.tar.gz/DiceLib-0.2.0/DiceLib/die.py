"""Defines the Die class."""

from random import randint

from DiceLib.rolls import Rolls


class Die:
    """Emulate the functionality of a single die.

    Attributes
    ----------
    faces : int
        The number of sides, or faces, the die possesses.

    """

    def __init__(self, faces):
        """Initialize a new Die object."""
        self.faces = faces

    def roll(self, count=1):
        """Roll the specified number of dice."""
        return Rolls([randint(1, self.faces) for _ in range(count)])
