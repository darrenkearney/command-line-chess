from piece import Piece


class Queen(Piece):

    def __init__( self, **kwargs ):
        
        self.name = "Queen"
        self.char = kwargs['char'] # this is used as the representation of the piece
        self.available_tiles = [] # array to store coords of available movement tiles
        self.state_list = []

        for key, value in kwargs.items():
            setattr( self, key, value )
