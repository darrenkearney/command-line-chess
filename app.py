#!/usr/bin/env python
# Command Line Chess
# Author: Darren Kearney
# https://github.com/darrenkearney

from chess import Chess
import random

# # To do.
# 1. Finish check state rules
#   1.1 
#
#
# 2. Add algebraic notation translator to allow player to input their desired move
#   2.1 Give feedback on bad/illegal/error moves 
#
#
# 3. Add a (verbose) input mode switcher to turn off cursor display.
#
# 4. Make different views - DONE!
#
# 5. Add more prettiness / polish
#   5.1 Research how to package the project as a standalone app
#   5.2 Implement findings to bring the project up to something that can be run as easily as possible
#
# 6. Road to Release
#   6.1 Add authorship info to all files
#   6.2 Add a license, include it within all files
#   6.3 
#
class App():

    def __init__( self ):

        self.chess = Chess()

        self.is_game_running = False

        self.get_view('MAIN_MENU')


    def input_int( self, message = '' ):
        # A handy reusable way of getting int from player/user

        while True:
            try:
                choice = input("{}\n > ".format(message))
                choice = int(choice)

            except ValueError:
                print("{} is not a number.".format(choice))
                continue

            except KeyboardInterrupt:
                print("Exiting menu.")
                return None

            else:
                return choice


    def get_view( self, view ):
        
        if view == 'MAIN_MENU':
            return self.main_menu()

        elif view == 'SETTINGS':
            return self.settings()

        # elif view == 'GRAPHICS_SETTINGS':
        #     return self.graphics_settings()

        # elif view == 'GAME_SETTINGS':
        #     return self.chess_settings()

        else:
            print("View not found.")
            return self.maing_menu()


    def main_menu( self ):

        motd = "An unintuitive chess game by Darren Kearney."

        # Fancy ascii art
        title_art = """
        8\"\"\"\"8                                            8                   
        8    \" eeeee eeeeeee eeeeeee eeeee eeeee eeeee    8     e  eeeee eeee 
        8e     8  88 8  8  8 8  8  8 8   8 8   8 8   8    8e    8  8   8 8    
        88     8   8 8e 8  8 8e 8  8 8eee8 8e  8 8e  8    88    8e 8e  8 8eee 
        88   e 8   8 88 8  8 88 8  8 88  8 88  8 88  8    88    88 88  8 88   
        88eee8 8eee8 88 8  8 88 8  8 88  8 88  8 88ee8    88eee 88 88  8 88ee 
                                                                              
                             8\"\"\"\"8                                           
                             8    \" e   e eeee eeeee eeeee                    
                             8e     8   8 8    8   \" 8   \"                    
                             88     8eee8 8eee 8eeee 8eeee                    
                             88   e 88  8 88      88    88                    
                             88eee8 88  8 88ee 8ee88 8ee88                    
                                                                          
    """

        lines = title_art.split('\n')
        title_string = ""

         # Nice gradient start points
        gradients = [28,40,178,190,220]
        # Pick a random colour
        r_gradient = random.choice(gradients)

        # Let's add a splash of colour using our gradient start point
        for line in lines:
            title_string += "{}{}{}{}{}".format('\u001b[38;5;', str(r_gradient + int(lines.index(line) * 0.9 )), 'm', line,'\u001b[0m\n')

        print(u"\n{}\n".format(title_string))
        print("\n    {}\n    https://github.com/darrenkearney/command-line-chess\n".format(motd))


        self.available_options = [1,2,3,9,0]

        if self.is_game_running == False:
            self.available_options.remove(2)
            resume_msg = "(Not available)"
        else:
            resume_msg = ''
            

        choice_menu = """{}

    Start menu:

        1)  Start a new game
        2)  Resume current game {}
        3)  Load a saved game

        9)  Options
        0)  Quit

""".format("~"*42, resume_msg )



        choice = self.input_int( choice_menu )

        if choice == 1:
            # Initialize new game of chess 
            self.chess = Chess()

            # Clean up menu options
            self.is_game_running = True
            self.available_options.append(2)

            # Run the game
            self.run_chess(self.chess)

        elif choice == 2:
            self.run_chess(self.chess)

        elif choice == 3:
            self.chess.do_command('load')
            self.run_chess(self.chess)

        elif choice == 9:
            self.get_view("SETTINGS")

        elif choice == 0:
            print("\n Thanks for playing. Bye! \n")
            exit()

        elif choice not in available_options:
            choice = self.input_int( choice_menu )


    def run_chess( self, chess ):

        chess.turn_count = 0
        is_playing = True

        try:
            # The main game loop
            while is_playing:

                chess.update()

                # Get input
                command = input(" > ")

                if command == "menu":
                    self.get_view("MAIN_MENU")
                if command == "graphics":
                    self.get_view("GRAPHICS_SETTINGS")
                else:
                    self.chess.command == command

                self.chess.add_command( command )

                # Do command (such as move)
                # If the command list is not empty, pop a command and do it.
                if self.chess.command_list != []:
                    self.chess.do_command(self.chess.command_list.pop())

                # update the current state of board
                self.chess.update_state_of_board()

            
                if chess.state['CHECKMATE'] == True:
                    is_playing = False
            else:
                chess.do_command('exit')
                
        except KeyboardInterrupt:
            chess.do_command('exit')
        else:
            print("Game exited.")


    def settings( self ):
        
        choice_menu = """{}

      ~ Opps. No options available just yet! ~

        1)  Graphics:

            -) Chess font characters
            -) Colour Options

        2)  Game Settings:

            -) Enter new player name
        
        0)  Back to Main Menu

""".format("~"*42)
        choice = self.input_int( choice_menu )

        if choice == 0:
            self.get_view('MAIN_MENU')

        elif choice == 1:
            self.get_view('GRAPHICS_SETTINGS')

        elif choice == 2:
            self.get_view('GAME_SETTINGS')

        elif choice not in [0,1,2]:
            choice = self.input_int( choice_menu )


# Run the game
App()