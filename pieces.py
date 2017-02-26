class Piece(object):
    def __init__( self, **kwargs ):
        
        self.char = kwargs['char'] # this is used as the representation of the piece

        for key, value in kwargs.items():
            setattr( self, key, value )

    def __str__( self ):
        return "{}".format(self.char)

class Bishop(Piece):
    def __init__( self, **kwargs ):
        
        self.char = kwargs['char'] # this is used as the representation of the piece

        for key, value in kwargs.items():
            setattr( self, key, value )

class King(Piece):
    pass

class Knight(Piece):
    pass

class Pawn(Piece):

    def __init__( self, **kwargs ):

        self.is_first_turn = True

        #self.pos = kwargs['pos'] # (x,y)
        for key, value in kwargs.items():
            setattr( self, key, value )

    def define_possible_moves( self ):
    
        total_available_moves = 1
    
        if self.is_first_turn:
        
            total_available_moves = 2

        self.available_tiles = [] # array of (x,y) coordinate tuples

        # A pawn has a simple moveset. It can only advance in the y access.
        for tile in total_available_moves:
            
            if side == "black":
                tile = -tile
            
            if self.pos[1] + tile <= 8 or self.pos[1] + tile >= 0:
                self.available_tiles.append( ( self.pos[0], self.pos[1] + tile ) )


class Queen(Piece):
    pass

class Rook(Piece):

    def __init__( self, **kwargs ):
        
        #self.char = kwargs['char'] # this is used as the representation of the piece

        for key, value in kwargs.items():
            setattr( self, key, value )
