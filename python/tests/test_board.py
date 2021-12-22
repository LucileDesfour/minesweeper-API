import pytest


from mines.board import Board


def test_sould_get_5_mines_on_board():
    board = Board(10, 10)
    board.init_board(5)

    count_mines = 0

    for row in board._tiles:
            for tile in row:
                if (tile.is_mined()):
                    count_mines += 1
    
    assert(count_mines == 5)

def test_sould_get_8_mines_on_board():
    board = Board(10, 20)
    board.init_board(8)

    count_mines = 0

    for row in board._tiles:
            for tile in row:
                if (tile.is_mined()):
                    count_mines += 1
    
    assert(count_mines == 8)

# Test discover tile 

def test_sould_explode_when_discovering_a_bomb():
    board = Board(10, 20)
    board.init_board(8)

    for idx_row, row in enumerate(board._tiles):
        for idx_tile, tile in enumerate(row):
            if (tile.is_mined()):
                value = board.get_value(idx_row, idx_tile)
                pass
    
    assert(value == "BOOM")
