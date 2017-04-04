from piece import Piece


class Pawn(Piece):

    def __init__( self, **kwargs ):

        self.char = kwargs['char'] # this is used as the representation of the piece
        self.available_tiles = [] # array to store coords of available movement tiles
        self.is_debug_mode = False
        self.debug_logs = []
        self.state_list = []

        # Pawn special
        self.name = "Pawn"
        self.is_first_move = True

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
            self.debug_log("@@@@ Oddly player is neither uppercase or lowercase, its {}".format(player))

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
        moves = []
        while len(moves) + 1 <= total_available_moves:
            self.debug_log("PAWN Move y_direction: {}".format(y_direction))

            # Cannot move out of bounds of the board
            if self.pos[1] + ( (len(moves)+1) * y_direction)  >= 0 and self.pos[1] + ((len(moves)+1) * y_direction) <= 7:

                if self.is_piece_at_tile( board[ self.pos[1] + ((len(moves)+1) * y_direction) ][ self.pos[0] ] ) == False:
                    self.available_tiles.append( ( self.pos[0], self.pos[1] + ((len(moves)+1) * y_direction) ) )
                elif self.is_piece_at_tile( board[ self.pos[1] + ((len(moves)+1) * y_direction) ][ self.pos[0] ] ) == True:
                    break

                # # if there is a piece at target tile, break continue the loop
                # if self.is_piece_at_tile( board[ self.pos[1] + (total_available_moves * y_direction) ][ self.pos[0] ] ) == True:
                #     total_available_moves -= 1
                #     continue

                # #  if no piece ar target tile, and there is nothing blocking the path, add it.
                # elif self.is_piece_at_tile( board[ self.pos[1] + (total_available_moves * y_direction) ][ self.pos[0] ] ) == False:

                #     if self.is_first_move and (total_available_moves*y_direction) + self.pos[1] in [self.pos[1] + 2, self.pos[1] - 2 ]:
                #         if self.is_piece_at_tile( board[ self.pos[1] + y_direction ][ self.pos[0] ] ):
                #             break

                #     else:
                #         self.available_tiles.append( ( self.pos[0], self.pos[1] + (total_available_moves * y_direction) ) )

            moves.append(( self.pos[0], self.pos[1] + ((len(moves)+1) * y_direction) ))

        return self.available_tiles

    def moved( self ):
        # Triggered when this pawn is moved
        if self.is_first_move == True:
            self.is_first_move = False

    def select( self, board, player ):
        # Now that this piece is being selected, see what available moves it has
        self.get_possible_moves( board, player )
        print("Available Tiles: {}".format(self.available_tiles))
