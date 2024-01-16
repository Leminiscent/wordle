# Wordle
This repository contains a Python implementation of the popular Wordle game, including both a command-line version and a graphical user interface (GUI) version using Pygame.

![WORDLE_GUI](wordle_gui.webp)

## Description

The project is divided into two main parts: `WordleGame` and `WordlePygame`. The `WordleGame` class handles the logic and mechanics of the Wordle game, while `WordlePygame` provides a Pygame-based GUI for an enhanced gameplay experience.

### `WordleGame`

The `WordleGame` class is responsible for managing the core gameplay of Wordle. It allows the player to guess words, checks the accuracy of these guesses, and keeps track of the game's state. Key features include:

- Word validation against a dictionary API.
- Color-coded feedback for each guess.
- Tracking of guessed words and remaining attempts.

### `WordlePygame`

The `WordlePygame` class is a Pygame-based graphical interface for the Wordle game. It includes:

- Main menu with word size selection.
- Input handling for guesses.
- Graphical display of guesses and game state.

## Requirements

- Python 3
- Pygame library
- Internet access for word validation (API use)

## Installation

1. Clone the repository or download the source code.
2. Install Pygame using `pip install pygame` if not already installed.
3. Run the main script to start the game.

## Usage

### Command-Line Interface

Run `wordle.py` to start the Wordle game in the command line. The game will prompt you to input a word size and then start the guessing game.

### Graphical User Interface

Run `runner.py` to start the Wordle game with a graphical interface. Use the mouse to interact with the on-screen elements.

## Configuration

- The word list can be modified or extended by editing the corresponding `.txt` files.
- The GUI appearance can be customized by changing the color and font constants in `WordlePygame`.

## Acknowledgments

This implementation was inspired by the original Wordle game and aims to provide a simple yet engaging gameplay experience in Python.