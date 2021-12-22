# minesweeper-API

## Rules of the game

### Objective
Minesweeper is a game which is played on a board which is made up of tiles.
Each tile can either contain a mine or not.
The goal of the game is to discover the location of all mines.

### How to play
In the beginning, the contents of all squares are hidden.

![Board at the beginning](./beginning.png)

**Figure 1** The board at the beginning of the game

The player can uncover the contents of one tile at a time.
The following things can happen depending on the contents of the tile.
1. The tile contains a mine. This ends the game and the player loses.
2. The tile is next to a mine:
   The tile is uncovered and will show the number of adjacent mines (i.e., those of the surrounding 8 tiles)
3. The tile is not a mine and not adjacent to a mine. 
   The tile will be shown as an empty tile, and all adjacent tiles
   will be uncovered too. (For these tiles, the rules are applied again.)
4. The tile is the last tile which is not a mine. The game ends and the player wins.


![](./adjacent.png)

**Figure 2** If the field which is marked with an X is uncovered, all adjacent
tiles are uncovered too. (And their adjacent fields too.)

![](./complete.png)

**Figure 3** A complete board of a solved game.
You can see how the numbers in the tiles  correspond to the number of adjacent mines.

## Your task
Your task is to implement a REST API for playing minesweeper.

The REST API will provide the data to a frontend, and it will not care about
how it is displayed. However, the REST API should assume that the frontend is not secure,
and it should not send sensible information like the location of the mines.

Use the provided skeleton as a starting point (but feel free to change 
anything that you think is not fitting).

Important: You will not be expected to complete the whole task.
We want to use this exercise to learn how you work (for details see below).
