class Chess:

    # Initialize
    def __init__( self, **kwargs ):

        # Default Settings
        self.settings = {
            'players':    1,
            'game_mode':  "normal",
            'max_x': 8,
            'max_y': 8
        }

        self.turn_count = 0

        for item in kwargs.items():
            setattr( self, item )


    def convert_coordinates( self, coords ):
        # If player enters the chess board coordinate used in the board game
        # As a string "xy" where x is a letter and y is a number

        if len( coords ) == 2:
            coords = coords.split()

        for index, value in [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' ]:
            if coord[0].lower() == value:
                coord[0] = index
                break


    def get_board( self ):

        output_string = ""

        # Keeps track of alternating board tiles for rendering bg
        alt = 0

        for y in range( len(self.board) ):

            line_x = "|"

            for x in range( len(self.board[y]) ):
                
                # If there is nothing on the board tile use bg color
                if self.board[y][x] == "":
                    if alt % 2 == 0:
                        line_x += "::|"
                    else:
                        line_x += "  |"
                else:
                    if alt % 2 == 0:
                        line_x += "{}:|".format( self.board[y][x] )
                    else:
                        line_x += "{} |".format( self.board[y][x] )
                    
                alt += 1

            output_string += "{}\n".format( line_x )

            alt += 1
            
        # Return the output string
        return output_string


    # Sets up a two dimensional array for the game pieces
    def setup_game_board( self ):
        
 
        self.board = []
        for y in range( self.settings[ 'max_y' ] ):
            line_x = []
            for x in range( self.settings[ 'max_x' ] ):
                line_x.append( "" )
            self.board.append( line_x )

        # Just in case we add more game modes with odd setups
        if self.settings['game_mode'] == 'normal':
            board_setup_stack = ['r','n','b','k','q','b','n','r']
            for tile in range( len( self.board[0] ) ):
                self.board[0][tile] = board_setup_stack[tile]
            for tile in range( len( self.board[1] ) ):
                self.board[1][tile] = 'p'
            for tile in range( len( self.board[6] ) ):
                self.board[6][tile] = 'P'
            for tile in range( len( self.board[7] ) ):
                self.board[7][tile] = board_setup_stack[tile].upper()







    # Run a "Frame" or execute a turn
    def update( self ):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update {}\n".format(self.turn_count))
        print(self.get_board())
        choice = input("Enter your move: ")
        print("Your move is {}".format(choice))
        self.turn_count += 1
