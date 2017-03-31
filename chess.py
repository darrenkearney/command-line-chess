from piece  import Piece
from bishop import Bishop
from king   import King
from knight import Knight
from pawn   import Pawn
from queen  import Queen
from rook   import Rook
import os

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

        self.is_turn_ended = False

        self.current_player = 'uppercase'

        self.player_info = {
            self.current_player : {
                'check_pieces' : [],    # Player pieces causing opponent's Check
                'is_in_check': False,
                'last_cursor_pos': [0,0],
                'name': "Player 1",
                'pieces_taken': [],
                'pieces': []
            },
            self.get_opposite_player() : {
                'check_pieces' : [],
                'is_in_check': False,
                'last_cursor_pos': [7,7],
                'name': "Player 2",
                'pieces_taken': [],
                'pieces': []
            }
        }

        self.update_count = 0

        self.cursor_pos = [0,0] # (x,y)
        
        self.selected_tile_pos = []

        self.state = {
            'CHECKMATE': False
        }

        for item in kwargs.items():
            setattr( self, item )

        self.setup_game_board()


    def add_command( self, command ):

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

                    if self.selected_tile_pos == [0, y] and self.is_piece_selected == True:
                        line_x += "{}".format( self.settings['cursor_move_left_char'] )

                    else:
                        line_x += "{}".format( self.settings['cursor_left_char'] )

                elif self.cursor_pos[0] != 0:

                    if [0, y] == self.selected_tile_pos and self.is_piece_selected == True:
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

        #
        # Message / Debug Area
        #

        if self.is_piece_selected == True:
            print("Selected: {}. Position: {}, Side: {}".format(
                self.selected_piece.name,
                self.selected_piece.pos,
                self.selected_piece.side))

            print("Available Tiles: {}".format(self.selected_piece.available_tiles))

            # Display who is in a Check state
            for player in [self.current_player, self.get_opposite_player()]:
                
                print("{} is_in_check: {}".format( player, self.player_info[player]['is_in_check'] ))
                
                print("{} has taken pieces: {}".format(player, self.player_info[player]['pieces_taken']))

        print("Current player: {}".format(self.current_player))

        print("~" * 42)


    def do_command( self, player_command ):

        #
        # Reset help mode
        #

        if self.is_help_mode == True:
            self.is_help_mode = False

        if player_command == "":
            print("None")
            player_command = "None"

        if player_command.lower() in ["h", "help", "?"]:
            self.is_help_mode = True
            print("{}".format(self.get_help_menu()))

        if player_command.lower() == "debug":
            print("{}".format(self.get_debug_log()))

        #
        # Save
        #
        if player_command == "save":
            player_command = "Save Game"
            print("THIS FEATURE IS INCOMPLETE. WARNING!")
            
            file_name = input(" Enter save name: ")

            path = os.path.dirname(os.path.abspath(__file__))            
            path = path + '/saves/{}.csv'.format(file_name)

            print("Saving...")

            save_file = open(path,'wt')
            save_game = self.get_board_string()
            save_game += "current_player,{}\n".format(self.current_player)
            save_file.write(save_game)
            save_file.close()
            
            print("Saved.")

        #
        # Load
        #
        if player_command == "load":
            print("THIS FEATURE IS INCOMPLETE. WARNING!")
            player_command = "Load Game"
            
            path = os.path.dirname(os.path.abspath(__file__))            
            path = path + '/saves/'

            print("Saves:\n{}".format( os.listdir(path) ) )

            file_name = input(" Enter file name: ")
            path = path + '{}.csv'.format(file_name)

            print("Loading...")

            load_file = open(path,'rt')
            save_game = load_file.read()
            load_file.close()

            print("Here is the loaded file \n{}".format(save_game))


        #
        # Cursor Movement
        #
        
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

                    self.is_turn_ended = True

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

        # Save cursor pos
        self.player_info[self.current_player]['last_cursor_pos'] = self.cursor_pos

        # Get next player
        self.current_player = self.get_opposite_player()

        # Set cursor to players side
        self.cursor_pos = self.player_info[self.current_player]['last_cursor_pos']

        # Reset is turn ended check
        self.is_turn_ended = False


    def get_board_string( self ):

        output_string = ""

        for y in range( len(self.board) ):

            #line_x = "|"
            line_x = ""

            for x in range( len(self.board[y]) ):
                
                # If there is nothing on the board tile use bg color
                if self.board[y][x] == "":

                    line_x +="0"

                else:

                    line_x += "{}".format( self.board[y][x] )
                    

            output_string += "{}\n".format( line_x )
            
        # Return the output string
        return output_string


    def get_debug_log( self ):
        # Add more stuff there
        return "Command List: {}".format(self.command_list)


    def get_opposite_player( self, player = None ):
        # Returns a string of the opposite player to given or current_player
        # or None if neither are defined

        if player == None:
            player = self.current_player

        if player == "uppercase":
            return "lowercase"

        if player == "lowercase":
            return "uppercase"

        if player == "black":
            return "white"

        if player == "white":
            return "black"
    
        return None


    def get_state_of_piece( self, piece ):
        return piece.state_list;


    def is_opponent_at_tile( self, tile ):
        # Returns True if opponent player has a piece on the tile

        if type(self.board[ tile[1] ][ tile[0] ]) == str:
            return False

        if self.get_opposite_player() == self.board[ tile[1] ][ tile[0] ].side:
            return True
        
        return False


    def is_piece_causing_check( self, piece, player = None ):
        # Just a handy way to check if a piece is causing check.
        # Returns True or False

        if player == None:
            player = self.current_player
        
         
        # Detect state
        # Check it's currently available move tiles for presence of king

        available_tiles = piece.get_possible_moves(
            board = self.board,
            player = player
        )

        for tile in available_tiles:

            if self.is_piece_at_tile( tile ) == True:

                p = self.board[tile[1]][tile[0]]

                print("@@@@ piece at tile. piece.name = {}, p.side = {}".format(p.name.lower(), p.side))

                if p.name.lower() == 'king' and p.side == self.get_opposite_player(player):
                        # If king is present set opponent's check to True

                        print("@@@@ Piece {} causes Check! ! ! ! !".format(piece))

                        return True
     
        print("@@@@ Piece {} not causing Check!".format(piece))

        return False


    def is_piece_at_tile( self, coords ):

        # Returns True if opponent player has a piece on the tile
        
        if type(self.board[coords[1]][coords[0]]) == str:
            return False

        if self.board[coords[1]][coords[0]].side in ["uppercase", "lowercase"]:
            print("+-+-+-+-+-+-+    Something at tile {} and it's type is {}".format(coords, type(self.board[coords[1]][coords[0]]) ))
            return True

        return False


    def move_piece( self, src, dest ):

        # Generic move method - this is part of the chess class and not the piece class.
        # This will likely need to be looked at again in future to decide how to implement special moves
        # If the destination is not empty or containing a piece from the same player then move there.

        if self.board[dest[1]][dest[0]] == "" or self.board[dest[1]][dest[0]].side != self.current_player:

            if self.is_opponent_at_tile( dest ) == True:
                print("{} {} takes {} {}.".format(
                    self.player_info[ self.current_player ]['name'],
                    self.board[src[1]][src[0]].name,
                    self.player_info[ self.get_opposite_player() ]['name'],
                    self.board[dest[1]][dest[0]].name
                ))

                # A piece is being taken. Add it to this players list of taken pieces.
                self.player_info[self.current_player]['pieces_taken'].append(self.board[dest[1]][dest[0]].name)


            self.board[dest[1]][dest[0]] = self.board[src[1]][src[0]]
            
            # Give it the new position tuple coordinate
            self.board[dest[1]][dest[0]].pos = (dest[0], dest[1]) 

            # Let the piece know it was moved
            self.board[dest[1]][dest[0]].moved()

            # Update the pieces state list
            self.update_state_of_piece( self.board[dest[1]][dest[0]] )

            # now that the piece has moved the boards src tile is set to blank
            self.board[src[1]][src[0]] = ""


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

        return Piece( char = char, pos = pos, side = side )


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


    def set_state_of_piece( self, piece, state_list ):
        piece.state_list = state_list


    def setup_game_board( self ):
        # Sets up the two dimensional array for referencing the game pieces

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
                self.player_info[self.current_player]['pieces'].append(self.board[0][tile])
            
            for tile in range( len( self.board[1] ) ):
                self.board[1][tile] = Pawn( char = self.settings['white_pawn_char'], pos = (tile, 1), side = "uppercase" ) # P
                self.player_info[self.current_player]['pieces'].append(self.board[1][tile])

            for tile in range( len( self.board[6] ) ):
                self.board[6][tile] = Pawn( char = self.settings['black_pawn_char'], pos = (tile, 6), side = "lowercase" ) # p
                self.player_info[self.get_opposite_player()]['pieces'].append(self.board[6][tile])

            for tile in range( len( self.board[7] ) ):
                self.board[7][tile] = self.new_piece( board_setup_stack[0][tile], (tile, 7), "lowercase" )
                self.player_info[self.get_opposite_player()]['pieces'].append(self.board[7][tile])

            print("Uppercase pieces after board set up: {}".format(self.player_info[self.current_player]['pieces']))


    def get_help_menu( self ):

        return """
Help menu

    Commands:

        help            Help (display this menu) = h / ? / help
        save            Save current game to file (in saves/ directory)
        load            Load game from file

    Cursor Commands:

        w               up
        s               down
        a               left
        d               right

        x               (no selection)   Select Piece at cursor
        x               (piece selected) Move the selected piece to cursor 
"""


    def update( self ):
        # Run a "Frame" (typically on executing a command)

        # Display chess board
        self.display()

        # Get input
        self.player_command = input(" > ")
        self.add_command( self.player_command )

        # Do command (such as move)
        # If the command list is not empty, pop a command and do it.
        if self.command_list != []:
            self.do_command(self.command_list.pop())

        # update the current state of board
        self.update_state_of_board()

        # Increment update count (our version of a time delta)
        self.update_count += 1


    def update_state_of_board( self ):

        ##
        ## Update both players
        ##

        # For each player
        for player in [self.current_player, self.get_opposite_player()]:
            # For each piece owned by player
            for piece in self.player_info[player]['pieces']:

                # Update piece state
                self.update_state_of_piece(piece, player)

                # If this piece has a king in it's available tiles, cause check
                if self.is_piece_causing_check(piece, player) == True:

                    # Add it to list of check causing pieces
                    if piece.pos not in self.player_info[player]['check_pieces']:
                        self.player_info[player]['check_pieces'].append(piece.pos)

                    # If this piece is causing opponent to be in check, set it
                    if self.player_info[self.get_opposite_player(player)]['is_in_check'] == False:
                        self.player_info[self.get_opposite_player(player)]['is_in_check'] = True

                elif self.is_piece_causing_check(piece, player) == False:
                    # If not, remove it from this players list of check pieces
                    if piece.pos in self.player_info[player]['check_pieces']:
                        i = self.player_info[player]['check_pieces'].index(piece.pos)
                        self.player_info[player]['check_pieces'].pop(i)

        # Debug log
        print("@@@@ {} check pieces {}".format(self.current_player, self.player_info[self.current_player]['check_pieces']))
        print("@@@@ {} check pieces {}".format(self.get_opposite_player(), self.player_info[self.get_opposite_player()]['check_pieces']))

        ##
        ##  Do stuff for current player with current check state
        ##

        if self.player_info[self.get_opposite_player()]['is_in_check'] == True:

            for piece in self.player_info[self.current_player]['pieces_taken']:
                if piece.lower() == "king":

                    self.state['CHECKMATE'] = True

                    print("CHECKMATE!")

        ## End players turn if it's done
        if self.is_turn_ended == True:
            self.end_turn()

        #
        #   Update check state
        #

        for player in [self.current_player, self.get_opposite_player()]:
            if len(self.player_info[player]['check_pieces']) == 0:
                self.player_info[self.get_opposite_player(player)]['is_in_check'] = False


    def update_state_of_piece( self, piece, player = None ):
        # Piece specific state management

        if player == None:
            player = self.current_player

        # Get old state
        state_list = self.get_state_of_piece( piece )

        # Is it now causing check?
        is_causing_check = self.is_piece_causing_check( piece, player )

        if is_causing_check == True:
            if "PIECE_CAUSES_CHECK" not in state_list:
                state_list.append("PIECE_CAUSES_CHECK")

        else:
            if "PIECE_CAUSES_CHECK" in state_list:
                state_list.remove("PIECE_CAUSES_CHECK")

        self.set_state_of_piece( piece, state_list )
