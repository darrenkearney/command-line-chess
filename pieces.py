class Piece(object):
    def __init__( self, **kwargs ):
        for item in kwargs.items():
            setattr( self, item )

class Bishop(Piece):
    pass

class King(Piece):
    pass

class Knight(Piece):
    pass

class Pawn(Piece):
    pass

class Queen(Piece):
    pass

class Rook(Piece):
    pass
