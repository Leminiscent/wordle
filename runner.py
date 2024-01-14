import pygame
import sys
from wordle import WordleGame

pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
FONT = pygame.font.Font(OPEN_SANS, 36)


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
        self.screen.fill(WHITE)
        title = FONT.render("Wordle", True, BLACK)
        instructions = FONT.render("Choose your word size to start", True, BLACK)
        self.screen.blit(title, (WINDOW_WIDTH / 2 - title.get_width() / 2, 50))
        self.screen.blit(
            instructions, (WINDOW_WIDTH / 2 - instructions.get_width() / 2, 100)
        )

        # Button dimensions and positions
        button_width, button_height = 100, 50
        start_x, start_y = WINDOW_WIDTH / 2 - button_width / 2, 200
        button_gap = 60

        # Drawing buttons for word sizes and quit
        word_sizes = [5, 6, 7, 8]
        buttons = {}
        for i, size in enumerate(word_sizes):
            button_rect = pygame.Rect(
                start_x,
                start_y + i * (button_height + button_gap),
                button_width,
                button_height,
            )
            buttons[
                (
                    start_x,
                    start_y + i * (button_height + button_gap),
                    button_width,
                    button_height,
                )
            ] = size
            pygame.draw.rect(self.screen, BLACK, button_rect, 2)
            button_text = FONT.render(str(size), True, BLACK)
            self.screen.blit(
                button_text,
                (
                    start_x + button_width / 2 - button_text.get_width() / 2,
                    start_y
                    + i * (button_height + button_gap)
                    + button_height / 2
                    - button_text.get_height() / 2,
                ),
            )

        # Quit button
        quit_button = pygame.Rect(
            start_x,
            start_y + 4 * (button_height + button_gap),
            button_width,
            button_height,
        )
        pygame.draw.rect(self.screen, BLACK, quit_button, 2)
        quit_text = FONT.render("Quit", True, BLACK)
        self.screen.blit(
            quit_text,
            (
                start_x + button_width / 2 - quit_text.get_width() / 2,
                start_y
                + 4 * (button_height + button_gap)
                + button_height / 2
                - quit_text.get_height() / 2,
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
                        self.current_screen = "game_screen"
                        return
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

    def game_screen(self):
        self.screen.fill(WHITE)
        # Input box setup
        input_box = pygame.Rect(WINDOW_WIDTH / 2 - 100, 50, 200, 40)
        text = ""
        active = False  # Active state of input box

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
                                score, status = self.wordle_game.check_word(guess)
                                self.guess_log.append((guess, status))
                                text = ""  # Reset text
                                self.wordle_game.guesses -= 1
                                if (
                                    score
                                    == self.wordle_game.EXACT
                                    * self.wordle_game.wordsize
                                ):
                                    self.display_result("You won!")
                                    return
                                elif self.wordle_game.guesses == 0:
                                    self.display_result(
                                        f"The word was {self.wordle_game.choice}. You lost!"
                                    )
                                    return
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            if len(text) < self.wordle_game.wordsize:
                                text += event.unicode

            # Input box
            self.screen.fill(WHITE)
            txt_surface = FONT.render(text, True, BLACK)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, BLACK, input_box, 2)

            # Display guess log
            self.display_guess_log()

            pygame.display.flip()
            self.clock.tick(30)

    def display_guess_log(self):
        log_start_x, log_start_y = 50, 100  # Starting position of the guess log
        letter_box_size = 40  # Size of each letter box
        spacing = 5  # Spacing between boxes

        for guess_index, (guess, status) in enumerate(self.guess_log):
            for letter_index, letter in enumerate(guess):
                # Determine the color based on the status
                if status[letter_index] == self.wordle_game.EXACT:
                    color = GREEN
                elif status[letter_index] == self.wordle_game.CLOSE:
                    color = YELLOW
                else:
                    color = RED

                # Position of each letter box
                x = log_start_x + letter_index * (letter_box_size + spacing)
                y = log_start_y + guess_index * (letter_box_size + spacing)

                # Draw letter box
                letter_rect = pygame.Rect(x, y, letter_box_size, letter_box_size)
                pygame.draw.rect(self.screen, color, letter_rect)

                # Draw letter
                letter_surface = FONT.render(letter.upper(), True, BLACK)
                letter_x = x + (letter_box_size - letter_surface.get_width()) / 2
                letter_y = y + (letter_box_size - letter_surface.get_height()) / 2
                self.screen.blit(letter_surface, (letter_x, letter_y))

    def display_result(self, message):
        # Display the result message
        result_msg = FONT.render(message, True, BLACK)
        self.screen.blit(
            result_msg,
            (
                WINDOW_WIDTH / 2 - result_msg.get_width() / 2,
                WINDOW_HEIGHT / 2 - result_msg.get_height() / 2,
            ),
        )
        pygame.display.update()

        # Wait for a few seconds and return to the main menu
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
