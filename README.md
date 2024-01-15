# Wordle

This repository contains two Python scripts to play a Wordle-like game. The first script (`wordle.py`) implements a console-based version of the game, while the second script (`runner.py`) provides a graphical user interface using Pygame.

## Files

- `wordle.py`: A console-based implementation of the Wordle game.
- `runner.py`: A Pygame-based graphical version of the Wordle game.

## wordle.py

![WORDLE_GUI](wordle_gui.webp)

### Description

This script defines two classes, `WordList` and `WordleGame`, to manage the word list and game logic, respectively.

- `WordList`: Handles loading a word list from a file and selecting a random word.
- `WordleGame`: Manages the game logic, including word guessing, scoring, and displaying results.

### Usage

To play the console version, run `wordle.py`. You'll be prompted to enter a word size (5 to 8 letters) and then to guess the word.

## runner.py

### Description

This script utilizes the Pygame library to create a graphical user interface for the Wordle game.

- `WordlePygame`: A class that manages the game's UI, including drawing elements on the screen, handling user input, and transitioning between different screens.

### Usage

To play the graphical version, ensure Pygame is installed and run `runner.py`. You can select the word size from the main menu and then play the game using a graphical interface.

## Requirements

- Python 3
- Pygame (for the graphical version)

To install Pygame, run:

```bash
pip install pygame
