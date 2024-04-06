from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .IslandSmallLogic import Board
import numpy as np

"""
Game class implementation for the game of TicTacToe.
Based on the OthelloGame then getGameEnded() was adapted to new rules.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloGame by Surag Nair.
"""
class IslandSmallGame(Game):

    n = 3

    def __init__(self, seed=[0,1,2,3,4,5,6,7,8]):
        self.seed = seed

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.seed)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n + 1 # the last item is a special signifier of no more valid moves

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        # TODO: find caller and figure out what the structure of action is, need better contract
        if action == self.n*self.n: # this must be e.g. something akin to there are no moves for me, your turn?
            return (board, -player)
        b = Board(seed=None, pieces=np.copy(board))
        (x, y, targetx, targety) = np.unravel_index(action, [self.n, self.n, self.n, self.n])
        move = (x, y, targetx, targety)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        # TODO: this appears to be inefficient because getValidMoves should be read only
        # there should be no cause to e.g. copy the board, we should be able to jsut use it.
        # it also looks like maybe the action size of the game is one larger than the vlaid moves on the board
        # correpsonding to 'no more legal moves left for me'. This might be triggering e.g. getNextState if action== 
        valids = [0]*self.getActionSize()
        b = Board(seed=None, pieces=np.copy(board))
        legalMoves =  b.get_legal_moves(player)
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)
        for x, y, targetx, targety in legalMoves:
            valids[self.n*x+y]=1 # TODO: this is not the right encoding scheme, we need to use the one accepted by getNextState
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(seed=None, pieces=np.copy(board))

        if b.is_win(player):
            return 1
        if b.is_win(-player):
            return -1
        if b.has_legal_moves():
            return 0
        # draw has a very little value 
        return 1e-4

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return board # we dont do inversion because we plan to play both players back to back

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()
    
    def formatSquare(self, square):
        if square[0]:
            return str(int(square[1]))
        else:
            return "-"

    def stringRepresentationReadable(self, board):
        board_s = " ".join(self.formatSquare(square) for row in board for square in row)
        return board_s

    @staticmethod
    def display(board):
        n = board.shape[0]
        print("")
        print("   ", end="")
        for y in range(n):
            print (y,"", end="")
        print("")
        print("  ", end="")
        for _ in range(n):
            print ("-", end="-")
        print("--")
        for y in range(n):
            print(y, "|",end="")    # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                if piece[0]:
                    print(str(int(piece[1])) + " ",end="")
                else:
                    if x==n:
                        print("-",end="")
                    else:
                        print("- ",end="")
            print("|")

        print("  ", end="")
        for _ in range(n):
            print ("-", end="-")
        print("--")
