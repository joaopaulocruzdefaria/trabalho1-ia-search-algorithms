import math
from typing import Tuple

Pos = Tuple[int, int]


def manhattan(a: Pos, b: Pos) -> float:
    """Implemente a distância Manhattan entre duas posições."""
    distance = abs(a[0]-b[0]) + abs(a[1]-b[1])
    return float(distance)


def euclidean(a: Pos, b: Pos) -> float:
    """Implemente a distância Euclidiana entre duas posições."""
    distance = math.sqrt(pow(a[0]-b[0],2)+pow(a[1]-b[1],2))
    return float(distance)
