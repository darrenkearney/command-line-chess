from piece import Piece


class Knight(Piece):

    def __init__( self, **kwargs ):
        
        self.name = "Knight"
        self.char = kwargs['char'] # this is used as the representation of the piece

        for key, value in kwargs.items():
            setattr( self, key, value )
