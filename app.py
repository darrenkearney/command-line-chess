# Chess
# Author: Darren Kearney

from chess import Chess




def main():

    # The main game loop
    is_playing = True


    game = Chess()
    game.setup_game_board()
    game.turn_count = 0
    print(game.get_board())

    try:
        while is_playing:
            game.update()
    except KeyboardInterrupt:
        print("\nThanks for playing chess. Goodbye!\n")
        exit()

main()