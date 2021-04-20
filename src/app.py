import random

default = ["Meh", "Boring", "What about it?", "Nothing special"]
present = 2021

def review(year):
    if not isinstance(year, int):
        raise TypeError("Expected int, received {x}".format(x = type(year).__name__))
    if year > present:
        raise ValueError("Can't review a year that has not happened yet (year > {x})".format(x = present))
    if year == 0:
        return "Jesus Christ what a year!"
    elif year == 42:
        return "A year worth living for"
    elif year == 1337:
        return ":sunglasses:"
    elif year == 1984:
        return "You never felt alone"
    elif year == 1987:
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    elif year == 2020:
        return "Sad year :("
    else:
        return default[random.randint(0, len(default) - 1)]