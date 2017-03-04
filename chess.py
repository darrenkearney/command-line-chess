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
            'cursor_left_char': '[',
            'cursor_right_char': ']',
            'cursor_move_left_char': '<',
            'cursor_move_right_char': '>',
            'tile_dark_bg_char': ':'
        }
        self.player_command = ""

        self.is_help_mode = False

        self.is_piece_selected = False

        self.current_player = 'lowercase'

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
            # Paint "Left" side of tile (we will hereafter append the tile edges to the tile content)
            # check to see of the first tile on a row is selected, if so paint the tile edge/border appropriately
            
            line_x = "\t" # Reset line_x for constructing new line

            if self.is_help_mode == True:
                line_x = "      {} ".format( 8 - y )


            if y == self.cursor_pos[1] and self.cursor_pos[0] == 0:
            
                if self.selected_tile_pos == [0, y]:
                    line_x += "{}".format( self.settings['cursor_move_left_char'] )
            
                else:
                    line_x += "{}".format( self.settings['cursor_left_char'] )
            else:
                line_x += "|"

            if self.is_piece_selected == True:
            
                if self.selected_tile_pos == [0, y]:
                    line_x += "{}".format( self.settings['cursor_move_left_char'] )


            for x in range( len( self.board[y] ) ):
                # Paint "Contents" of tile
                # If there is nothing on the board tile use bg color

                # if the board tile is empty
                if self.board[y][x] == "":

                    # check state - if there is a piece selected then we want to render it's available move tiles
                    if self.is_piece_selected == True and [x,y] in self.selected_piece.available_tiles:
                        
                        if alt % 2 == 0:
                            line_x += "{}{}".format( "+", self.settings['tile_dark_bg_char'])
                        else:
                            line_x += "{}{}".format( self.settings['tile_dark_bg_char'], self.settings['tile_dark_bg_char'] )
                    else:

                        if alt % 2 == 0:
                            line_x += "{}{}".format( self.settings['tile_dark_bg_char'], self.settings['tile_dark_bg_char'] )
                        else:
                            line_x += "  " # Empty blank tile
                      
                    # if alt % 2 == 0:
                    #     if self.is_piece_selected == True and [x,y] in self.selected_piece.available_tiles:
                    #         line_x += "{}{}".format( self.settings['tile_dark_bg_char'], "+")
                
                    #     else:
                    #         line_x += "{}{}".format( self.settings['tile_dark_bg_char'], self.settings['tile_dark_bg_char'] )
                
                    # else:
                    #     if self.is_piece_selected == True and [x,y] in self.selected_piece.available_tiles:
                    #         print("[{},{}] in available tiles: {}".format(x,y, self.selected_piece.available_tiles))
                    #         line_x += " {}".format( "+" )
                    #     line_x += "  " # Empty blank tile

                else:
                    
                    if alt % 2 == 0:
                        if self.is_piece_selected == True and [x,y] in self.selected_piece.available_tiles:
                            line_x += "{}{}".format( "x", self.board[y][x] )
                        else:
                            line_x += "{}{}".format( self.settings['tile_dark_bg_char'], self.board[y][x] )
                
                    else:
                        if self.is_piece_selected == True and [x,y] in self.selected_piece.available_tiles:
                            line_x += "{}{}".format( "x", self.board[y][x], )
                        else:
                            line_x += " {}".format( self.board[y][x] )
                
                # Paint "Right" side of tile
                # If it's the same tile as the cursor paint a square closing bracket
                # otherwise paint a normal tile edge

                if self.is_piece_selected == True:
                    # Okay, a piece is selected. Now we are in Move Mode.


                    if [x, y] != self.cursor_pos:
                        # If the currently rendering tile is not the cursor tile
                        # But it is adjacent to it
                        if [x + 1, y] == self.selected_tile_pos:
                            #if the one to the right is the cursor tile, paint it's left border
                            line_x += self.settings['cursor_move_left_char'] 

                        # If the current rendered tile is the selected tile and not the cursor tile
                        elif [x, y] == self.selected_tile_pos:
                            line_x += self.settings['cursor_move_right_char']

                        # If the currently rendered tile is adjacent to the cursor ( but not the above )
                        elif [x + 1, y] == self.cursor_pos:
                            line_x += self.settings['cursor_left_char'] 
                
                        # Otherwise paint the normal board edge
                        else:
                            line_x += "|"

                    if [x, y] == self.cursor_pos:
                        # In Move mode,
                        # And the currently rendering tile is the cursor tile, AND it is the Selected Piece/Tile
                        # Give it the move-mode tile paint
                        if self.cursor_pos == self.selected_tile_pos:
                            line_x += self.settings['cursor_move_right_char']

                        # Otherwise the current cursor is being rendered, so use the normal cursor
                        else:
                            line_x += self.settings['cursor_right_char']


                if self.is_piece_selected == False:

                    if [x, y] == self.cursor_pos:
                        line_x += self.settings['cursor_right_char']

                    elif [x + 1, y] == self.cursor_pos:
                        line_x += self.settings['cursor_left_char'] 
                    
                    else:
                        line_x += "|"

                alt += 1

            output_string += "{}".format( line_x )

            if y <= 7:
                output_string += "\n" # add a newline

            # Help mode text
            if y == 7 and self.is_help_mode == True:
                line_x = "\t"
                coords = ['a','b','c','d','e','f','g','h']

                for x in range( len( self.board[y] ) ):
                    line_x += " {} ".format( coords[x] )

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
                self.board[0][tile] = self.new_piece( board_setup_stack[tile].upper(), (tile, 0), "uppercase" )
            
            for tile in range( len( self.board[1] ) ):
                self.board[1][tile] = Pawn( char = "P", pos = (tile, 1), side = "uppercase" )
            
            for tile in range( len( self.board[6] ) ):
                self.board[6][tile] = Pawn( char = "p", pos = (tile, 6), side = "lowercase" )
            
            for tile in range( len( self.board[7] ) ):
                self.board[7][tile] = self.new_piece( board_setup_stack[tile], (tile, 7), "lowercase" )


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


    def do_command( self, player_command ):

        # Reset help mode
        if self.is_help_mode == True:
            self.is_help_mode = False

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

        if player_command.lower() in ["h", "help", "?"]:
            self.is_help_mode = True
            print("Help menu")
            print(
"""Commands:
    Help (display this menu) = h / ? / help
    Move Cursor = w (up) / s (down / a (left) / d (right)
    Select Piece = x
""")

        print("Your move is {}. Cursor at {}".format(player_command, self.cursor_pos))
        

    def select_piece( self ):
        x = self.cursor_pos[0]
        y = self.cursor_pos[1]
        
        # If nothing is selected, select nothing
        if self.board[y][x] == "":
            print("Nothing to select")
            self.is_piece_selected = False
            return

        if self.current_player != self.board[y][x].side:
            print("Cannot select the other player's piece.")
            return

        self.is_piece_selected = True
        
        self.board[y][x].select() # trigger the select method on the piece
    
        self.selected_piece = self.board[y][x]
        print("Selected: {}. Position: {}, Side: {}".format(
            self.selected_piece.name,
            self.selected_piece.pos,
            self.selected_piece.side))


        self.selected_tile_pos = [x,y]

        # Set up possible moves (must send the chess board to this method)
        self.selected_piece.get_possible_moves( self )

    def is_opponent_at_tile( self, tile ):
        # Returns True if opponent player has a piece on the tile
        if type(self.board[ tile[0] ][ tile[1] ]) == str:
            return False

        if self.current_player == self.board[ tile[0] ][ tile[1] ].side:
            return True
        
        return False


    # Run a "Frame" or execute a turn
    def update( self ):
        print("~" * 42)
        if self.is_help_mode == True:
            print("\t\tUppercase")

        # Display chess board
        self.display()

        if self.is_help_mode == True:
            print("\t\tLowercase")

        print("~" * 42)
        print("Update {}".format(self.update_count))

        # Get input
        print("Current player: {}".format(self.current_player))
        self.player_command = input("Enter a command: ")
        self.do_command( self.player_command )
 
        if self.player_command.lower() == "x":
            print("Using piece at {}".format(self.cursor_pos))

            # pick up piece
            self.select_piece()
        
        

        self.update_count += 1