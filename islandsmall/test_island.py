"""
To run tests:
pytest-3 connect4
"""

from collections import namedtuple
import textwrap
import numpy as np

from .IslandSmallGame import IslandSmallGame
from .IslandSmallLogic import Board, ENCODER_LAST, ENCODER_PIECE, ENCODER_PRESENT, ENCODER_STACKED

def test_simple_repr():
    g = IslandSmallGame()
    board = g.getInitBoard()
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
    assert b.has_legal_moves()

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

def test_exec_game_move():
    # Define the dimensions
    n = 3

    # Define the indices
    indices = (0, 2, 0, 1)
    action = np.ravel_multi_index(indices, (n, n, n, n))
    print(action)
    g = IslandSmallGame([1,2,3,6,5,4,7,8,0])
    (nextBoard, _) = g.getNextState(g.getInitBoard(), 1, action)
    assert "1 3 - 6 5 4 7 8 0" == g.stringRepresentationReadable(nextBoard)

def test_get_valid():
    g = IslandSmallGame([1,2,3,6,5,4,7,8,0])
    m = g.getValidMoves(g.getInitBoard(), 1)
    assert 9 == sum([i for i in m if i > 0]) # see TODO:
    assert 82 == len(m) # 81 is the product of our action space, plus our 1 extra noop move

def test_count_stacks():
    b = Board([1,2,3,6,5,4,7,8,0])
    assert 9 == b.count_stacks()
    b.execute_move((0, 2, 0, 1), 1)
    assert 8 == b.count_stacks()