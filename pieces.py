class Piece(object):

    available_tiles = [] # array to store coords of available movement tiles

    def __init__( self, **kwargs ):
        
        self.char = kwargs['char'] # this is used as the representation of the piece


        for key, value in kwargs.items():
            setattr( self, key, value )

    def __str__( self ):
        return "{}".format(self.char)

    def select( self ):
        pass

    def get_possible_moves( self, game ):
        return []
    

class Bishop(Piece):

    def __init__( self, **kwargs ):
        
        self.name = "Bishop"
        self.char = kwargs['char'] # this is used as the representation of the piece

        for key, value in kwargs.items():
            setattr( self, key, value )

class King(Piece):

    def __init__( self, **kwargs ):
        
        self.name = "King"
        self.char = kwargs['char'] # this is used as the representation of the piece

        for key, value in kwargs.items():
            setattr( self, key, value )


class Knight(Piece):

    def __init__( self, **kwargs ):
        
        self.name = "Knight"
        self.char = kwargs['char'] # this is used as the representation of the piece

        for key, value in kwargs.items():
            setattr( self, key, value )


class Pawn(Piece):

    def __init__( self, **kwargs ):

        self.name = "Pawn"
        self.is_first_move = True

        #self.pos = kwargs['pos'] # (x,y)
        for key, value in kwargs.items():
            setattr( self, key, value )

    def get_possible_moves( self, game ):
        # A for loop that checks for possible movement of this piece on the game board.
        # Returns array of coordinate tuples of legal tiles available for the piece to move into.

        total_available_moves = 1
    
        if self.is_first_move:
            total_available_moves = 2

        self.available_tiles = [] # array of (x,y) coordinate tuples

        # Check for opponent pieces that would need to be taken
        #for tile_x in [self.pos[0]-1, self.pos[0], self.pos[0]+1]:
            # Only check within board
         #   if tile_x >= 0 and tile_x <= 7:
                # Does the tile contain an opponent piece
          #      if game.is_opponent_at_tile( [ tile_x, self.pos[1]+1 ] ) == True:
                    # Add coordinates to available tiles
           #         self.available_tiles.append( [ tile_x, self.pos[1]+1 ] )

        # A pawn has a simple moveset. It can only advance in the y access unless taking an

        for tile in range(1, total_available_moves):
            print("PAWN MOVE TILE: {}".format(tile))

            if game.current_player == "lowercase":
                tile = -tile
            
            # Cannot move out of bounds of the board
            if self.pos[1] + tile <= 7 or self.pos[1] + tile >= 0:
                self.available_tiles.append( [ self.pos[0], self.pos[1] + tile ] )

        return self.available_tiles

    def select( self ):

        #available_tiles = self.possible_moves()

        # Now that we have taken a move with the tile set this first move to false so we cannot do more
        self.is_first_move = False



class Queen(Piece):

    def __init__( self, **kwargs ):
        
        self.name = "Queen"
        self.char = kwargs['char'] # this is used as the representation of the piece

        for key, value in kwargs.items():
            setattr( self, key, value )


class Rook(Piece):

    def __init__( self, **kwargs ):
        
        self.name = "Rook"
        self.char = kwargs['char'] # this is used as the representation of the piece

        for key, value in kwargs.items():
            setattr( self, key, value )
