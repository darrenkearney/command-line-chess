from pieces import Bishop, King, Knight, Pawn, Queen, Rook 
class Chess:

    # Initialize
    def __init__( self, **kwargs ):

        # Default Settings
        self.settings = {
            'players': 2,
            'game_mode': "normal",
            'max_x': 8,
            'max_y': 8,
            'cursor_select_left_char': '[',
            'cursor_select_right_char': ']',
            'cursor_move_left_char': '<',
            'cursor_move_right_char': '>',
            'tile_dark_bg_char':     ':'
        }

        self.is_piece_selected = False

        self.current_player = 'black'

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


    def display( self ):
        # This get's called every update.
        # It returns the output that will be displayed to the user
        # So it needs to handle all the conditions for displaying things.
        # It may call helper functions to make the code cleaner and easier to understand.


        # We're building a string to output to the console.
        output_string = "\n"

        alt = 0 # Used to keep track of alternating tiles to paint the background

        # Let's run a loop over all the tiles of all the rows on the board
        # Filling in the characters as appropriate to their state
        for y in range( len(self.board) ):
            # Paint "Left" side of tile
            # check to see of the first tile on a row is selected, if so paint the border appropriately
            if y == self.cursor_pos[1] and self.cursor_pos[0] == 0:
            
                if self.selected_tile_pos == (0, y):
                    line_x = "\t{}".format( self.settings['cursor_move_left_char'] )
            
                else:
                    line_x = "\t{}".format( self.settings['cursor_select_left_char'] )
            else:
                line_x = "\t|"

            if self.is_piece_selected == True:
            
                if self.selected_tile_pos == (0, y):
                    line_x = "\t{}".format( self.settings['cursor_move_left_char'] )


            for x in range( len( self.board[y] ) ):
                # Paint "Contents" of tile
                # If there is nothing on the board tile use bg color
                if self.board[y][x] == "":
                
                    if alt % 2 == 0:
                        line_x += "{}{}".format( self.settings['tile_dark_bg_char'], self.settings['tile_dark_bg_char'] )
                
                    else:
                        line_x += "  " # Empty blank tile
                else:
                    if alt % 2 == 0:
                        line_x += "{}{}".format( self.board[y][x], self.settings['tile_dark_bg_char'] )
                
                    else:
                        line_x += "{} ".format( self.board[y][x] )
                
                # Paint "Right" side of tile
                # If it's the same tile as the cursor paint a square closing bracket
                # otherwise paint a normal tile edge

                if self.is_piece_selected == True:

                    if self.cursor_pos != (x,y):
                        
                        if (x + 1, y) == self.selected_tile_pos:
                            line_x += self.settings['cursor_move_left_char'] 

                        elif self.selected_tile_pos == (x, y):
                            line_x += self.settings['cursor_move_right_char']
                
                        else:
                            line_x += "|"

                    if self.cursor_pos == (x,y):

                        if self.selected_tile_pos == (x, y):
                            line_x += self.settings['cursor_move_right_char']
                
                        else:
                            line_x += "|"


                if self.is_piece_selected == False:

                    if x == self.cursor_pos[0] and y == self.cursor_pos[1]:
                        line_x += self.settings['cursor_select_right_char']

                    elif x + 1 == self.cursor_pos[0] and y == self.cursor_pos[1]:
                        line_x += self.settings['cursor_select_left_char'] 
                    
                    else:
                        line_x += "|"

                alt += 1

            output_string += "{}\n".format( line_x )

            alt += 1

        print(output_string)


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
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # Display chess board
        self.display()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update {}".format(self.update_count))
        
        # Get input
        print("""
Move Cursor = w (up) / s (down / a (left) / d (right)
Select Piece = x
""")
        player_command = input("Enter command: ")
        self.move_cursor( player_command )

        if player_command.lower() == "x":
            print("Using piece at {}".format(self.cursor_pos))
            # pick up piece
            self.select_piece()

        self.update_count += 1


    def move_cursor( self, player_command ):
        if player_command.lower() == "s":
            print("Down")
            if self.cursor_pos[1] < len(self.board) - 1:
                self.cursor_pos[1] += 1
        
        if player_command.lower() == "w":
            print("Up")
            if self.cursor_pos[1] > 0:
                self.cursor_pos[1] -= 1
        
        if player_command.lower() == "a":
            print("Left")
            if self.cursor_pos[0] > 0:
                self.cursor_pos[0] -= 1
        
        if player_command.lower() == "d":
            print("Right")
            if self.cursor_pos[0] < len(self.board[self.cursor_pos[1]]) - 1:
                self.cursor_pos[0] += 1
        
        if player_command == "":
            print("None")
            player_command = "None"

        print("Your move is {}. Cursor at {}".format(player_command, self.cursor_pos))
        

    def select_piece( self ):
        x = self.cursor_pos[0]
        y = self.cursor_pos[1]
        
        # If nothing is selected, select nothing
        if self.board[y][x] == "":
            print("Nothing to select")
            self.is_piece_selected = False
            return

        self.is_piece_selected = True

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

    def is_opponent_at_tile( self, tile ):
        # Returns True if opponent player has a piece on the tile
        
        if self.current_player == self.board[tile[1], tile[0]].side:
            return True
        else:
            return False