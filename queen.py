from piece import Piece


class Queen(Piece):

    def __init__( self, **kwargs ):
        
        self.char = kwargs['char'] # this is used as the representation of the piece
        self.available_tiles = [] # array to store coords of available movement tiles
        self.is_debug_mode = False
        self.debug_logs = []
        self.state_list = []

        # Queen special!
        self.name = "Queen"

        for key, value in kwargs.items():
            setattr( self, key, value )


    def get_possible_moves( self, board, player ):
        # The games board is board[y][x] but every reference to a position is (x,y)
        # A for loop that checks for possible movement of this piece on the game board.
        # Returns array of coordinate tuples of possible tiles available for the piece to move into.
        # Does not consider check rules or special rules - only piece's moveset.

        self.available_tiles = [] # array of (x,y) coordinate tuples

        # A queen can move horizontally, vertically and diagonally. We'll scan those directions clockwise

        # Scan up
        self.recursive_tile_scanner( board, [0,1,0,1,-1] )

        # Scan up-right
        self.recursive_tile_scanner( board, [1,1,1,1,-1] )

        # Scan right
        self.recursive_tile_scanner( board, [1,0,1,0,-1] )

        # Scan down-right
        self.recursive_tile_scanner( board, [1,-1,1,-1,-1] )

        # Scan down
        self.recursive_tile_scanner( board, [0,-1,0,-1,-1] )

        # Scan down-left
        self.recursive_tile_scanner( board, [-1,-1,-1,-1,-1] )

        # Scan left
        self.recursive_tile_scanner( board, [-1,0,-1,0,-1] )

        # Scan up-left
        self.recursive_tile_scanner( board, [-1,1,-1,1,-1] )

        return self.available_tiles