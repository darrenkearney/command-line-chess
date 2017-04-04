# Command Line Chess
# Author: Darren Kearney
# https://github.com/darrenkearney

from chess import Chess


def main():

    motd = "An unintuitive chess game."

    print("""

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