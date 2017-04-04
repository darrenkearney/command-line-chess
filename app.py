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
