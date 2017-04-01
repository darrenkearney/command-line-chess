# Command Line Chess
# Author: Darren Kearney
# https://github.com/darrenkearney

from chess import Chess


def main():

    print("\nLet's play chess.\n")

    while True:
        try:
            choice = input(
"""
    Would you like to:

        1)  New game
        2)  Load a saved game
        3)  Quit

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
                game.do_command('exit')

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