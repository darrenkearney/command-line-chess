from piece  import Piece
from bishop import Bishop
from king   import King
from knight import Knight
from pawn   import Pawn
from queen  import Queen
from rook   import Rook
import io    #
import json  # These imports are for saving and loading games to files
import os    #


class Chess:

    command_list = []

    # Initialize
    def __init__( self, **kwargs ):

        # Initialize Default Settings & states

        self.command = ""
        self.current_player = 'uppercase' # lowercase start needs to be fixed
        self.cursor_pos = [0,0] # [4,6] # (x,y)
        self.debug_logs = []

        self.is_debug_mode = False
        self.is_help_mode = False
        self.is_piece_selected = False
        self.is_turn_ended = False

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
        
        self.selected_tile_pos = []
        
        self.settings = {
            'players': 2,
            'game_mode': "normal",
            'graphics': 'colourful', # colourful or normal
            'max_x': 8,
            'max_y': 8,
            'cursor_left_char': '>',
            'cursor_right_char': '<',
            'cursor_move_left_char':'{',
            'cursor_move_right_char':'}',
            'tile_light_bg_char':   ':',
            'tile_light_bg_colour': '\u001b[48;5;240m',
            'tile_edge_char':       '|',
            'tile_edge_colour':     '\u001b[38;5;236m', # '\u001b[48;5;232m',
            'move_marker':          '⦁',
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
            'white_rook_char':      'R',    # '♖',
            'save_file_extension': '.savegame'
        }

        self.state = {
            'CHECKMATE': False
        }

        self.update_count = 0

        # Override defaults with given values
        for key, value in kwargs.items():
            setattr( self, key, value )

        # If given a command on init, hop to and do it (such as 'load')
        if self.command != "":
            self.do_command( self.command )

        # Otherwise, we'll start a new game (with defaults & overrides)
        else:
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


    def debug_log( self, message ):

        if self.is_debug_mode != True:
            return

        # Add it to a list of debug messages
        self.debug_logs.append(message)

        # Out the message as it happens
        print(message)


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

        if self.settings['graphics'] == 'colourful':
            tile_light_bg = '{} '.format(self.settings['tile_light_bg_colour'])
            tile_edge = '{}{}{}'.format(self.settings['tile_edge_colour'],self.settings['tile_edge_char'], '\u001b[0m')
            move_marker = '{}'.format(self.settings['move_marker'])
        else:
            tile_light_bg = self.settings['tile_light_bg_char']
            tile_edge = '{}'.format(self.settings['tile_edge_char'])
            move_marker = self.settings['move_marker']


        # Let's run a loop over all the tiles of all the rows on the board
        # Filling in the characters as appropriate to their state
        for y in range( len(self.board) ):
            # Paint "Left" side of tile (we will hereafter append the tile edges to the tile content)
            # check to see of the first tile on a row is selected, if so paint the tile edge/border appropriately
            
            line_x = "\t" # Reset line_x for constructing new line

            # Actually going to set the colours for each row
            if self.settings['graphics'] == 'colourful':
                # If set to colour, we'll programmatically add a little gradient
                colour_gradient = '{}'.format( '\u001b[48;5;'+str(235+int((y*2+1)/2))+'m' )
                tile_light_bg = '{} '.format( colour_gradient )
                tile_edge = '{}{}{}'.format( colour_gradient, self.settings['tile_edge_char'], '\u001b[0m')

            if self.is_help_mode == True:
                line_x = "      {} ".format( 8 - y )

            if y != self.cursor_pos[1]:

                if self.is_piece_selected == True:

                    if self.selected_tile_pos == [0, y]:
                        line_x += "{}".format( self.settings['cursor_move_left_char'] )
                    else:
                        line_x += "{}".format(tile_edge)
                else:
                    line_x += "{}".format(tile_edge)

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
                        line_x += "{}".format(tile_edge)

            for x in range( len( self.board[y] ) ):
                # Paint "Contents" of tile
                # If there is nothing on the board tile use bg color

                # if the board tile is empty
                if self.board[y][x] == "":

                    # check state - if there is a piece selected then we want to render it's available move tiles
                    if self.is_piece_selected == True and (x,y) in self.selected_piece.available_tiles:
                        
                        if alt % 2 == 0:
                            
                            if self.settings['graphics'] == 'colourful':
                                line_x += '{}'.format(colour_gradient)

                                line_x += "{}{}".format( move_marker, ' ' )
                                # Reset the ANSI colour codes
                                line_x += '\u001b[0m'
                            else:
                                line_x += "{}{}".format( move_marker, tile_light_bg )
                        else:
                            line_x += "{} ".format( move_marker )
                    else:

                        if alt % 2 == 0:
                            line_x += "{}{}".format( tile_light_bg, tile_light_bg )
                            # Reset the ANSI colour codes
                            if self.settings['graphics'] == 'colourful':
                                line_x += '\u001b[0m'
                        else:
                            line_x += "  " # Empty blank tile

                else:
                    
                    if alt % 2 == 0:
                        if self.is_piece_selected == True and [x,y] in self.selected_piece.available_tiles:
                            line_x += "{}{}".format( "x", self.board[y][x] )
                        else:
                            line_x += "{}{}".format( tile_light_bg, self.board[y][x] )
                            # Reset the ANSI colour codes
                            if self.settings['graphics'] == 'colourful':
                                line_x += '\u001b[0m'

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
                            line_x += "{}".format(tile_edge)

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
                        line_x += "{}".format(tile_edge)

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
        print(u"{}".format(output_string))

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
                
            if self.player_info[player]['is_in_check'] == True:
                str_ = 'is'
            else:
                str_ = 'is not'
            print("{} {} in check.".format( player, str_ ))
            print("{} has taken pieces: {}".format(player, self.player_info[player]['pieces_taken']))

        print("Current player: {}".format(self.current_player))

        print("~" * 42)


    def do_command( self, command ):
        # Executes command assigned to given string

        #
        # Reset help mode
        #
        if self.is_help_mode == True:
            self.is_help_mode = False

        if command == "":
            print("None")
            command = "None"

        if command.lower() in ["h", "help", "?"]:
            self.is_help_mode = True
            print("{}".format(self.get_help_menu()))

        if command.lower() == "debug":
            if self.is_debug_mode == True:
                self.is_debug_mode = False
            elif self.is_debug_mode == False:
                self.is_debug_mode = True

            #print("{}".format(self.get_debug_log()))

        #
        # Save
        #
        if command == "save":
            self.save_game()
            
        #
        # Load
        #
        if command == "load":
            self.load_game()

        #
        # Forfeit
        #
        if command == "forfeit":
            self.forfeit()

        #
        # Quit / Exit Game
        #
        if command == "exit" or command == "quit":
            print("\nThanks for playing chess. Goodbye!\n")
            exit()

        #
        # Cursor Movement
        #
        if command.lower() == "s":
            print("Down")
            if self.cursor_pos[1] < len(self.board) - 1:
                self.cursor_pos[1] += 1

        if command.lower() == "w":
            print("Up")
            if self.cursor_pos[1] > 0:
                self.cursor_pos[1] -= 1

        if command.lower() == "a":
            print("Left")
            if self.cursor_pos[0] > 0:
                self.cursor_pos[0] -= 1

        if command.lower() == "d":
            print("Right")
            if self.cursor_pos[0] < len(self.board[self.cursor_pos[1]]) - 1:
                self.cursor_pos[0] += 1

        #
        # Selecting a Piece on, entering move mode, then selecting it's desination or not
        #
        if command.lower() == "x":

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
                self.select_piece( coords = self.cursor_pos )

        print("Your command was '{}'. Cursor at {}".format(command, self.cursor_pos))


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


    def forfeit( self ):
        # The current player has forfeited the match.
        # Anything that needs to get tidied up can get done here.

        # Set the winner
        self.winner = self.get_opposite_player()

        print("\n{}\n{} has forfeited the match. {} wins.\n".format(
            '~'*42,
            self.current_player,
            self.get_opposite_player()
        ))

        return


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
        return "Command List: {},\nLogs: {}".format(self.command_list, self.debug_logs)


    def get_debug_log_of_piece( self, piece ):
        return piece.debug_log


    def get_help_menu( self ):

        return """
Help menu

    Instructions:

        In order to play command line chess, you need to use the commands below.
        It takes one command at a time. To enter a command type the letter or
        word and press the Enter Key. 

    Commands:

        help / h / ?    Help (display this menu) = h / ? / help

        forfeit         Declare your opponent the winner.

        menu            Return to Main menu.
        
        save            Save current game to file (in saves/ directory).
        
        load            Load game from file.
        
        debug           Turn on/off debug mode. (Handy for Darren!)

        exit            Exit the game immediately (without saving)

    Cursor Movement:

        w               Up
        s               Down
        a               Left
        d               Right

    To Select A Piece:

        x               Press x over the piece to select it, or pick it up. 
                        Once selected, move the cursor to where you want to put
                        the piece, then enter 'x' again to place it. Pieces
                        should only successfully place on legal tiles. Let me
                        know if there are any wierd bugs!
"""


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

                self.debug_log("@@@@ piece at tile. piece.name = {}, p.side = {}".format(p.name.lower(), p.side))

                if p.name.lower() == 'king' and p.side == self.get_opposite_player(player):
                        # If king is present set opponent's check to True

                        self.debug_log("@@@@ Piece {} causes Check! ! ! ! !".format(piece))

                        return True
     
        self.debug_log("@@@@ Piece {} not causing Check!".format(piece))

        return False


    def is_piece_at_tile( self, coords ):

        # Returns True if opponent player has a piece on the tile
        
        if type(self.board[coords[1]][coords[0]]) == str:
            return False

        if self.board[coords[1]][coords[0]].side in ["uppercase", "lowercase"]:
            self.debug_log("+-+-+-+-+-+-+    Something at tile {} and it's type is {}".format(coords, type(self.board[coords[1]][coords[0]]) ))
            return True

        return False


    def load_game( self ):
        print("WARNING! THIS FEATURE IS INCOMPLETE!")

        path = os.path.dirname(os.path.abspath(__file__))
        path = path + '/saves/'

        save_files = os.listdir(path)
        saves = []
        for save in save_files:
            if '.' in save:
                save = save.split('.')
                if save[1] == 'savegame':
                    saves.append(save[0])

        save_str_ = ''
        for save in saves:
            save_str_ += "\t{}) {}\n".format( saves.index(save) + 1, save)

        print("Pick a save to load:\n{}".format( save_str_ ))

        choice = self.input_int()
        if choice == None:
            print("No save game was chosen, so we'll go back.")
            return None

        save_name = saves[choice-1]
        path = path + '{}{}'.format(save_name, self.settings['save_file_extension'])

        print("Loading...")

        # load_file = open(path,'rt')
        # save_game = load_file.read()
        # load_file.close()

        # Read JSON file
        with open(path) as data_file:
            data_loaded = json.load(data_file)

        self.current_player = data_loaded['current_player']

        # Set up board
        self.setup_game_board(data_loaded['board'])

        self.player_info['uppercase']['pieces_taken'] = data_loaded['player_info']['uppercase']['pieces_taken']
        self.player_info['lowercase']['pieces_taken'] = data_loaded['player_info']['lowercase']['pieces_taken']
        self.player_info['uppercase']['last_cursor_pos'] = data_loaded['player_info']['uppercase']['last_cursor_pos']
        self.player_info['lowercase']['last_cursor_pos'] = data_loaded['player_info']['lowercase']['last_cursor_pos']
        self.cursor_pos = data_loaded['cursor_pos']

        print("Here is the loaded file data \n{}".format(data_loaded))


    def input_int( self ):
        # A handy reusable way of getting int from player/user

        while True:
            try:
                choice = input(" > ")
                choice = int(choice)

            except ValueError:
                print("{} is not a number.".format(choice))
                continue

            except KeyboardInterrupt:
                print("Exiting menu.")
                return None

            else:
                return choice


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


    def save_game( self ):
        # Save a game to file.
        # Saves in saves/ subfolder of game directory.
        # Uses .savegame extension by default ( set in game settings )
        print("WARNING! THIS FEATURE IS INCOMPLETE!")

        save_name = input(" Enter save name: ")

        path = os.path.dirname(os.path.abspath(__file__))
        path = path + '/saves/{}{}'.format(save_name, self.settings['save_file_extension'])

        print("Saving...")

        # Define data to save

        data = {
            'board': self.get_board_string(),
            'current_player': self.current_player,
            'cursor_pos': self.cursor_pos,
            'player_info': {
                'lowercase': {
                    'name': self.player_info['lowercase']['name'],
                    'pieces_taken': self.player_info['lowercase']['pieces_taken'],
                    'last_cursor_pos': self.player_info['lowercase']['last_cursor_pos']
                },
                'uppercase': {
                    'name': self.player_info['uppercase']['name'],
                    'pieces_taken': self.player_info['uppercase']['pieces_taken'],
                    'last_cursor_pos': self.player_info['uppercase']['last_cursor_pos']
                }
            }
        }

        try:
            to_unicode = unicode
        except NameError:
            to_unicode = str

        # Write JSON file
        with io.open(path,'wt', encoding='utf8') as save_file:
            str_ = json.dumps(data,
                              indent=4,
                              sort_keys=True,
                              separators=(',',':'),
                              ensure_ascii=False)

            save_file.write(to_unicode(str_))

        print("Saved.")


    def select_piece( self, coords = None):

        if coords == None:
            x = self.cursor_pos[0]
            y = self.cursor_pos[1]
        else:
            x = coords[0]
            y = coords[1]

        # If nothing is selected, select nothing
        if self.board[y][x] == "":
            print("Nothing to select")
            self.is_piece_selected = False
            return False

        if self.current_player != self.board[y][x].side:
            if self.is_piece_selected == False:
                print("Cannot select the other player's piece. (You: {}, Piece: {})".format(self.current_player, self.board[y][x].side))
                return False
            else:
                print("Taking enemy pieces is not yet implemented properly! Sorry :O")
                return False

        # Tell the game that a piece is selected
        self.is_piece_selected = True

        # trigger the select method on the piece and pass in the game board
        self.board[y][x].select( board = self.board, player = self.current_player )

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


    def setup_game_board( self, game_board_string = None ):
        # Sets up the two dimensional array for referencing the game pieces


        if game_board_string != None:
            # In the event of a game is being loaded

            # Reset board
            self.board = []
            self.player_info["uppercase"]['pieces'] = []
            self.player_info["lowercase"]['pieces'] = []

            for y in range(0, 8):
                line_x = []

                for x in range(0, 8):
                    line_x.append( "" ) # Empty board tiles are empty strings

                self.board.append( line_x )

            # Set up piece validator against settings
            board_setup_validator = [
            [
                self.settings['black_bishop_char'],
                self.settings['black_king_char'],
                self.settings['black_knight_char'],
                self.settings['black_pawn_char'],
                self.settings['black_queen_char'],
                self.settings['black_rook_char']
            ],[
                self.settings['white_bishop_char'],
                self.settings['white_king_char'],
                self.settings['white_knight_char'],
                self.settings['white_pawn_char'],
                self.settings['white_queen_char'],
                self.settings['white_rook_char']
            ]]

            game_board_split = game_board_string.split()

            for y in range( len(self.board[y]) ):

                for x in range( len(self.board[y]) ):

                    self.debug_log("@@@@ game_board_split[y][x] = {}".format(game_board_split[y][x]))

                    if game_board_split[y][x] in board_setup_validator[0]:
                        self.board[y][x] = self.new_piece( char = game_board_split[y][x], pos = (x, y), side = "lowercase" )
                        self.player_info["lowercase"]['pieces'].append(self.board[y][x])

                    elif game_board_split[y][x] in board_setup_validator[1]:
                        self.board[y][x] = self.new_piece( char = game_board_split[y][x], pos = (x, y), side = "uppercase" )
                        self.player_info["uppercase"]['pieces'].append(self.board[y][x])

                    elif game_board_split[y][x] == 0:
                        self.board[y][x] = ""

            return "Board data loaded into game."

        elif game_board_string == None:
            # Just in case we add more game modes with odd setups
            if self.settings['game_mode'] == 'normal':

                self.board = []

                for y in range( self.settings[ 'max_y' ] ):
                    line_x = []

                    for x in range( self.settings[ 'max_x' ] ):
                        line_x.append( "" ) # Empty board tiles are empty strings

                    self.board.append( line_x )

                # board_setup_stack = ['r','n','b','k','q','b','n','r'] # array of pieces
                board_setup_stack = [
                    [
                        self.settings['black_rook_char'],
                        self.settings['black_knight_char'],
                        self.settings['black_bishop_char'],
                        self.settings['black_queen_char'],
                        self.settings['black_king_char'],
                        self.settings['black_bishop_char'],
                        self.settings['black_knight_char'],
                        self.settings['black_rook_char']
                    ],[
                        self.settings['white_rook_char'],
                        self.settings['white_knight_char'],
                        self.settings['white_bishop_char'],
                        self.settings['white_queen_char'],
                        self.settings['white_king_char'],
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

                self.debug_log("Uppercase pieces after board set up: {}".format(self.player_info[self.current_player]['pieces']))

            return "New board set up."


    def update( self ):
        # Run a "Frame" (typically on executing a command)

        # Display chess board
        self.display()

        ###
        ### Commented out as we will pass input into the chess class via the app.py
        ###
        # # Get input
        # self.command = input(" > ")
        # self.add_command( self.command )

        # # Do command (such as move)
        # # If the command list is not empty, pop a command and do it.
        # if self.command_list != []:
        #     self.do_command(self.command_list.pop())

        # # update the current state of board
        # self.update_state_of_board()

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
        self.debug_log("@@@@ {} check pieces {}".format(self.current_player, self.player_info[self.current_player]['check_pieces']))
        self.debug_log("@@@@ {} check pieces {}".format(self.get_opposite_player(), self.player_info[self.get_opposite_player()]['check_pieces']))

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
