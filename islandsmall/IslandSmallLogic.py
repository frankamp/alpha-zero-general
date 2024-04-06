import numpy as np

NUM_ENCODERS = 4
ENCODER_PRESENT = 0
ENCODER_PIECE = 1
ENCODER_STACKED = 2
ENCODER_LAST = 3
EATS_BELOW = 3
'''
Board class for the game of Food chain island small (modified food chain island).
Default board size is 3x3.
Board data:
  first dim is row , 2nd is col:
     pieces[0][0] is the top left square,
     pieces[2][0] is the bottom left square,
Squares are stored and manipulated as (x,y) tuples.
The third dimension is an array of dimension NUM_ENCODERS, containing the ENCODER values in positions above
'''
# from bkcharts.attributes import color
class Board():
    
    # list of all for adjacent directions on the board, as (x,y) offsets
    __directions = [(1,0),(0,-1),(-1,0),(0,1)]

    def __init__(self, seed, pieces=None):
        "Set up initial board configuration."
        self.n = 3
        if (pieces is not None):
            self.pieces = pieces
        else:
            self.pieces = np.zeros((self.n, self.n, NUM_ENCODERS))
            self.pieces[:, :, ENCODER_PRESENT] = np.array([1] * self.n * self.n).reshape(self.n, self.n) # all present
            self.pieces[:, :, ENCODER_PIECE] = np.array(seed).reshape(self.n, self.n) # which piece


    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def get_legal_moves(self, color, shortcircuit=False):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        @param color not used and came from previous version.        
        """
        moves = set()  # stores the legal moves.
        upperx = self.pieces.shape[0] - 1
        uppery = self.pieces.shape[1] - 1
        #print("")
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y][ENCODER_PRESENT] == 1:
                    # check adjacencies according to rules
                    for (deltax, deltay) in self.__directions:
                        # out of bounds check
                        if x + deltax < 0 or y + deltay < 0 or (x + deltax) > upperx or (y + deltay) > uppery:
                            continue
                        # if the adjacent piece is present
                        # and edible
                        #print(f"consider move from {x} {y} in dir {deltax} {x + deltax} {deltay} {y + deltay} {self.pieces.shape[1]}")
                        if self[x + deltax][y + deltay][ENCODER_PRESENT] == 1 \
                            and 1 <= \
                                self[x][y][ENCODER_PIECE] - self[x + deltax][y + deltay][ENCODER_PIECE] \
                                <= EATS_BELOW:
                            newmove = (x, y, x + deltax, y + deltay)
                            moves.add(newmove)
                            if shortcircuit:
                                return moves
                            #print("found move")
        return list(moves)

    def has_legal_moves(self):
        moves = self.get_legal_moves(1, shortcircuit=True)
        return len(moves) > 0
    
    def count_stacks(self):
        return np.sum(self.pieces[:, :, ENCODER_PRESENT])
    
    def is_win(self, color):
        """Check whether the given player has collected a triplet in any direction; 
        @param color (1=white,-1=black)
        """
        # this may not be used at all, we dont call it from game, the logic and scoring
        # are handled there because the game is not 'winnable' adversarially, we have to let both
        # agents play it out entirely
        
        # for island, there is no win condition (game ending) unless there are no more legal moves. If there are legal moves, the game is not won (or lost)
        if self.has_legal_moves():
            return False
        else:
            return True

    def execute_move(self, move, color):
        """Perform the given move on the board; 
        color gives the color pf the piece to play (1=white,-1=black)
        """

        (x, y, targetx, targety) = move
        # TODO: modify to 'eat' and also change the rules depending on who did the eating if there is a rule change
        # also check for whether this method returns the next user, it might in which case its one of the places we
        # can hook to let one player 'play out' the game, and then the other once there are no more valid moves.
        # in that case there will only be one 'is_win' and we can score and reset the game when the has_valid_moves runs out for the first
        # Add the piece to the empty square.
        # TODO: can illegal moves be passed to me? do i have to validate?
        self[targetx][targety] = self[x][y]
        self.pieces[x, y, :] = 0 # clear vacated
        self[targetx][targety][ENCODER_STACKED] = 1 # mark target as stacked
        self.pieces[:, :, ENCODER_LAST] = 0 # clear last from every location
        self[targetx][targety][ENCODER_LAST] = 1 # set last on target


