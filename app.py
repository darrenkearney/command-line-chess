#!/usr/bin/env python
# Command Line Chess
# Author: Darren Kearney
# https://github.com/darrenkearney

from chess import Chess

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
#
# 4. Make a new App class, or Game class, which inherits the chess class.
# It's main function is to MANAGE the VIEWS. This way we can easily switch views and return to the same Chess instance
#
#   Run App(Chess) 
#      \
#       [Node]                  Main Menu:  the start menu that holds top level menu options
#        |\
#        | [Node]            Game view: the chess board          
#         \     
#          [Node]              Settings Menu
#            \
#             [Node]        Graphics Settings
#              |\
#              | [Node]    Visual confirmation test - Display game board with new settings, ask if everything appeared ok.
#               \
#                [Node]        Gameplay Settings
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

def main():

    motd = "An unintuitive chess game."

    print(u"""

   ___  __   _  _  _  _   __   __ _  ____    __    __  __ _  ____     ___  _  _  ____  ____   ____ 
  / __)/  \ ( \/ )( \/ ) / _\ (  ( \(    \  (  )  (  )(  ( \(  __)   / __)/ )( \(  __)/ ___) / ___)
-( (__(  O )/ \/ \/ \/ \/    \/    / ) D (--/ (_/\ )( /    / ) _)---( (__ ) __ ( ) _) \___ \ \___ \-
  \___)\__/ \_)(_/\_)(_/\_/\_/\_)__)(____/  \____/(__)\_)__)(____)   \___)\_)(_/(____)(____/ (____/

""")
    print("\n\t{}\n\n".format(motd))

    while True:
        print("~"*42)
        try:
            choice = input(
"""
    Start menu:

        1)  New game
        2)  Load a saved game
        3)  Options

        0)  Quit

 > """)
            choice = int(choice)
        except ValueError:
            print("'{}' is not a number!".format(choice))

        else:
            if choice == 1:
                # Run chess 
                game = Chess()
                run_game(game)

            elif choice == 2:
                game = Chess(command='load')
                run_game(game)

            elif choice == 3:
                print("~"*42)
                print(
"""
  ~ Opps. No options available just yet! ~

    Graphics:

        -) Alphabet characters
        -) Chess font characters

    Settings:

        -) Enter new player name

""")
                continue

            elif choice == 0:
                print("\n Thanks for playing. Bye! \n")
                exit()

            else:
                continue

def run_game( game ):

    game.turn_count = 0
    is_playing = True

    try:
        # The main game loop
        while is_playing:

            game.update()
        
            if game.state['CHECKMATE'] == True:
                is_playing = False
        else:
            game.do_command('exit')
            
    except KeyboardInterrupt:
        game.do_command('exit')
    else:
        print("Game exited.")

# Run the game
main()
