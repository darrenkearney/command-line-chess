class Piece(object):

    available_tiles = [] # array to store coords of available movement tiles

    def __init__( self, **kwargs ):
        
        self.char = kwargs['char'] # this is used as the representation of the piece


        for key, value in kwargs.items():
            setattr( self, key, value )

    def __str__( self ):
        return "{}".format(self.char)

    def select( self, board = [[]], current_player = ""):
        pass

    def get_possible_moves( self, board = [[]], current_player = "" ):
        return []

    def is_opponent_at_tile( self, board_tile ):
        # Returns True if opponent player has a piece on the tile
        
        if type(board_tile) == str:
            return False

        if self.side == board_tile.side:
            return False
        
        return True

    def is_piece_at_tile( self, board_tile ):
        # Returns True if opponent player has a piece on the tile
        
        if type(board_tile) == str:
            return False

        if board_tile.side in ["uppercase", "lowercase"]:
            return True

        return False

    def moved( self ):
        pass
    

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

    def get_possible_moves( self, board, current_player):
        # The games board is board[y][x] but every reference to a position is (x,y)
        # A for loop that checks for possible movement of this piece on the game board.
        # Returns array of coordinate tuples of legal tiles available for the piece to move into.
        #
        # A pawn has a simple moveset. It can only advance in the y access unless taking a piece in adjacent lane
        #

        self.available_tiles = [] # array of (x,y) coordinate tuples


        total_available_moves = 1
    
        if self.is_first_move:
            total_available_moves = 2


        #
        # Check for opponent pieces that would need to be taken
        #
        for tile_x in [self.pos[0]-1, self.pos[0], self.pos[0]+1]:
            # Only check within board
            if tile_x >= 0 and tile_x <= 7:
                # Does the tile contain an opponent piece
                #print("Tile_x: {}".format(type(tile_x)))
                #print("self.pos[1]+1: {} + 1".format(type(self.pos[1])))

                if self.is_opponent_at_tile( board[ self.pos[1]+1 ][ tile_x ] ) == True:
                    # Add coordinates to available tiles
                    self.available_tiles.append( (self.pos[1]+1, tile_x ) )

        #
        # Pawn advancement in-lane
        #

        if current_player == "uppercase":
            y_direction = 1

        if current_player == "lowercase":
            y_direction = -1

        while total_available_moves > 0:
            print("PAWN MOVE TILE: {}".format(y_direction))

                      
            # Cannot move out of bounds of the board
            if self.pos[1] + y_direction <= 7 or self.pos[1] + y_direction >= 0:

                if self.is_piece_at_tile( board[ self.pos[1] + (total_available_moves * y_direction) ][ self.pos[0] ] ) == False:
                
                    self.available_tiles.append( ( self.pos[0], self.pos[1] + (total_available_moves * y_direction)) )

            total_available_moves -= 1

        return self.available_tiles

    def moved( self ):
        # Triggered when this pawn is moved
        if self.is_first_move == True:
            self.is_first_move = False

    def select( self, board, current_player ):

        #available_tiles = self.possible_moves()
        self.get_possible_moves( board, current_player )
        print("Available Tiles: {}".format(self.available_tiles))

        # Now that we have taken a move with the tile set this first move to false so we cannot do more
        #self.is_first_move = False



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
