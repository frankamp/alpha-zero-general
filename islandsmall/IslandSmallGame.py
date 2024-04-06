from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .IslandSmallLogic import Board, NUM_ENCODERS
import numpy as np

"""
A simplified version of food chain island logic/game, prepped for AZG
"""
class IslandSmallGame(Game):
    white_stacks = 0
    n = 3
    seed = []

    def __init__(self, seed=[0,1,2,3,4,5,6,7,8]):
        self.seed = seed

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.seed)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n, NUM_ENCODERS)

    def getActionSize(self):
        # return number of actions, actions in my game are signified by x,y,targetx,targety tuples, where those are positive integers bounded by the board
        return np.prod((self.n, self.n, self.n, self.n)) + 1 # the last action is a special signifier of no more valid moves, or do nothing (i think)

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        # TODO: find caller and figure out what the structure of action is, need better contract
        if action == np.prod((self.n, self.n, self.n, self.n)): # this must be e.g. something akin to there are no moves for me, your turn?
            print("special top action, short circuit condition")
            input("return to continue")
            return (board, -player)
        b = Board(seed=None, pieces=np.copy(board))
        (x, y, targetx, targety) = np.unravel_index(action, (self.n, self.n, self.n, self.n))
        move = (x, y, targetx, targety)
        b.execute_move(move, player)
        next_player = player
        if player == 1 and not b.has_legal_moves():
            self.white_stacks = b.count_stacks()
            b = Board(seed=self.seed) # wipe the board, reset it to the seed
            next_player = -player
        return (b.pieces, next_player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        # TODO: this appears to be inefficient because getValidMoves should be read only
        # there should be no cause to e.g. copy the board, we should be able to jsut use it.
        # it also looks like maybe the action size of the game is one larger than the vlaid moves on the board
        # correpsonding to 'no more legal moves left for me'. This might be triggering e.g. getNextState if action== 
        valids = [0]*self.getActionSize()
        b = Board(seed=None, pieces=np.copy(board))
        legalMoves =  b.get_legal_moves(player)
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        for indices in legalMoves:
            valids[np.ravel_multi_index(indices, (self.n, self.n, self.n, self.n))] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(seed=None, pieces=np.copy(board))
        # if player is white, there is no end to the game, even with no legal moves,
        # because we are going to reset it for the purposes of reusing it
        if player == 1:
            return 0
        if b.has_legal_moves():
            return 0
        assert self.white_stacks > 0
        black_stacks = b.count_stacks()
        white_stacks = self.white_stacks
        self.white_stacks = 0 # I am not sure if the game instance is reused, so we need to reset it
        if black_stacks > white_stacks:
            return -1 # black won
        elif black_stacks < white_stacks:
            return 1
        else:
            return 1e-4 # special e.g. little value value for draw

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return board # we dont do inversion because we plan to play both players back to back

    def getSymmetries(self, board, pi):
        pi_board = np.reshape(pi[:-1], (self.n, self.n, self.n, self.n))
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

    def display_with_scores(self, board, player):
        print("")
        if player == -1:
            print(f"Black turn, white got: {self.white_stacks}")
        else:
            print("White turn")
        self.display(board)
    
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
