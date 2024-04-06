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

    def __init__(self, seed):
        "Set up initial board configuration."

        self.n = 3
        # TODO: create a seeded board
        # Create the empty board array.
        self.pieces = np.zeros((self.n, self.n, NUM_ENCODERS))
        self.pieces[:, :, ENCODER_PRESENT] = np.array([1] * self.n * self.n).reshape(self.n, self.n) # all present
        self.pieces[:, :, ENCODER_PIECE] = np.array(seed).reshape(self.n, self.n) # which piece


    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def get_legal_moves(self, color):
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
                                self[x][y][ENCODER_PIECE] - self[x+deltax][y+deltay][ENCODER_PIECE] \
                                <= EATS_BELOW:
                            newmove = (x, y, x + deltax, y + deltay)
                            moves.add(newmove)
                            #print("found move")
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


