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


    def recursive_tile_scanner( self, board, direction ):
        # Unfinished
        # Scans tiles in direction

        x = direction[0]
        y = direction[1]
        step_x = direction[2]
        step_y = direction[3]


        # if no direction then just exit
        if x == 0 and y == 0:
            return

        # Don't go off the board
        if self.pos[0] + x >= 8:
            return

        if self.pos[0] + x <= -1:
            return

        if self.pos[1] + y >= 8:
            return

        if self.pos[1] + y <= -1:
            return

        # Look for pieces in this direction on x axis
        if x != 0:
            if self.pos[0] + x <= 7 and self.pos[0] + x >= 0:

                if self.is_opponent_at_tile( board[ self.pos[1] ][ self.pos[0]+x ] ) == True:
                    # If tile contains opponent, add it to available tiles, break
                    self.available_tiles.append( (self.pos[0]+x, self.pos[1]) )
                    return

                elif self.is_piece_at_tile( board[ self.pos[1]][ self.pos[0]+x ] ) == False:
                    # If tile doesn't contain anything, add it to available tiles
                    self.available_tiles.append( (self.pos[0]+x, self.pos[1]) )

                elif self.is_piece_at_tile( board[ self.pos[1]][ self.pos[0]+x ] ) == True:
                    # Encountered a piece that isn't an opponent piece, so break
                    return

        if y != 0:
            if self.pos[1] + y <= 7 and self.pos[1] + y >= 0:

                if self.is_opponent_at_tile( board[ self.pos[1]+y ][ self.pos[0] ] ) == True:
                    # If tile contains opponent, add it to available tiles, break
                    self.available_tiles.append( (self.pos[0], self.pos[1]+y) )
                    return

                elif self.is_piece_at_tile( board[ self.pos[1]+y][ self.pos[0] ] ) == False:
                    # If tile doesn't contain anything, add it to available tiles
                    self.available_tiles.append( (self.pos[0], self.pos[1]+y) )

                elif self.is_piece_at_tile( board[ self.pos[1]+y][ self.pos[0] ] ) == True:
                    # Encountered a piece that isn't an opponent piece, so break
                    return


        # Increment/decrement direction by step
        direction[0] = x + step_x
        direction[1] = y + step_y

        self.recursive_tile_scanner( board, direction )


    def set_state_of_piece( self, state_list ):
        self.state_list = state_list


    def select( self, board = [[]], player = ""):
        # Now that this piece is being selected, see what available moves it has
        self.get_possible_moves( board, player )
        print("Available Tiles: {}".format(self.available_tiles))


