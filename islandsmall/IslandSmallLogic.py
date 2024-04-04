import numpy as np
'''
Board class for the game of Food chain island small (modified food chain island).
Default board size is 3x3.
Board data:
  1=white(O), -1=black(X), 0=empty
  first dim is column , 2nd is row:
     pieces[0][0] is the top left square,
     pieces[2][0] is the bottom left square,
Squares are stored and manipulated as (x,y) tuples.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the board for the game of Othello by Eric P. Nichols.

'''
# from bkcharts.attributes import color
class Board():
    NUM_ENCODERS = 3
    ENCODERS_MAP = {'present': 0, 'piece': 1, 'stacked': 2}
    EATS_BELOW = 3
    # list of all 8 directions on the board, as (x,y) offsets
    #__directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self, seed):
        "Set up initial board configuration."

        self.n = 3
        # TODO: create a seeded board
        # Create the empty board array.
        self.pieces = np.zeros((self.n, self.n, self.NUM_ENCODERS))
        self.pieces[:, :, 0] = np.array([1] * self.n * self.n).reshape(self.n, self.n) # all present
        self.pieces[:, :, 1] = np.array(seed).reshape(self.n, self.n) # which piece


    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        @param color not used and came from previous version.        
        """
        moves = set()  # stores the legal moves.
        # TODO: change to get all NON empty squares, enumerating adjacent squares that are n-EATS_BELOW
        # Get all the empty squares (color==0)
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==0:
                    newmove = (x,y)
                    moves.add(newmove)
        return list(moves)

    def has_legal_moves(self):
        # TODO: reimplement to call get_legal_moves with a short circuit flag
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==0:
                    return True
        return False
    
    def is_win(self, color):
        """Check whether the given player has collected a triplet in any direction; 
        @param color (1=white,-1=black)
        """
        # TODO: this might be involved in your multi user (user1 plays the full game, user2 plays the full game, then we determine 'winner' or tie)
        # because of that we might need to know whether we have to defer, or the score of the previous player depending on the level of abstraction
        # that the second of the paired games runs. i.e. maybe we can arrange for is_win to be called twice? but then we need to interpret
        # if it is called once after both players get a chance, then we need to lookup the score for the first player (or carry it through via some other means)
        # if we go side-by-side we wont have this problem i think? as long as both players get called for is_win (because they can both win in that case it is a tie)
        win = self.n
        # check y-strips
        for y in range(self.n):
            count = 0
            for x in range(self.n):
                if self[x][y]==color:
                    count += 1
            if count==win:
                return True
        # check x-strips
        for x in range(self.n):
            count = 0
            for y in range(self.n):
                if self[x][y]==color:
                    count += 1
            if count==win:
                return True
        # check two diagonal strips
        count = 0
        for d in range(self.n):
            if self[d][d]==color:
                count += 1
        if count==win:
            return True
        count = 0
        for d in range(self.n):
            if self[d][self.n-d-1]==color:
                count += 1
        if count==win:
            return True
        
        return False

    def execute_move(self, move, color):
        """Perform the given move on the board; 
        color gives the color pf the piece to play (1=white,-1=black)
        """

        (x,y) = move
        # TODO: modify to 'eat' and also change the rules depending on who did the eating if there is a rule change
        # also check for whether this method returns the next user, it might in which case its one of the places we
        # can hook to let one player 'play out' the game, and then the other once there are no more valid moves.
        # in that case there will only be one 'is_win' and we can score and reset the game when the has_valid_moves runs out for the first
        # Add the piece to the empty square.
        assert self[x][y] == 0
        self[x][y] = color

