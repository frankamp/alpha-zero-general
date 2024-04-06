import numpy as np

"""
Random and Human-ineracting players for the game of TicTacToe.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloPlayers by Surag Nair.

"""
class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanIslandSmallPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                # TODO: fixup for ravel/unravel quad tuple
                print(int(i/self.game.n), int(i%self.game.n))
        while True: 
            # Python 3.x
            # TODO: take a integer that will be looked up by value and a direction e.g. LRUD not two integers
            a = input()
            # Python 2.x 
            # a = raw_input()

            x,y,targetx,targety = [int(x) for x in a.split(' ')]
            a = self.game.n * x + y if x!= -1 else self.game.n ** 2 # TODO: fixup for ravel/unravel quad tuple
            if valid[a]:
                break
            else:
                print('Invalid')

        return a
