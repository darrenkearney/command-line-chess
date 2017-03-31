# Chess
# Author: Darren Kearney

from chess import Chess


def main():

    # The main game loop
    is_playing = True

    game = Chess()
    game.turn_count = 0

    print("\nLet's play chess.\n")

    # This command menu      
    print(game.get_help_menu())

    try:
        while is_playing:

            game.update()
        
            if game.state['CHECKMATE'] == True:
                is_playing = False
        else:
            print("\nThanks for playing chess. Goodbye!\n")
            exit()
            
    except KeyboardInterrupt:
        print("\nThanks for playing chess. Goodbye!\n")
        exit()

main()