import pygame
import sys
from wordle import WordleGame

# Initialize pygame
pygame.init()

# Constants for colors, fonts, and window dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BACKGROUND_COLOR = (242, 242, 242)  # Light Grey background
TEXT_COLOR = (48, 71, 94)  # Dark Blue text
BUTTON_COLOR = (100, 181, 246)  # Light Blue buttons
BUTTON_HOVER_COLOR = (41, 182, 246)  # Brighter Blue for button hover effect
INPUT_OUTLINE_COLOR = (224, 224, 224)  # Light Grey for input box outline
EXACT_GUESS_COLOR = (129, 199, 132)  # Soft Green for exact letter matches
CLOSE_GUESS_COLOR = (255, 235, 59)  # Muted Yellow for close letter matches
WRONG_GUESS_COLOR = (239, 83, 80)  # Soft Red for incorrect letters
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"  # Path to OpenSans font
FONT = pygame.font.Font(OPEN_SANS, 36)  # Default font for text
TITLE_FONT = pygame.font.Font(OPEN_SANS, 48)  # Larger font for the game title


class WordlePygame:
    """
    A class for handling the graphical user interface of the Wordle game using pygame.

    This class is responsible for creating and managing the game window, handling
    user inputs, and rendering the game's graphical elements.

    Attributes:
        screen (pygame.Surface): The main window surface where the game is displayed.
        clock (pygame.Clock): A pygame clock to control the game's frame rate.
        wordle_game (WordleGame): An instance of the WordleGame class.
        current_screen (str): A string indicating the current screen or game state.
        input_box (pygame.Rect): A rectangle defining the input box area.
        guess_log (list): A list to keep track of the guesses and their statuses.
        validation_cache (dict): A cache for storing and retrieving validated words.
    """

    def __init__(self, cache):
        """
        Initializes the WordlePygame with a cache for word validation.

        Sets up the pygame window, fonts, and initializes game-related attributes.

        Args:
            cache (dict): A cache for storing and retrieving validated words.
        """
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Wordle")
        self.clock = pygame.time.Clock()
        self.wordle_game = None
        self.current_screen = "main_menu"
        self.input_box = None
        self.guess_log = []
        self.validation_cache = cache

    def main_menu(self):
        """
        Handles the rendering and interaction of the main menu screen.

        Displays the game title, instructions, and buttons for choosing the word size
        or quitting the game. Handles button click events to start the game or exit.
        """
        self.screen.fill(BACKGROUND_COLOR)
        self.render_title()
        self.render_instructions()
        word_sizes = [5, 6, 7, 8]  # Available word sizes
        buttons = self.render_word_size_buttons(word_sizes)
        quit_button = self.render_quit_button()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_main_menu_click(event.pos, buttons, quit_button)

        pygame.display.update()

    def render_title(self):
        """
        Renders the game title at the top of the screen.
        """
        title = TITLE_FONT.render("Wordle", True, TEXT_COLOR)
        self.screen.blit(title, (WINDOW_WIDTH / 2 - title.get_width() / 2, 30))

    def render_instructions(self):
        """
        Renders instructions for the user on how to start the game.
        """
        instructions = FONT.render("Choose your word size to start", True, TEXT_COLOR)
        self.screen.blit(
            instructions, (WINDOW_WIDTH / 2 - instructions.get_width() / 2, 100)
        )

    def render_word_size_buttons(self, word_sizes):
        """
        Renders buttons for each available word size.

        Args:
            word_sizes (list): A list of integers representing the available word sizes.

        Returns:
            dict: A dictionary mapping button rectangles to their corresponding word sizes.
        """
        button_width, button_height = 100, 50
        grid_start_x, grid_start_y = WINDOW_WIDTH / 2 - button_width - 10, 200
        buttons = {}

        for i, size in enumerate(word_sizes):
            button_x = grid_start_x + (i % 2) * (button_width + 10)
            button_y = grid_start_y + (i // 2) * (button_height + 10)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            # Use a tuple of the rect's properties as the key for the button
            button_key = (button_x, button_y, button_width, button_height)
            buttons[button_key] = size

            # Change color on hover
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, button_rect)
            else:
                pygame.draw.rect(self.screen, BUTTON_COLOR, button_rect)
            pygame.draw.rect(self.screen, INPUT_OUTLINE_COLOR, button_rect, 2)

            # Draw button text
            button_text = FONT.render(str(size), True, TEXT_COLOR)
            self.screen.blit(
                button_text,
                (
                    button_x + button_width / 2 - button_text.get_width() / 2,
                    button_y + button_height / 2 - button_text.get_height() / 2,
                ),
            )

        return buttons

    def render_quit_button(self):
        """
        Renders a 'Quit' button on the main menu screen.

        Returns:
            pygame.Rect: A rectangle representing the position and size of the quit button.
        """
        button_width, button_height = 100, 50
        grid_start_x, grid_start_y = WINDOW_WIDTH / 2 - button_width - 10, 200
        quit_button = pygame.Rect(
            grid_start_x,
            grid_start_y + 2 * (button_height + 10),
            2 * button_width + 10,
            button_height,
        )

        # Change color on hover
        if quit_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, quit_button)
        else:
            pygame.draw.rect(self.screen, BUTTON_COLOR, quit_button)
        pygame.draw.rect(self.screen, INPUT_OUTLINE_COLOR, quit_button, 2)

        quit_text = FONT.render("Quit", True, TEXT_COLOR)
        self.screen.blit(
            quit_text,
            (
                quit_button.x + quit_button.width / 2 - quit_text.get_width() / 2,
                quit_button.y + button_height / 2 - quit_text.get_height() / 2,
            ),
        )

        return quit_button

    def handle_main_menu_click(self, mouse_pos, buttons, quit_button):
        """
        Handles click events on the main menu screen.

        Args:
            mouse_pos (tuple): The position of the mouse click.
            buttons (dict): A dictionary mapping button rectangles to word sizes.
            quit_button (pygame.Rect): The rectangle representing the quit button.
        """
        for button_key, size in buttons.items():
            button_rect = pygame.Rect(button_key)
            if button_rect.collidepoint(mouse_pos):
                self.wordle_game = WordleGame(size, self.validation_cache)
                self.wordle_game.guessed_words = set()
                self.guess_log = []
                self.current_screen = "game_screen"
                return

        if quit_button.collidepoint(mouse_pos):
            pygame.quit()
            sys.exit()

    def game_screen(self):
        """
        Manages the game screen where the actual Wordle game takes place.

        Initializes UI elements and enters the main game loop.
        """
        self.initialize_ui_elements()
        self.game_loop()

    def initialize_ui_elements(self):
        """
        Initializes input box and buttons for the game screen.
        """
        self.screen.fill(BACKGROUND_COLOR)
        # Input box setup
        self.input_box = pygame.Rect(WINDOW_WIDTH / 2 - 100, 50, 200, 40)
        self.text = ""
        self.active = True  # Active state of input box

        # Define button dimensions and positions
        button_width, button_height = 150, 50
        buttons_start_x, buttons_start_y = 50, 100

        # Reset Button
        self.reset_button = pygame.Rect(
            buttons_start_x, buttons_start_y, button_width, button_height
        )

        # Main Menu Button
        self.main_menu_button = pygame.Rect(
            buttons_start_x,
            buttons_start_y + button_height + 10,
            button_width,
            button_height,
        )

    def game_loop(self):
        """
        The main game loop, handling events and updating the game screen.

        Continuously processes user input events and updates the display.
        Exits the loop if the game screen changes.
        """
        while True:
            self.handle_events()
            if self.current_screen != "game_screen":
                break  # Exit the loop if the screen should change
            self.update_game_display()
            self.clock.tick(30)  # Limit to 30 frames per second for consistent timing

    def handle_events(self):
        """
        Handles user input events like mouse clicks and keyboard inputs.

        Processes events related to quitting the game, clicking the mouse, and pressing keys.
        Manages the input for the game, including submitting guesses and navigating between screens.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_press(event)

    def handle_mouse_click(self, event):
        """
        Handles mouse click events on the game screen.

        Args:
            event (pygame.Event): The event object containing information about the mouse click.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.input_box.collidepoint(event.pos):
            self.active = True
        elif self.reset_button.collidepoint(mouse_pos):
            # Reset game logic
            self.reset_game()
            self.active = True  # Activate the input box
            return
        elif self.main_menu_button.collidepoint(mouse_pos):
            self.current_screen = "main_menu"
            return
        else:
            self.active = False

    def handle_key_press(self, event):
        """
        Handles key press events during the game.

        Args:
            event (pygame.Event): The event object containing information about the key press.
        """
        if self.active:
            if event.key == pygame.K_RETURN:
                self.process_guess()
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Remove the last character
            else:
                # Add character to input if it doesn't exceed word length
                if len(self.text) < self.wordle_game.wordsize:
                    self.text += event.unicode

    def process_guess(self):
        """
        Processes the player's guess and updates the game state.

        Validates the guess, updates the guess log, and checks the game's win/lose condition.
        Displays messages for invalid inputs, repeated guesses, or game outcomes.
        """
        guess = self.text.lower()
        if len(guess) == self.wordle_game.wordsize:
            if not guess.isalpha():
                self.display_message("Invalid input! Use only letters.", 750)
                self.text = ""
                return

            if guess in self.wordle_game.guessed_words:
                self.display_message(f"You have already guessed '{guess}'.", 750)
                self.text = ""
                return
            self.wordle_game.guessed_words.add(guess)

            if not self.wordle_game.is_valid_word(guess):
                if self.wordle_game.api_available:
                    self.display_message("Not a valid word. Try again.", 750)
                else:
                    self.display_message(
                        [
                            "API currently unavailable,",
                            "continuing without word validation.",
                        ],
                        1500,
                    )

                self.text = ""
                return

            score, status = self.wordle_game.check_word(guess)
            self.guess_log.append((guess, status))
            self.text = ""  # Reset text
            self.wordle_game.guesses -= 1

            if score == self.wordle_game.EXACT * self.wordle_game.wordsize:
                self.display_message("You won!", 2000)
                self.current_screen = "main_menu"
                return
            elif self.wordle_game.guesses == 0:
                self.display_message(
                    f"The word was {self.wordle_game.choice}. You lost!", 2000
                )
                self.current_screen = "main_menu"
                return

    def update_game_display(self):
        """
        Updates and redraws the game display.

        Draws the input box, buttons, and the guess log on the screen.
        Also updates the display with the remaining number of guesses.
        """
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_buttons()
        self.draw_input_box()
        # Display guess log and guess counter
        self.display_guess_log()
        self.display_guess_counter()
        pygame.display.flip()

    def draw_buttons(self):
        """
        Draws buttons on the game screen, including the reset and main menu buttons.

        Changes button colors on hover and displays button text.
        """
        mouse_pos = pygame.mouse.get_pos()

        # Loop through each button and draw
        for button, text in [
            (self.reset_button, "Reset"),
            (self.main_menu_button, "Menu"),
        ]:
            if button.collidepoint(mouse_pos):
                # Change color on hover
                pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, button)
            else:
                pygame.draw.rect(self.screen, BUTTON_COLOR, button)

            # Draw button outline
            pygame.draw.rect(self.screen, INPUT_OUTLINE_COLOR, button, 2)

            # Draw button text
            text_surface = FONT.render(text, True, TEXT_COLOR)
            text_x = button.x + (button.width - text_surface.get_width()) / 2
            text_y = button.y + (button.height - text_surface.get_height()) / 2
            self.screen.blit(text_surface, (text_x, text_y))

    def draw_input_box(self):
        """
        Draws the input box where the user types their guesses.

        Highlights the box when active and displays the current text input.
        """
        txt_surface = FONT.render(self.text, True, TEXT_COLOR)
        # Align text in the center of the input box
        text_x = self.input_box.x + (self.input_box.width - txt_surface.get_width()) / 2
        text_y = (
            self.input_box.y + (self.input_box.height - txt_surface.get_height()) / 2
        )
        self.screen.blit(txt_surface, (text_x, text_y))
        box_color = BUTTON_HOVER_COLOR if self.active else INPUT_OUTLINE_COLOR
        pygame.draw.rect(self.screen, box_color, self.input_box, 2)

    def reset_game(self):
        """
        Resets the game to its initial state.

        Creates a new instance of WordleGame with the same word size and clears the guess log.
        """
        # Reset the game logic
        self.wordle_game = WordleGame(self.wordle_game.wordsize, self.validation_cache)
        self.wordle_game.guessed_words = set()
        self.guess_log = []
        self.current_screen = "game_screen"

    def quit_game(self):
        """
        Quits the game and exits.

        Closes the pygame window and terminates the program.
        """
        pygame.quit()
        sys.exit()

    def display_guess_log(self):
        """
        Renders the log of all guesses made by the player.

        For each guess, displays each letter in a colored box. The color indicates whether
        the letter is correct (green), in the wrong position (yellow), or not in the word (red).
        Adjusts the size of the boxes based on the word length.
        """
        # Dynamic adjustment based on word size
        if self.wordle_game.wordsize <= 5:
            letter_box_size = 40
            spacing = 5
        elif self.wordle_game.wordsize == 6:
            letter_box_size = 35
            spacing = 4
        elif self.wordle_game.wordsize == 7:
            letter_box_size = 30
            spacing = 3
        else:
            letter_box_size = 25
            spacing = 2

        # Calculate the starting position dynamically
        total_width = (
            self.wordle_game.wordsize * letter_box_size
            + (self.wordle_game.wordsize - 1) * spacing
        )
        log_start_x = WINDOW_WIDTH - total_width - 50  # Adjust for right alignment
        log_start_y = 50  # Starting position of the guess log

        for guess_index, (guess, status) in enumerate(self.guess_log):
            for letter_index, letter in enumerate(guess):
                # Determine the color based on the status
                if status[letter_index] == self.wordle_game.EXACT:
                    color = EXACT_GUESS_COLOR
                elif status[letter_index] == self.wordle_game.CLOSE:
                    color = CLOSE_GUESS_COLOR
                else:
                    color = WRONG_GUESS_COLOR

                # Position of each letter box
                x = log_start_x + letter_index * (letter_box_size + spacing)
                y = log_start_y + guess_index * (letter_box_size + spacing)

                # Draw letter box
                letter_rect = pygame.Rect(x, y, letter_box_size, letter_box_size)
                pygame.draw.rect(self.screen, color, letter_rect)

                # Draw letter
                dynamic_font = pygame.font.Font(OPEN_SANS, int(letter_box_size * 0.95))
                letter_surface = dynamic_font.render(letter.upper(), True, TEXT_COLOR)
                letter_x = x + (letter_box_size - letter_surface.get_width()) / 2
                letter_y = y + (letter_box_size - letter_surface.get_height()) / 2
                self.screen.blit(letter_surface, (letter_x, letter_y))

    def display_guess_counter(self):
        """
        Displays the remaining number of guesses on the game screen.

        Shows the number of guesses left for the player at the top of the screen.
        Helps the player keep track of how many attempts they have remaining.
        """
        counter_text = f"Guesses left: {self.wordle_game.guesses}"
        text_surface = FONT.render(counter_text, True, TEXT_COLOR)
        self.screen.blit(text_surface, (10, 10))

    def display_message(self, message, wait_time=None, quit_after=False):
        """
        Displays a message at the center of the screen, optionally waiting for a specified time.

        Can be used to display end-of-game messages, warnings, or other information.
        The method allows for multi-line messages and can control whether the game quits after displaying the message.

        Args:
            message (str or list of str): The message or list of messages to be displayed.
            wait_time (int, optional): Time in milliseconds to wait before continuing or quitting.
            quit_after (bool, optional): If True, quits the game after displaying the message.
        """
        # If the message is a string, make it a single-element list
        if isinstance(message, str):
            message = [message]

        # Calculate the starting Y position for the message
        start_y = 350
        for line in message:
            msg_surface = FONT.render(line, True, TEXT_COLOR)
            # Center the message horizontally on the screen
            self.screen.blit(
                msg_surface,
                (WINDOW_WIDTH / 2 - msg_surface.get_width() / 2, start_y),
            )
            # Move to the next line position
            start_y += FONT.size(line)[1] + 10

        pygame.display.update()

        # Wait for the specified time while processing events, if wait_time is provided
        if wait_time:
            start_time = pygame.time.get_ticks()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                current_time = pygame.time.get_ticks()
                if current_time - start_time >= wait_time:
                    break

        # If quit_after is True, exit the game after displaying the message
        if quit_after:
            pygame.quit()
            sys.exit()

        # If no wait_time is provided, transition to main menu after displaying the message
        if wait_time is None:
            self.current_screen = "main_menu"
            self.run()

    def run(self):
        """
        The main loop of the WordlePygame.

        Continuously updates the screen and handles transitions between different screens
        (main menu, game screen) based on the game state. Ensures the game runs at a consistent frame rate.
        """
        while True:
            if self.current_screen == "main_menu":
                self.main_menu()
            elif self.current_screen == "game_screen":
                self.game_screen()

            # Update the display and tick the clock
            pygame.display.flip()
            self.clock.tick(30)  # Limit to 30 frames per second


def main():
    """
    The entry point of the Wordle game application.

    Initializes a validation cache and creates an instance of WordlePygame to start the game.
    """
    validation_cache = {}  # Initialize the cache
    game = WordlePygame(validation_cache)
    game.run()


if __name__ == "__main__":
    main()
