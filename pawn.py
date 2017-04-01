from piece import Piece


class Pawn(Piece):

    def __init__( self, **kwargs ):

        self.name = "Pawn"
        self.available_tiles = [] # array to store coords of available movement tiles
        self.is_first_move = True
        self.state_list = []

        #self.pos = kwargs['pos'] # (x,y)
        for key, value in kwargs.items():
            setattr( self, key, value )

    def get_possible_moves( self, board, player ):
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
        # Pawn advancement direction
        #
        if player == "uppercase":
            y_direction = 1
            #print("get possible moves player uppercase {}".format(player))

        elif player == "lowercase":
            y_direction = -1
            #print("get possible moves player lowercase {}".format(player))

        else:
            print("@@@@ Oddly player is neither uppercase or lowercase, its {}".format(player))

        #
        # Check for opponent pieces that would need to be taken
        #
        for tile_x in [self.pos[0]-1, self.pos[0]+1]:
            
            # Only check within board (horizontal)
            if tile_x >= 0 and tile_x <= 7:

                # Only check within board (vertical)
                if self.pos[1]+y_direction >= 0 and self.pos[1]+y_direction <= 7:

                    # Does the tile contain an opponent piece?
                    if self.is_opponent_at_tile( board[ self.pos[1]+y_direction ][ tile_x ] ) == True:
                        # Add coordinates to available tiles
                        self.available_tiles.append( ( tile_x, self.pos[1]+y_direction ) )
        
        while total_available_moves > 0:
            print("PAWN Move y_direction: {}".format(y_direction))

            # Cannot move out of bounds of the board
            if self.pos[1] + (total_available_moves * y_direction) >= 0 and self.pos[1] + (total_available_moves * y_direction) <= 7:

                if self.is_piece_at_tile( board[ self.pos[1] + (total_available_moves * y_direction) ][ self.pos[0] ] ) == False:
                
                    self.available_tiles.append( ( self.pos[0], self.pos[1] + (total_available_moves * y_direction) ) )

            total_available_moves -= 1

        return self.filter_available_tiles(self.available_tiles)

    def moved( self ):
        # Triggered when this pawn is moved
        if self.is_first_move == True:
            self.is_first_move = False

    def select( self, board, player ):

        #available_tiles = self.possible_moves()
        self.get_possible_moves( board, player )
        print("Available Tiles: {}".format(self.available_tiles))

        # Now that we have taken a move with the tile set this first move to false so we cannot do more
        #self.is_first_move = False

