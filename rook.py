from piece import Piece


class Rook(Piece):

    def __init__( self, **kwargs ):
        
        self.name = "Rook"
        self.char = kwargs['char'] # this is used as the representation of the piece
        self.available_tiles = [] # array to store coords of available movement tiles
        self.state_list = []

        # Rook special!
        self.has_castled = False
        self.can_castle = True

        for key, value in kwargs.items():
            setattr( self, key, value )

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
            if self.pos[0] + y <= 7 and self.pos[0] + y >= 0:

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


        # Increment/decrement direction
        direction[0] = x + step_x
        direction[1] = y + step_y

        self.recursive_tile_scanner( board, direction )


    def get_possible_moves( self, board, player ):
        # The games board is board[y][x] but every reference to a position is (x,y)
        # A for loop that checks for possible movement of this piece on the game board.
        # Returns array of coordinate tuples of legal tiles available for the piece to move into.

        self.available_tiles = [] # array of (x,y) coordinate tuples

        # A rook can move horizontally and vertically. We'll scan 4 directions

        # Scan right
        self.recursive_tile_scanner( board, [1,0,1,0] )

        # Scan left
        self.recursive_tile_scanner( board, [-1,0,-1,0] )

        # Scan up
        self.recursive_tile_scanner( board, [0,1,0,1] )

        # Scan down
        self.recursive_tile_scanner( board, [0,-1,0,-1] )

        # Scan right
        # x = 1
        # scanner = 1
        # while self.pos[0] + x - 1 <= 7:

        #     if self.pos[0] == 7:
        #         break

        #     if self.pos[0] + x <= 7:

        #         if self.is_opponent_at_tile( board[ self.pos[1] ][ self.pos[0]+x ] ) == True:
        #             # If tile contains opponent, add it to available tiles, break
        #             self.available_tiles.append( (self.pos[0]+x, self.pos[1]) )
        #             break

        #         elif self.is_piece_at_tile( board[ self.pos[1]][ self.pos[0]+x ] ) == False:
        #             # If tile doesn't contain anything, add it to available tiles
        #             self.available_tiles.append( (self.pos[0]+x, self.pos[1]) )

        #         elif self.is_piece_at_tile( board[ self.pos[1]][ self.pos[0]+x ] ) == True:
        #             # Encountered a piece that isn't an opponent piece, so break
        #             break

        #     x = x + scanner

        # # Scan left
        # x = -1
        # scanner = -1
        # while self.pos[0] + x + 1 >= 0:

        #     if self.pos[0] == 0:
        #         break

        #     if self.pos[0] + x >= 0:
        #         # horizontal done

        #         if self.is_opponent_at_tile( board[ self.pos[1] ][ self.pos[0]+x ] ) == True:
        #             self.available_tiles.append( (self.pos[0]+x, self.pos[1]) )
        #             break

        #         elif self.is_piece_at_tile( board[ self.pos[1]][ self.pos[0]+x ] ) == False:
        #             self.available_tiles.append( (self.pos[0]+x, self.pos[1]) )

        #         elif self.is_piece_at_tile( board[ self.pos[1]][ self.pos[0]+x ] ) == True:
        #             break

        #     x = x + scanner

        # # Scan Up
        # y = 1
        # scanner = 1
        # while self.pos[1] + y - 1 <= 7:

        #     if self.pos[1] == 7:
        #         break

        #     if self.pos[1] + y <= 7:

        #         if self.is_opponent_at_tile( board[ self.pos[1]+y ][ self.pos[0] ] ) == True:
        #             self.available_tiles.append( (self.pos[0], self.pos[1]+y) )
        #             break

        #         elif self.is_piece_at_tile( board[ self.pos[1]+y][ self.pos[0] ] ) == False:
        #             self.available_tiles.append( (self.pos[0], self.pos[1]+y) )

        #         elif self.is_piece_at_tile( board[ self.pos[1]+y][ self.pos[0] ] ) == True:
        #             break

        #     y = y + scanner

        # # Scan down
        # y = -1
        # scanner = -1
        # while self.pos[1] + y + 1 >= 0:

        #     if self.pos[1] == 0:
        #         break

        #     if self.pos[1] + y >= 0:

        #         if self.is_opponent_at_tile( board[ self.pos[1]+y ][ self.pos[0] ] ) == True:
        #             self.available_tiles.append( (self.pos[0], self.pos[1]+y) )
        #             break

        #         elif self.is_piece_at_tile( board[ self.pos[1]+y][ self.pos[0] ] ) == False:
        #             self.available_tiles.append( (self.pos[0], self.pos[1]+y) )

        #         elif self.is_piece_at_tile( board[ self.pos[1]+y][ self.pos[0] ] ) == True:
        #             break

        #     y = y + scanner

        return self.available_tiles

        # A rook can also "castle"

        if self.has_castled == False and self.can_castle == True:

            if self.pos == (0,0):

                # Check tiles in between
                x = 1
                if self.is_piece_at_tile( (x,0) ) == True:
                    x += 1
                    if self.is_piece_at_tile( (x,0) ) == True:
                        x += 1
                        if self.is_piece_at_tile( (x,0) ) == True:
                            x += 1
                            if self.is_piece_at_tile( (x,0) ) == True:

                                # Check state of king
                                if board[0][x].name.lower() == 'king':
                                    if board[0][x].can_castle == True:
                                        self.available_tiles.append( (x,0) )

            if self.pos == (7,0):

                # Check tiles in between
                x = 7
                if self.is_piece_at_tile( (x,0) ) == True:
                    x -= 1
                    if self.is_piece_at_tile( (x,0) ) == True:
                        x -= 1
                        if self.is_piece_at_tile( (x,0) ) == True:

                            # Check state of king
                            if board[0][x].name.lower() == 'king':
                                if board[0][x].can_castle == True:
                                    self.available_tiles.append( (x,0) )

            if self.pos == (0,7):

                # Check tiles in between
                x = 1
                if self.is_piece_at_tile( (x,7) ) == True:
                    x += 1
                    if self.is_piece_at_tile( (x,7) ) == True:
                        x += 1
                        if self.is_piece_at_tile( (x,7) ) == True:
                            x += 1
                            if self.is_piece_at_tile( (x,7) ) == True:

                                # Check state of king
                                if board[7][x].name.lower() == 'king':
                                    if board[7][x].can_castle == True:
                                        self.available_tiles.append( (x,7) )

                                # Check state of king
                                if board[7][x].name.lower() == 'king':
                                    if board[7][x].can_castle == True:
                                        self.available_tiles.append( (x,7) )

            if self.pos == (7,7):

                # Check tiles in between
                x = 7
                if self.is_piece_at_tile( (x,7) ) == True:
                    x -= 1
                    if self.is_piece_at_tile( (x,7) ) == True:
                        x -= 1
                        if self.is_piece_at_tile( (x,7) ) == True:

                            # Check state of king
                            if board[7][x].name.lower() == 'king':
                                if board[7][x].can_castle == True:
                                    self.available_tiles.append( (x,7) )