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
        # board_tile given is the contents of the board tile, either a string or an object instance of a piece
        # Returns True if opponent player has a piece on the tile
        
        print("DEBUG: IS_OPPONENT_AT_TILE:{}".format(board_tile))

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
