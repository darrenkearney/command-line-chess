from piece import Piece


class Knight(Piece):

    def __init__( self, **kwargs ):
        
        self.name = "Knight"
        self.char = kwargs['char'] # this is used as the representation of the piece
        self.available_tiles = [] # array to store coords of available movement tiles
        self.state_list = []

        for key, value in kwargs.items():
            setattr( self, key, value )


    def get_possible_moves( self, board, player ):

        self.available_tiles = [] # array of (x,y) coordinate tuples

        # A knight moves weirdly. on tile out, then diagonally.

        move_limit = 1

        # Scan up up right
        self.recursive_tile_scanner( board, [1,2,0,0, move_limit ] )

        # Scan up right right
        self.recursive_tile_scanner( board, [2,1,0,0, move_limit ] )

        # Scan down right right
        self.recursive_tile_scanner( board, [2,-1,0,0, move_limit ] )

        # Scan down down right
        self.recursive_tile_scanner( board, [1,-2,0,0, move_limit ] )

        # Scan down down left
        self.recursive_tile_scanner( board, [-1,-2,0,0, move_limit ] )

        # Scan down left left
        self.recursive_tile_scanner( board, [-2,-1,0,0, move_limit ] )

        # Scan up left left
        self.recursive_tile_scanner( board, [-2,1,0,0, move_limit ] )

        # Scan up up left
        self.recursive_tile_scanner( board, [-1,2,0,0, move_limit ] )

        return self.available_tiles