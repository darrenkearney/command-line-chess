from pieces import Bishop, King, Knight, Pawn, Queen, Rook 
class Chess:

    # Initialize
    def __init__( self, **kwargs ):

        # Default Settings
        self.settings = {
            'players':      1,
            'game_mode':    "normal",
            'max_x':        8,
            'max_y':        8
        }

        self.update_count = 0

        self.cursor_pos = [0,0] # (x,y)
        self.selected_tile_pos = []

        for item in kwargs.items():
            setattr( self, item )


        self.setup_game_board()


    def convert_coordinates( self, coords ):
        # If player enters the chess board coordinate used in the board game
        # As a string "xy" where x is a letter and y is a number

        if len( coords ) == 2:
            coords = coords.split()

        for index, value in [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' ]:
            if coord[0].lower() == value:
                coord[0] = index
                break


    def get_board_string( self ):

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


    def display( self ):
        # This get's called every update.
        # It returns the output that will be displayed to the user
        # So it needs to handle all the conditions for displaying things.
        # It may call helper functions to make the code cleaner and easier to understand.


        # We're building a string to output to the console.
        output_string = ""

        alt = 0 # Used to keep track of alternating tiles to paint the background

        # Let's run a loop over all the tiles of all the rows on the board
        # Filling in the characters as appropriate to their state
        for y in range( len(self.board) ):

            # check to see of the first tile on a row is selected, if so paint the border appropriately
            if y == self.cursor_pos[1] and self.cursor_pos[0] == 0:
                line_x = "["
            else:
                line_x = "|"

            for x in range( len( self.board[y] ) ):
                
                # If there is nothing on the board tile use bg color
                if self.board[y][x] == "":
                    if alt % 2 == 0:
                        line_x += "::"
                    else:
                        line_x += "  "
                else:
                    if alt % 2 == 0:
                        line_x += "{}:".format( self.board[y][x] )
                    else:
                        line_x += "{} ".format( self.board[y][x] )
                
                # If it's the same tile as the cursor paint a square closing bracket
                # otherwise paint a normal wall
                if x == self.cursor_pos[0] and y == self.cursor_pos[1]:
                    if (x,y) == self.selected_tile_pos:
                        line_x += ">"
                    else:
                        line_x += "]"
                elif x + 1 == self.cursor_pos[0] and y == self.cursor_pos[1]:
                    if (x + 1, y) == self.selected_tile_pos:
                        line_x += "<"
                    else:
                        line_x += "["
                else:
                    line_x += "|"

                alt += 1

            output_string += "{}\n".format( line_x )

            alt += 1

        print(output_string)


    # Sets up the two dimensional array for referencing the game pieces
    def setup_game_board( self ):
 
        self.board = []
        for y in range( self.settings[ 'max_y' ] ):
            line_x = []
            for x in range( self.settings[ 'max_x' ] ):
                line_x.append( "" ) # Empty board tiles are emty strings
            self.board.append( line_x )

        # Just in case we add more game modes with odd setups
        if self.settings['game_mode'] == 'normal':

            board_setup_stack = ['r','n','b','k','q','b','n','r'] # array of pieces

            for tile in range( len( self.board[0] ) ):
                char = board_setup_stack[tile]
                self.board[0][tile] = self.new_piece( board_setup_stack[tile], (tile, 0), "white" )
            for tile in range( len( self.board[1] ) ):
                self.board[1][tile] = Pawn( char = "p", pos = (tile, 1), side = "white" )
            for tile in range( len( self.board[6] ) ):
                self.board[6][tile] = Pawn( char = "P", pos = (tile, 6), side = "black" )
            for tile in range( len( self.board[7] ) ):
                self.board[7][tile] = self.new_piece( board_setup_stack[tile].upper(), (tile, 7), "black" )

    def new_piece( self, char = "", pos = (0,0), side = "" ):
        # Returns a new instance of a pieces class based on the char representation given

        if char.lower() == 'b':
            return Bishop( char = char, pos = pos, side = side )

        if char.lower() == 'k':
            return King( char = char, pos = pos, side = side )

        if char.lower() == 'n': 
            return Knight( char = char, pos = pos, side = side )
     
        if char.lower() == 'p': 
            return Pawn( char = char, pos = pos, side = side )
     
        if char.lower() == 'q':
            return Queen( char = char, pos = pos, side = side )

        if char.lower() == 'r':
            return Rook( char = char, pos = pos, side = side )


    # Run a "Frame" or execute a turn
    def update( self ):
        # reset cursor
        # print("^[[A"*40)

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update {}\n".format(self.update_count))
        #print(self.get_board_string())
        
        user_direction = input("Move Cursor [w/s/a/d]: ")
        self.move_cursor( user_direction )
        if user_direction.lower() == "x":
            print("Using piece at {}".format(self.cursor_pos))
            # pick up piece
            self.select_piece()
        
        # Display chess board
        self.display()

        self.update_count += 1


    def move_cursor( self, user_direction ):
        if user_direction.lower() == "s":
            print("Down")
            if self.cursor_pos[1] < len(self.board):
                self.cursor_pos[1] += 1
        if user_direction.lower() == "w":
            print("Up")
            if self.cursor_pos[1] > 0:
                self.cursor_pos[1] -= 1
        if user_direction.lower() == "a":
            print("Left")
            if self.cursor_pos[0] > 0:
                self.cursor_pos[0] -= 1
        if user_direction.lower() == "d":
            print("Right")
            if self.cursor_pos[0] < len(self.board[self.cursor_pos[1]]):
                self.cursor_pos[0] += 1

        print("Your move is {}. Cursor at {}".format(user_direction, self.cursor_pos))
        

    def select_piece( self ):
        x = self.cursor_pos[0]
        y = self.cursor_pos[1]
        
        if self.board[y][x] == "":
            print("Nothing to select")
            return

        # Bishop
        if self.board[y][x].char.lower() == 'b':
            print("Selected Bishop")
            
        # King
        if self.board[y][x].char.lower() == 'k':
            print("Selected King")
        
        # Knight
        if self.board[y][x].char.lower() == 'n':
            print("Selected Knight")

        # Pawn
        if self.board[y][x].char.lower() == 'p':
            print("Selected Pawn")

        # Queen
        if self.board[y][x].char.lower() == 'q':
            print("Selected Queen")

        # Rook
        if self.board[y][x].char.lower() == 'r':
            print("Selected Rook")

        self.selected_tile_pos = (x,y)