from piece import Piece


class Rook(Piece):

    def __init__( self, **kwargs ):

        # Normal setup
        self.char = kwargs['char'] # this is used as the representation of the piece
        self.available_tiles = [] # array to store coords of available movement tiles
        self.is_debug_mode = False
        self.debug_logs = []
        self.state_list = []

        # Rook special!
        self.name = "Rook"
        self.has_castled = False
        self.can_castle = True

        for key, value in kwargs.items():
            setattr( self, key, value )


    def get_possible_moves( self, board, player ):
        # The games board is board[y][x] but every reference to a position is (x,y)
        # A for loop that checks for possible movement of this piece on the game board.
        # Returns array of coordinate tuples of legal tiles available for the piece to move into.

        self.available_tiles = [] # array of (x,y) coordinate tuples

        # A rook can move horizontally and vertically. We'll scan 4 directions

        # Scan right
        self.recursive_tile_scanner( board, [1,0,1,0,-1] )

        # Scan left
        self.recursive_tile_scanner( board, [-1,0,-1,0,-1] )

        # Scan up
        self.recursive_tile_scanner( board, [0,1,0,1,-1] )

        # Scan down
        self.recursive_tile_scanner( board, [0,-1,0,-1,-1] )

        return self.available_tiles

        # A rook can also "castle"

        # if self.has_castled == False and self.can_castle == True:

        #     if self.pos == (0,0):

        #         # Check tiles in between
        #         x = 1
        #         if self.is_piece_at_tile( (x,0) ) == True:
        #             x += 1
        #             if self.is_piece_at_tile( (x,0) ) == True:
        #                 x += 1
        #                 if self.is_piece_at_tile( (x,0) ) == True:
        #                     x += 1
        #                     if self.is_piece_at_tile( (x,0) ) == True:

        #                         # Check state of king
        #                         if board[0][x].name.lower() == 'king':
        #                             if board[0][x].can_castle == True:
        #                                 self.available_tiles.append( (x,0) )

        #     if self.pos == (7,0):

        #         # Check tiles in between
        #         x = 7
        #         if self.is_piece_at_tile( (x,0) ) == True:
        #             x -= 1
        #             if self.is_piece_at_tile( (x,0) ) == True:
        #                 x -= 1
        #                 if self.is_piece_at_tile( (x,0) ) == True:

        #                     # Check state of king
        #                     if board[0][x].name.lower() == 'king':
        #                         if board[0][x].can_castle == True:
        #                             self.available_tiles.append( (x,0) )

        #     if self.pos == (0,7):

        #         # Check tiles in between
        #         x = 1
        #         if self.is_piece_at_tile( (x,7) ) == True:
        #             x += 1
        #             if self.is_piece_at_tile( (x,7) ) == True:
        #                 x += 1
        #                 if self.is_piece_at_tile( (x,7) ) == True:
        #                     x += 1
        #                     if self.is_piece_at_tile( (x,7) ) == True:

        #                         # Check state of king
        #                         if board[7][x].name.lower() == 'king':
        #                             if board[7][x].can_castle == True:
        #                                 self.available_tiles.append( (x,7) )

        #                         # Check state of king
        #                         if board[7][x].name.lower() == 'king':
        #                             if board[7][x].can_castle == True:
        #                                 self.available_tiles.append( (x,7) )

        #     if self.pos == (7,7):

        #         # Check tiles in between
        #         x = 7
        #         if self.is_piece_at_tile( (x,7) ) == True:
        #             x -= 1
        #             if self.is_piece_at_tile( (x,7) ) == True:
        #                 x -= 1
        #                 if self.is_piece_at_tile( (x,7) ) == True:

        #                     # Check state of king
        #                     if board[7][x].name.lower() == 'king':
        #                         if board[7][x].can_castle == True:
        #                             self.available_tiles.append( (x,7) )