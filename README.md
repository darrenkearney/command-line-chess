# command-line-chess

This is a chess game you can play in the terminal. It's a small python project which I started for 1GAM Galway and will be working on casually in my spare time.
Tested using gnome-terminal on Linux (Arch & Ubuntu).

Lot's of work still left to do before it's playable. So far it's only 2 player hotseat and only the Pawn pieces are someway coded!

### Installation:
1. Open your terminal and navigate to a folder you want to store your game in.
2. Download it from github.

### Running a new Game
1. Move into the project directory.
2. Run `python app.py` and follow on screen instructions. Type help when in-game to get help information.
 
Here are the commands:

```bash
git clone https://github.com/darrenkearney/command-line-chess
cd command-line-chess
python app.py
```

### How to play

Start a new game from the game menu or load a saved game.

Instructions:

        In order to play command line chess, you need to use the commands below.

        **Type one command at a time** followed by the Enter/Return Key.

    Commands:

        help / h / ?    Help (display this menu)

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

    To Select Piece Under Cursor:

        x               Selects the piece under the cursor, like picking it up.
                        Once selected, move the cursor to where you want to put
                        the piece.
    Move Piece

        x               Must have a piece selected. Then enter 'x' again to attempt to place it.
                        Pieces should only be placed on legal tiles. Let me know if there are any wierd bugs!


Future goals:
- [x] 1. Make a full game of chess possible with basic movesets (and a bit of trust from the player!)
- [ ] 2. Enforce all standard chess rules. (Nearly there!)
- [ ] 3. To integrate an open source AI chess engine as an include/dependancy.

Your (constructive) feedback is quite welcome!
