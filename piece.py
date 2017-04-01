class Piece(object):

    def __init__( self, **kwargs ):
        
        self.char = kwargs['char'] # this is used as the representation of the piece
        self.available_tiles = [] # array to store coords of available movement tiles
        self.state_list = []

        for key, value in kwargs.items():
            setattr( self, key, value )

    def __str__( self ):
        return "{}".format(self.char)

    # May not use this after all
    # def filter_available_tiles( self, available_tiles = [] ):
    #     # This filter takes in an array of (x,y) tile coordinates.
    #     # This function serves as a way of overriding the available tile output for
    #     # specific use cases in which the available tiles must be altered. 
        
    #     if self.available_tiles != []:
    #         if available_tiles == []:
    #             available_tiles = self.available.tiles

    #     return available_tiles


    def get_possible_moves( self, board = [[]], player = "" ):
        return self.available_tiles


    def get_state_of_piece( self ):
        return self.state_list


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


    def set_state_of_piece( self, state_list ):
        self.state_list = state_list


    def select( self, board = [[]], player = ""):
        # Now that this piece is being selected, see what available moves it has
        self.get_possible_moves( board, player )
        print("Available Tiles: {}".format(self.available_tiles))


