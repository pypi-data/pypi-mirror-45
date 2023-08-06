"""Defines the Rolls class."""

from DiceLib.exceptions import DropError


class Rolls:
    """Represent a series of rolls.

    This class will also provide simple functions for manipulating rolls.

    Attributes
    ----------
    rolls : list
        A list of all the rolls in the set.
    total : int
        The sum of all rolls in the set.
    count : int
        The number of rolls in the set.
    highest : int
        The highest roll in the set.
    lowest : int
        The lowest roll in the set.

    """

    def __init__(self, rolls):
        self.rolls = rolls
        self.total = sum(self.rolls)
        self.count = len(self.rolls)
        try:
            self.highest = max(rolls)
        except ValueError:
            self.highest = 0
        try:
            self.lowest = min(rolls)
        except ValueError:
            self.lowest = 0

    def __int__(self):
        return self.total

    def __len__(self):
        return self.count

    def __iter__(self):
        for value in self.rolls:
            yield value

    def __getitem__(self, key):
        if type(key) == int:
            return Rolls([self.rolls[key]])
        return Rolls(self.rolls[key])

    def __setitem__(self, key, value):
        if type(key) == int:
            self.rolls[key] = int(value)
        self.rolls[key] = value
        self.total = sum(self.rolls)

    def __lt__(self, target):
        return self.total < target

    def __le__(self, target):
        return self.total <= target

    def __eq__(self, target):
        return self.total == target

    def __ne__(self, target):
        return self.total != target

    def __gt__(self, target):
        return self.total > target

    def __ge__(self, target):
        return self.total >= target

    def __repr__(self):
        return str(self.rolls)

    def drop_lowest(self, count=1):
        return self._drop(count, min)

    def drop_highest(self, count=1):
        return self._drop(count, max)

    def _drop(self, count, sorting_function):
        if count > self.count:
            raise DropError("Cannot drop more dice than were rolled.")
        if count < 0:
            raise DropError("Cannot drop a negative number of dice.")
        new_rolls = self.rolls.copy()
        for _ in range(count):
            new_rolls.pop(new_rolls.index(sorting_function(new_rolls)))
        return Rolls(new_rolls)
