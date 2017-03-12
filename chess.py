from piece  import Piece
from bishop import Bishop
from king   import King
from knight import Knight
from pawn   import Pawn
from queen  import Queen
from rook   import Rook

class Chess:

    command_list = []

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
            'cursor_move_left_char': '{',
            'cursor_move_right_char': '}',
            'tile_dark_bg_char': ':',
            'move_marker': '⦁',
            'black_bishop_char':    'b',    # '♝',
            'black_king_char':      'k',    # '♚',
            'black_knight_char':    'n',    # '♞',
            'black_pawn_char':      'p',    # '♟',
            'black_queen_char':     'q',    # '♛',
            'black_rook_char':      'r',    # '♜',
            'white_bishop_char':    'B',    # '♗',
            'white_king_char':      'K',    # '♔',
            'white_knight_char':    'N',    # '♘',
            'white_pawn_char':      'P',    # '♙',
            'white_queen_char':     'Q',    # '♕',
            'white_rook_char':      'R'     # '♖'
        }
        self.player_command = ""

        self.is_help_mode = False

        self.is_piece_selected = False

        self.current_player = 'uppercase'

        self.update_count = 0

        self.cursor_pos = [0,0] # (x,y)
        
        self.selected_tile_pos = []

        for item in kwargs.items():
            setattr( self, item )


        self.setup_game_board()


    def add_command( self, command ):

        # if type(command) == list:
        #     for c in command:
        #         self.command_list.append(command)

        self.command_list.append(command)

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

        print("~" * 42)
        print("Update {}".format(self.update_count))

        if self.is_help_mode == True:
            print("\t\tUppercase")

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


            if y != self.cursor_pos[1]:

                if self.is_piece_selected == True:
            
                    if self.selected_tile_pos == [0, y]:
                        line_x += "{}".format( self.settings['cursor_move_left_char'] )
                    else:
                        line_x += "|"
                else:
                    line_x += "|"

            elif y == self.cursor_pos[1]:

                if self.cursor_pos[0] == 0:

                    if self.selected_tile_pos == [0, y]:
                        line_x += "{}".format( self.settings['cursor_move_left_char'] )
            
                    else:
                        line_x += "{}".format( self.settings['cursor_left_char'] )

                elif self.cursor_pos[0] != 0:

                    if [0, y] == self.selected_tile_pos:
                        line_x += "{}".format( self.settings['cursor_move_left_char'] )
                    else:
                        line_x += "|"


            for x in range( len( self.board[y] ) ):
                # Paint "Contents" of tile
                # If there is nothing on the board tile use bg color

                # if the board tile is empty
                if self.board[y][x] == "":

                    # check state - if there is a piece selected then we want to render it's available move tiles
                    if self.is_piece_selected == True and (x,y) in self.selected_piece.available_tiles:
                        
                        if alt % 2 == 0:
                            line_x += "{}{}".format( self.settings['tile_dark_bg_char'], self.settings['move_marker'] )
                        else:
                            line_x += " {}".format( self.settings['move_marker'] )
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

                alt += 1 # Bg tiles

            output_string += "{}".format( line_x )

            alt += 1 # Bg tiles

            if y <= 7:
                output_string += "\n" # add a newline

            # Help mode text
            if y == 7 and self.is_help_mode == True:
                line_x = "\t"
                coords = ['a','b','c','d','e','f','g','h']

                for x in range( len( self.board[y] ) ):
                    line_x += "  {}".format( coords[x] )

                output_string += "{}\n".format( line_x )


        

        # Print board
        print(output_string)

        if self.is_help_mode == True:
            print("\t\tLowercase")


        # Message Area
        if self.is_piece_selected == True:
            print("Selected: {}. Position: {}, Side: {}".format(
                self.selected_piece.name,
                self.selected_piece.pos,
                self.selected_piece.side))

            print("Available Tiles: {}".format(self.selected_piece.available_tiles))
        
        print("Current player: {}".format(self.current_player))

        print("~" * 42)
        

    def do_command( self, player_command ):

        # Reset help mode
        if self.is_help_mode == True:
            self.is_help_mode = False

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
        if player_command.lower() == "debug":
            print(
"""Command List: {}
""".format(
                self.command_list
            ))

        # Cursor Movement

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
        
        
        # Selecting a Piece on, entering move mode, then selecting it's desination or not

        if player_command.lower() == "x":


            if self.is_piece_selected == True:
                if (self.cursor_pos[0],self.cursor_pos[1]) in self.selected_piece.available_tiles:
                    print("Fantastic! Let's move something.")
                    
                    self.move_piece( self.selected_piece.pos, self.cursor_pos )
                    
                    self.is_piece_selected = False # Deselect piece

                    self.end_turn()

                else:
                    print("Cannot move to that tile.")

                    self.is_piece_selected = False # Deselect piece

            elif self.is_piece_selected == False:
                print("Using piece at {}".format(self.cursor_pos))
                # pick up piece
                self.select_piece()

            

        print("Your command was '{}'. Cursor at {}".format(player_command, self.cursor_pos))
    

    def end_turn( self ):
        print("Ending turn for {}.".format( self.current_player ))

        # Set cursor to players side
        if self.current_player == "uppercase":
            self.current_player = "lowercase"
            self.cursor_pos = [0,7]
        elif self.current_player == "lowercase":
            self.current_player = "uppercase"
            self.cursor_pos = [0,0]


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


    def is_opponent_at_tile( self, tile ):
        # Returns True if opponent player has a piece on the tile
        if type(self.board[ tile[0] ][ tile[1] ]) == str:
            return False

        if self.current_player == self.board[ tile[0] ][ tile[1] ].side:
            return True
        
        return False


    def move_piece( self, src, dest ):

        # Generic move method - this is part of the chess class and not the piece class.
        # This will likely need to be looked at again in future to decide how to implement special moves
        # If the destination is not empty or containing a piece from the same player then move there.

        if self.board[dest[1]][dest[0]] == "" or self.board[dest[1]][dest[0]].side != self.current_player:
            
            self.board[dest[1]][dest[0]] = self.board[src[1]][src[0]]
            
            self.board[dest[1]][dest[0]].pos = (dest[0], dest[1]) # Give it the new position tuple coordinate

            self.board[dest[1]][dest[0]].moved()

            self.board[src[1]][src[0]] = "" # now that the piece has moved the board src tile is set to blank


    def new_piece( self, char = "", pos = (0,0), side = "" ):
        # Returns a new instance of a pieces class based on the string given to this method

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


    # Sets up the two dimensional array for referencing the game pieces
    def setup_game_board( self ):
 
        self.board = []
        for y in range( self.settings[ 'max_y' ] ):
            line_x = []
            
            for x in range( self.settings[ 'max_x' ] ):
                line_x.append( "" ) # Empty board tiles are empty strings
            
            self.board.append( line_x )

        # Just in case we add more game modes with odd setups
        if self.settings['game_mode'] == 'normal':

            # board_setup_stack = ['r','n','b','k','q','b','n','r'] # array of pieces
            board_setup_stack = [
                [
                    self.settings['black_rook_char'],
                    self.settings['black_knight_char'],
                    self.settings['black_bishop_char'],
                    self.settings['black_king_char'],
                    self.settings['black_queen_char'],
                    self.settings['black_bishop_char'],
                    self.settings['black_knight_char'],
                    self.settings['black_rook_char']
                ],[
                    self.settings['white_rook_char'],
                    self.settings['white_knight_char'],
                    self.settings['white_bishop_char'],
                    self.settings['white_king_char'],
                    self.settings['white_queen_char'],
                    self.settings['white_bishop_char'],
                    self.settings['white_knight_char'],
                    self.settings['white_rook_char']
                ]]


            for tile in range( len( self.board[0] ) ):
                #char = board_setup_stack[tile]
                self.board[0][tile] = self.new_piece( board_setup_stack[1][tile], (tile, 0), "uppercase" ) # .upper()
            
            for tile in range( len( self.board[1] ) ):
                self.board[1][tile] = Pawn( char = self.settings['white_pawn_char'], pos = (tile, 1), side = "uppercase" ) # P
            
            for tile in range( len( self.board[6] ) ):
                self.board[6][tile] = Pawn( char = self.settings['black_pawn_char'], pos = (tile, 6), side = "lowercase" ) # p
            
            for tile in range( len( self.board[7] ) ):
                self.board[7][tile] = self.new_piece( board_setup_stack[0][tile], (tile, 7), "lowercase" )



    def select_piece( self ):
        x = self.cursor_pos[0]
        y = self.cursor_pos[1]
        
        # If nothing is selected, select nothing
        if self.board[y][x] == "":
            print("Nothing to select")
            self.is_piece_selected = False
            return False

        if self.current_player != self.board[y][x].side:
            if self.is_piece_selected == False:
                print("Cannot select the other player's piece.")
                return False
            else:
                print("Taking enemy pieces is not yet implemented! Sorry :O")
                return False

        self.is_piece_selected = True

        # trigger the select method on the piece and pass in the game board
        self.board[y][x].select( board = self.board, current_player = self.current_player ) 
    
        self.selected_piece = self.board[y][x]
        print("Selected: {}. Position: {}, Side: {}".format(
            self.selected_piece.name,
            self.selected_piece.pos,
            self.selected_piece.side))


        self.selected_tile_pos = [x,y]

        # Set up possible moves (must send the chess board to this method)
        #self.selected_piece.get_possible_moves( board = self.board, current_player = self.current_player  )


    # Run a "Frame" or execute a turn
    def update( self ):

        # Display chess board
        self.display()

        # Get input
        self.player_command = input("Enter a command: ")
        self.add_command( self.player_command )

        # Do command
        # If the command list is not empty, pop a command and do it.
        if self.command_list != []:
            self.do_command(self.command_list.pop())
        

        self.update_count += 1