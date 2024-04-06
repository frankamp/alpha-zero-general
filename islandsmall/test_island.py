"""
To run tests:
pytest-3 connect4
"""

from collections import namedtuple
import textwrap
import numpy as np

from .IslandSmallGame import IslandSmallGame
from .IslandSmallLogic import Board, ENCODER_LAST, ENCODER_PIECE, ENCODER_PRESENT, ENCODER_STACKED
# # Tuple of (Board, Player, Game) to simplify testing.
# BPGTuple = namedtuple('BPGTuple', 'board player game')


# def init_board_from_moves(moves, height=None, width=None):
#     """Returns a BPGTuple based on series of specified moved."""
#     game = Connect4Game(height=height, width=width)
#     board, player = game.getInitBoard(), 1
#     for move in moves:
#         board, player = game.getNextState(board, player, move)
#     return BPGTuple(board, player, game)


# def init_board_from_array(board, player):
#     """Returns a BPGTuple based on series of specified moved."""
#     game = Connect4Game(height=len(board), width=len(board[0]))
#     return BPGTuple(board, player, game)


def test_simple_repr():
    g = IslandSmallGame()
    board = g.getInitBoard()
    # this is display... which isnt the string repr hah
    # expected = textwrap.dedent("""\
    #        0 1 2  
    #       --------
    #     0 |- - - |
    #     1 |- - - |
    #     2 |- - - |
    #       --------""")
    print(board.shape)
    print(g.stringRepresentationReadable(board))
    assert '0 1 2 3 4 5 6 7 8' == g.stringRepresentationReadable(board)

def test_seeded_repr():
    g = IslandSmallGame([1,2,3,6,5,4,7,8,0])
    board = g.getInitBoard()
    print(board.shape)
    print(g.stringRepresentationReadable(board))
    assert '1 2 3 6 5 4 7 8 0' == g.stringRepresentationReadable(board)

def test_display():
    g = IslandSmallGame([1,2,3,6,5,4,7,8,0])
    board = g.getInitBoard()
    g.display(board)


def test_legal_move():
    b = Board([1,2,3,6,5,4,7,8,0])
    moves = b.get_legal_moves(1)
    assert [(0, 2, 0, 1), (1, 0, 1, 1), (0, 1, 0, 0), (1, 1, 1, 2), (2, 1, 2, 0), (1, 1, 0, 1), (1, 2, 0, 2), (2, 1, 1, 1), (2, 0, 1, 0)] == moves
    
def test_exec_move():
    g = IslandSmallGame([1,2,3,6,5,4,7,8,0])
    b = Board([1,2,3,6,5,4,7,8,0])
    assert 9 == len(b.get_legal_moves(1))
    b.execute_move((0, 2, 0, 1), 1)
    g.display(b.pieces)
    assert "1 3 - 6 5 4 7 8 0" == g.stringRepresentationReadable(b.pieces)
    assert 7 == len(b.get_legal_moves(1))
    assert b.pieces[0][1][ENCODER_STACKED] == 1
    assert b.pieces[0][1][ENCODER_LAST] == 1
    b.execute_move((1, 0, 1, 1), 1)
    g.display(b.pieces)
    assert 5 == len(b.get_legal_moves(1))
    assert b.pieces[0][1][ENCODER_STACKED] == 1
    assert b.pieces[0][1][ENCODER_LAST] == 0
    assert b.pieces[1][1][ENCODER_LAST] == 1