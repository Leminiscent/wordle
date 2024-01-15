import pygame
import sys
from wordle import WordleGame

pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BACKGROUND_COLOR = (242, 242, 242)  # Light Grey
TEXT_COLOR = (48, 71, 94)  # Dark Blue
BUTTON_COLOR = (100, 181, 246)  # Light Blue
BUTTON_HOVER_COLOR = (41, 182, 246)  # Brighter Blue
INPUT_OUTLINE_COLOR = (224, 224, 224)  # Light Grey
CORRECT_GUESS_COLOR = (129, 199, 132)  # Soft Green
CLOSE_GUESS_COLOR = (255, 235, 59)  # Muted Yellow
INCORRECT_GUESS_COLOR = (239, 83, 80)  # Soft Red
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
FONT = pygame.font.Font(OPEN_SANS, 36)
TITLE_FONT = pygame.font.Font(OPEN_SANS, 48)


class WordlePygame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Wordle")
        self.clock = pygame.time.Clock()
        self.wordle_game = None
        self.current_screen = "main_menu"
        self.input_box = None
        self.guess_log = []

    def main_menu(self):
        self.screen.fill(BACKGROUND_COLOR)
        mouse_pos = pygame.mouse.get_pos()  # Get current mouse position
        title = TITLE_FONT.render("Wordle", True, TEXT_COLOR)
        instructions = FONT.render("Choose your word size to start", True, TEXT_COLOR)
        self.screen.blit(title, (WINDOW_WIDTH / 2 - title.get_width() / 2, 30))
        self.screen.blit(
            instructions, (WINDOW_WIDTH / 2 - instructions.get_width() / 2, 100)
        )

        # Button dimensions and positions
        button_width, button_height = 100, 50
        grid_start_x, grid_start_y = WINDOW_WIDTH / 2 - button_width - 10, 200

        # Drawing buttons for word sizes and quit
        word_sizes = [5, 6, 7, 8]
        buttons = {}
        for i, size in enumerate(word_sizes):
            button_x = grid_start_x + (i % 2) * (button_width + 10)
            button_y = grid_start_y + (i // 2) * (button_height + 10)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            buttons[(button_x, button_y, button_width, button_height)] = size

            # Change button color when hovered
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, button_rect)
            else:
                pygame.draw.rect(self.screen, BUTTON_COLOR, button_rect)
            pygame.draw.rect(self.screen, INPUT_OUTLINE_COLOR, button_rect, 2)
            button_text = FONT.render(str(size), True, TEXT_COLOR)
            self.screen.blit(
                button_text,
                (
                    button_x + button_width / 2 - button_text.get_width() / 2,
                    button_y + button_height / 2 - button_text.get_height() / 2,
                ),
            )

        # Quit button positioned under the 2x2 grid
        quit_button_x, quit_button_y = grid_start_x, grid_start_y + 2 * (
            button_height + 10
        )
        quit_button = pygame.Rect(
            quit_button_x,
            quit_button_y,
            2 * button_width + 10,  # Width to span the entire grid width
            button_height,
        )
        if quit_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, quit_button)
        else:
            pygame.draw.rect(self.screen, BUTTON_COLOR, quit_button)
        pygame.draw.rect(self.screen, INPUT_OUTLINE_COLOR, quit_button, 2)
        quit_text = FONT.render("Quit", True, TEXT_COLOR)
        self.screen.blit(
            quit_text,
            (
                quit_button_x + quit_button.width / 2 - quit_text.get_width() / 2,
                quit_button_y + button_height / 2 - quit_text.get_height() / 2,
            ),
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button_key, size in buttons.items():
                    # Create a Rect object from the tuple to use collidepoint
                    button_rect = pygame.Rect(*button_key)
                    if button_rect.collidepoint(mouse_pos):
                        self.wordle_game = WordleGame(size)
                        self.guess_log = []
                        self.current_screen = "game_screen"
                        return
                if quit_button.collidepoint(mouse_pos):
                    self.screen.fill(BACKGROUND_COLOR)
                    self.display_message("Goodbye!", 2000)  # Display goodbye message

        pygame.display.update()

    def game_screen(self):
        self.screen.fill(BACKGROUND_COLOR)
        # Input box setup
        input_box = pygame.Rect(WINDOW_WIDTH / 2 - 100, 50, 200, 40)
        text = ""
        active = True  # Active state of input box

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            # Process guess
                            guess = text.lower()
                            if len(guess) == self.wordle_game.wordsize:
                                if not guess.isalpha():
                                    self.display_message(
                                        "Invalid input! Use only letters.", 500
                                    )
                                    text = ""
                                    continue

                                # Check if guess is in word list
                                if guess not in self.wordle_game.wordList.options:
                                    self.display_message("Word not in list!", 500)
                                    text = ""
                                    continue

                                score, status = self.wordle_game.check_word(guess)
                                self.guess_log.append((guess, status))
                                text = ""  # Reset text
                                self.wordle_game.guesses -= 1
                                if (
                                    score
                                    == self.wordle_game.EXACT
                                    * self.wordle_game.wordsize
                                ):
                                    self.display_message("You won!")
                                    return
                                elif self.wordle_game.guesses == 0:
                                    self.display_message(
                                        f"The word was {self.wordle_game.choice}. You lost!"
                                    )
                                    return
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            if len(text) < self.wordle_game.wordsize:
                                text += event.unicode

            # Input box
            self.screen.fill(BACKGROUND_COLOR)
            txt_surface = FONT.render(text, True, TEXT_COLOR)
            # Align text in the center of the input box
            text_x = input_box.x + (input_box.width - txt_surface.get_width()) / 2
            text_y = input_box.y + (input_box.height - txt_surface.get_height()) / 2
            self.screen.blit(txt_surface, (text_x, text_y))
            box_color = (
                BUTTON_HOVER_COLOR if active else INPUT_OUTLINE_COLOR
            )  # Change color when active
            pygame.draw.rect(self.screen, box_color, input_box, 2)

            # Display guess log and guess counter
            self.display_guess_log()
            self.display_guess_counter()

            pygame.display.flip()
            self.clock.tick(30)

    def dynamic_font_size(self, letter_box_size):
        """Calculate font size dynamically based on the letter box size."""
        return int(letter_box_size * 0.95)

    def display_guess_log(self):
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
                    color = CORRECT_GUESS_COLOR
                elif status[letter_index] == self.wordle_game.CLOSE:
                    color = CLOSE_GUESS_COLOR
                else:
                    color = INCORRECT_GUESS_COLOR

                # Position of each letter box
                x = log_start_x + letter_index * (letter_box_size + spacing)
                y = log_start_y + guess_index * (letter_box_size + spacing)

                # Draw letter box
                letter_rect = pygame.Rect(x, y, letter_box_size, letter_box_size)
                pygame.draw.rect(self.screen, color, letter_rect)

                # Draw letter
                dynamic_font = pygame.font.Font(
                    OPEN_SANS, self.dynamic_font_size(letter_box_size)
                )
                letter_surface = dynamic_font.render(letter.upper(), True, TEXT_COLOR)
                letter_x = x + (letter_box_size - letter_surface.get_width()) / 2
                letter_y = y + (letter_box_size - letter_surface.get_height()) / 2
                self.screen.blit(letter_surface, (letter_x, letter_y))

    def display_guess_counter(self):
        """Display the remaining number of guesses."""
        counter_text = f"Guesses left: {self.wordle_game.guesses}"
        text_surface = FONT.render(counter_text, True, TEXT_COLOR)
        self.screen.blit(text_surface, (10, 10))

    def display_message(self, message, wait_time=None):
        """Display a message at the center of the screen.

        Args:
        message (str): The message to display.
        wait_time (int, optional): Time in milliseconds to wait. If None, returns to main menu after displaying the message.
        """
        msg_surface = FONT.render(message, True, TEXT_COLOR)
        self.screen.blit(
            msg_surface,
            (
                WINDOW_WIDTH / 2 - msg_surface.get_width() / 2,
                WINDOW_HEIGHT / 2 - msg_surface.get_height() / 2,
            ),
        )
        pygame.display.update()
        if wait_time is not None:
            pygame.time.wait(wait_time)  # Wait for the specified time
            if wait_time == 2000:  # Specific case for quitting after "Goodbye!"
                pygame.quit()
                sys.exit()
        else:
            pygame.time.wait(2000)
            self.current_screen = "main_menu"
            self.run()

    def run(self):
        while True:
            if self.current_screen == "main_menu":
                self.main_menu()
            elif self.current_screen == "game_screen":
                self.game_screen()

            # Update the display and tick the clock
            pygame.display.flip()
            self.clock.tick(30)  # 30 frames per second


def main():
    game = WordlePygame()
    game.run()


if __name__ == "__main__":
    main()
