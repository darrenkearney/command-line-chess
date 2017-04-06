from piece import Piece


class Bishop(Piece):

    def __init__( self, **kwargs ):
        
        self.char = kwargs['char'] # this is used as the representation of the piece
        self.available_tiles = [] # array to store coords of available movement tiles
        self.is_debug_mode = False
        self.debug_logs = []
        self.state_list = []

        # Bishop special
        self.name = "Bishop"

        for key, value in kwargs.items():
            setattr( self, key, value )


    def get_possible_moves( self, board, player ):

        self.available_tiles = [] # array of (x,y) coordinate tuples

        # A bishop can move diagonally. We'll scan those directions clockwise

        # Scan up-right
        self.recursive_tile_scanner( board, [1,1,1,1,-1] )

        # Scan down-right
        self.recursive_tile_scanner( board, [1,-1,1,-1,-1] )

        # Scan down-left
        self.recursive_tile_scanner( board, [-1,-1,-1,-1,-1])

        # Scan up-left
        self.recursive_tile_scanner( board, [-1,1,-1,1,-1] )

        return self.available_tiles