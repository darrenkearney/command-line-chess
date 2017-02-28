class Piece(object):
    def __init__( self, **kwargs ):
        
        self.char = kwargs['char'] # this is used as the representation of the piece

        for key, value in kwargs.items():
            setattr( self, key, value )

    def __str__( self ):
        return "{}".format(self.char)

class Bishop(Piece):
    def __init__( self, **kwargs ):
        
        self.char = kwargs['char'] # this is used as the representation of the piece

        for key, value in kwargs.items():
            setattr( self, key, value )

class King(Piece):
    pass

class Knight(Piece):
    pass

class Pawn(Piece):

    def __init__( self, **kwargs ):

        self.is_first_move = True

        #self.pos = kwargs['pos'] # (x,y)
        for key, value in kwargs.items():
            setattr( self, key, value )

    def possible_moves( self, game ):
        # A for loop that checks for possible movement of this piece on the game board.
        # Returns array of coordinate tuples of legal tiles available for the piece to move into.

        total_available_moves = 1
    
        if self.is_first_move:
            total_available_moves = 2

        self.available_tiles = [] # array of (x,y) coordinate tuples

        # Check for opponent pieces that would need to be taken
        for tile_x in [self.pos[0]-1, self.pos[0], self.pos[0]+1]:
            # Only check within board
            if tile_x >= 0 and tile_x <= 8:
                # Does the tile contain an opponent piece
                if game.is_opponent_at_tile((self.pos[1]+1)(tile_x)) == True:
                    # Add coordinates to available tiles
                    self.available_tiles.append((self.pos[1]+1)(tile_x))

        # A pawn has a simple moveset. It can only advance in the y access.
        for tile in total_available_moves:
            
            if side == "black":
                tile = -tile
            
            # Cannot move out of bounds of the board
            if self.pos[1] + tile <= 8 or self.pos[1] + tile >= 0:
                self.available_tiles.append( ( self.pos[0], self.pos[1] + tile ) )

    def move( self ):

        available_tiles = self.possible_moves()

        # Now that we have taken a move with the tile set this first move to false so we cannot do more
        self.is_first_move = False



class Queen(Piece):
    pass

class Rook(Piece):

    def __init__( self, **kwargs ):
        
        #self.char = kwargs['char'] # this is used as the representation of the piece

        for key, value in kwargs.items():
            setattr( self, key, value )
