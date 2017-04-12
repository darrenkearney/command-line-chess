from piece import Piece


class King(Piece):

    def __init__( self, **kwargs ):
        
        self.char = kwargs['char'] # this is used as the representation of the piece
        self.available_tiles = [] # array to store coords of available movement tiles
        self.is_debug_mode = False
        self.debug_logs = []
        self.state_list = []

        # King special
        self.name = "King"

        for key, value in kwargs.items():
            setattr( self, key, value )


    def get_possible_moves( self, board, player ):
        # The games board is board[y][x] but every reference to a position is (x,y)
        # A for loop that checks for possible movement of this piece on the game board.
        # Returns array of coordinate tuples of possible tiles available for the piece to move into.
        # Does not consider check rules or special rules - only piece's moveset.

        self.available_tiles = [] # array of (x,y) coordinate tuples

        # A king can move 1 square horizontally, vertically or diagonally. We'll scan those directions clockwise

        move_limit = 1

        # Scan up
        self.recursive_tile_scanner( board, [0,1,0,1, move_limit ] )

        # Scan up-right
        self.recursive_tile_scanner( board, [1,1,1,1, move_limit ] )

        # Scan right
        self.recursive_tile_scanner( board, [1,0,1,0, move_limit ] )

        # Scan down-right
        self.recursive_tile_scanner( board, [1,-1,1,-1, move_limit ] )

        # Scan down
        self.recursive_tile_scanner( board, [0,-1,0,-1, move_limit ] )

        # Scan down-left
        self.recursive_tile_scanner( board, [-1,-1,-1,-1, move_limit ] )

        # Scan left
        self.recursive_tile_scanner( board, [-1,0,-1,0, move_limit ] )

        # Scan up-left
        self.recursive_tile_scanner( board, [-1,1,-1,1, move_limit ] )

        return self.available_tiles