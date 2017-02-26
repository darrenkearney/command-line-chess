# Chess
# Author: Darren Kearney

from chess import Chess


def main():

    # The main game loop
    is_playing = True


    game = Chess()
    game.turn_count = 0

    print("Let's play chess.\n")

    game.display()

    try:
        while is_playing:
            game.update()
            
    except KeyboardInterrupt:
        print("\nThanks for playing chess. Goodbye!\n")
        exit()

main()