"""
To run tests:
pytest-3 connect4
"""

from collections import namedtuple
import textwrap
import numpy as np

from .IslandSmallGame import IslandSmallGame

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