from dataclasses import dataclass


@dataclass
class CreateGameRequest:
    width: int
    height: int
    numberOfMines: int


@dataclass
class UncoverTile:
    x: int
    y: int
