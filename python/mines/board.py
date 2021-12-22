

from werkzeug.exceptions import BadRequest

from .entities import CreateGameRequest, UncoverTile
import dacite
import random
import pickle

import flask
from flask import request

class Tile:
    HIDDEN = "?"
    BOMB = "*"
    value = 0
    _is_a_bomb = False

    def __init__(self):
        self._is_a_bomb = False
        pass

    def display(self) -> str:
        return Tile.HIDDEN

    def set_mined(self):
        self._is_a_bomb = True
    
    def is_mined(self) -> bool:
        return self._is_a_bomb


    

class Board:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._tiles = [[Tile()] * width for _ in range(0, height + 1)]


        for idx, row in enumerate(self._tiles):
            width_idx = 0
            while (width_idx < width - 1):
                self._tiles[idx][width_idx] = Tile()
                width_idx += 1


    # debug function
    def show_content(self):
        for row in self._tiles:
            for tile in row:
                print(tile.is_mined(), end='')
            print("")

    def get_neighbour_value(self, pos_y, pos_x):
        if (self._tiles[pos_y] and self._tiles[pos_y][pos_x]):
            if (self._tiles[pos_y][pos_x].is_mined()):
                return 1
        return  0

    def get_value(self, pos_y, pos_x):

        print("pos y " + str(pos_y) + " pos x : " + str(pos_x))

        print(self._tiles[pos_y][pos_x])
        if (self._tiles[pos_y][pos_x].is_mined() is True):
            return "BOOM"
        else: 
            value = self.get_neighbour_value(pos_y - 1, pos_x - 1) + \
                    self.get_neighbour_value(pos_y - 1, pos_x) + \
                    self.get_neighbour_value(pos_y - 1, pos_x + 1) + \
                    self.get_neighbour_value(pos_y, pos_x - 1) + \
                    self.get_neighbour_value(pos_y, pos_x + 1) + \
                    self.get_neighbour_value(pos_y + 1, pos_x - 1) + \
                    self.get_neighbour_value(pos_y + 1, pos_x + 1) + \
                    self.get_neighbour_value(pos_y + 1, pos_x - 1)
        return value


    def init_board(self, nb_mines):

        nb_mines_left = nb_mines

        while nb_mines_left != 0: 
            random_width = random.randint(0, self._width - 1)
            random_height = random.randint(0, self._height - 1)
            if not (self._tiles[random_height][random_width].is_mined()):
                self._tiles[random_height][random_width].set_mined()
                nb_mines_left -= 1


    def debug(self):
        for row in self._tiles:
            for tile in row:
                print(tile.display(), end="")
            print("")


def save_board(board) -> int:
    game_id = 0

    with open('data/board_ids', 'rb') as board_ids:
        try:
            game_id = pickle.load(board_ids)
        except Exception:
            pass 

    with open('data/pickle_board_file_' + str(game_id + 1), 'wb') as pickle_board_file:
        pickle.dump(board, pickle_board_file)
    
    with open('data/board_ids', 'wb') as board_ids:
        pickle.dump(game_id + 1, board_ids)
    
    print("Store the board with id " + str(game_id + 1))
    print(board.show_content())
    return game_id + 1

def read_board(game_id):

    print("read the board with id " + str(game_id))
    with open('data/pickle_board_file_' + str(game_id), 'rb') as pickle_board_file:
        board = pickle.load(pickle_board_file)
    return board

def create_board():
    """Creates a new game and returns the id to it."""
    if not request.is_json:
        raise BadRequest("Request is not in json format")

    try:
        create_game_request = dacite.from_dict(CreateGameRequest, request.json)
    except dacite.DaciteError as e:
        raise BadRequest(f"Request is not a valid CreateGameRequest: {e}")

    board = Board(create_game_request.width, create_game_request.height)
    board.init_board(create_game_request.numberOfMines)
    game_id = save_board(board)
    # TODO - create a board, store it somehow in memory, return an identifier to the board
    # You can debug the board with a statement like
    # Board(create_game_request.width, create_game_request.height).debug()

    return flask.jsonify({"id": game_id})


def uncover_tile(game_id: int):

    if not request.is_json:
        raise BadRequest("Request is not in json format")

    try:
        uncover_tile = dacite.from_dict(UncoverTile, request.json)
    except dacite.DaciteError as e:
        raise BadRequest(f"Request is not a valid CreateGameRequest: {e}")
    
    board = read_board(game_id)

    value = board.get_value(uncover_tile.y, uncover_tile.x)

    # Return for the specified tile the value {number or BOMB}
    return flask.jsonify({"result": str(value)})
