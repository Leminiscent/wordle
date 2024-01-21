import random
import requests


class WordList:
    """
    A class used to represent a list of words.

    This class handles the loading of a word list from a file and provides
    functionality to get a random word from this list.

    Attributes:
        LISTSIZE (int): The number of words to be loaded from the file.
        wl_filename (str): The name of the file containing the word list.
        options (list): A list of words loaded from the file.
        cache (dict): A cache to store words for quick lookup.

    Methods:
        load_word_list(): Loads words from the file into the list and cache.
        get_random_word(): Returns a random word from the list.
    """

    LISTSIZE = 1000

    def __init__(self, wordsize, cache):
        """
        Initializes the WordList with a specific word size and cache.

        Args:
            wordsize (int): The size of the words to be loaded (e.g., 5 for five-letter words).
            cache (dict): A cache to store and quickly retrieve words.
        """
        self.wl_filename = f"{wordsize}.txt"
        self.options = []
        self.cache = cache
        self.load_word_list()

    def load_word_list(self):
        """
        Loads words from the file into the options list and the cache.

        Reads a fixed number of words from the file specified by wl_filename,
        adding each word to the options list and the cache for quick access.

        Raises:
            RuntimeError: If there is an IOError while opening the file.
        """
        try:
            with open(self.wl_filename, "r") as wordlist:
                for _ in range(self.LISTSIZE):
                    word = wordlist.readline().strip()
                    self.options.append(word)
                    self.cache[word] = True  # Add to cache
        except IOError:
            raise RuntimeError(f"Error opening file {self.wl_filename}.")


class WordleGame:
    """
    A class used to represent the Wordle game logic.

    This class manages the core game mechanics, including guessing words,
    validating guesses, and keeping track of game state.

    Attributes:
        EXACT (int): Constant value representing an exact letter match.
        CLOSE (int): Constant value representing a close letter match.
        WRONG (int): Constant value representing an incorrect letter.
        wordsize (int): The size of the target word.
        guessed_words (set): A set of words that have been guessed.
        validation_cache (dict): A cache for validated words.
        wordList (WordList): An instance of the WordList class.
        choice (str): The target word for the current game.
        guesses (int): The number of guesses allowed.
        api_available (bool): Flag to indicate if the dictionary API is available.

    Methods:
        get_guess(): Prompts the user to input a guess.
        check_word(guess): Checks the guess against the target word.
        is_valid_word(word): Validates if a word is in the dictionary.
        print_word(guess, status): Prints the guess with color-coded feedback.
        start(): Starts the main game loop.
    """

    EXACT = 2
    CLOSE = 1
    WRONG = 0

    def __init__(self, wordsize, cache):
        """
        Initializes the WordleGame with a specific word size and cache.

        Args:
            wordsize (int): The size of the target word.
            cache (dict): A cache for storing and retrieving validated words.

        Raises:
            ValueError: If the wordsize is not between 5 and 8 inclusive.
        """
        if wordsize < 5 or wordsize > 8:
            raise ValueError("Error: wordsize must be either 5, 6, 7, or 8")
        self.wordsize = wordsize
        self.guessed_words = set()
        self.validation_cache = cache
        self.wordList = WordList(wordsize, self.validation_cache)
        self.choice = random.choice(self.wordList.options)
        self.guesses = wordsize + 1
        self.api_available = True

    def get_guess(self):
        """
        Prompts the user to input a guess of the correct word size.

        Continuously prompts until a word of the correct length is input.

        Returns:
            str: The user's guessed word.
        """
        guess = ""
        while len(guess) != self.wordsize:
            guess = input(f"Input a {self.wordsize}-letter word: ").strip().upper()
        return guess

    def check_word(self, guess):
        """
        Compares the guess to the target word and generates a score and status list.

        The method compares each letter of the guess to the target word and assigns
        a status (EXACT, CLOSE, WRONG) to each letter. It also calculates a total score.

        Args:
            guess (str): The guessed word.

        Returns:
            tuple: A tuple containing the total score and a list of status for each letter.
        """
        status = [self.WRONG] * self.wordsize
        score = 0
        letter_counts = {c: self.choice.count(c) for c in set(self.choice)}

        for i, char in enumerate(guess):
            if char == self.choice[i]:
                status[i] = self.EXACT
                score += self.EXACT
                letter_counts[char] -= 1

        for i, char in enumerate(guess):
            if status[i] != self.EXACT and letter_counts.get(char, 0) > 0:
                status[i] = self.CLOSE
                score += self.CLOSE
                letter_counts[char] -= 1

        return score, status

    def is_valid_word(self, word):
        """
        Checks if a word is valid by querying a dictionary API or using a cache.

        First checks the cache for the word. If not found, it queries the dictionary API.
        Handles situations where the API is unavailable.

        Args:
            word (str): The word to validate.

        Returns:
            bool: True if the word is valid, False otherwise.
        """
        # First, check the cache
        if word in self.validation_cache:
            return self.validation_cache[word]

        if not self.api_available:
            # Skip API validation if it's marked as unavailable
            return True

        try:
            response = requests.get(
                f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", timeout=5
            )
            valid = response.status_code == 200
            self.validation_cache[word] = valid  # Cache the result
            return valid
        except (requests.Timeout, requests.RequestException) as e:
            # Handle timeout and other request-related exceptions
            print(f"Warning: Unable to validate words using the dictionary API ({e}).")
            print(
                "Continuing without word validation. Please restart the program to try reconnecting."
            )
            self.api_available = (
                False  # Disable API validation for the rest of the session
            )
            return False

    def print_word(self, guess, status):
        """
        Prints the guessed word with color-coded feedback for each letter.

        Each letter is printed with a background color indicating its correctness:
        green for exact matches, yellow for close matches, and red for wrong letters.

        Args:
            guess (str): The guessed word.
            status (list): A list of status codes for each letter in the guess.
        """
        for i in range(self.wordsize):
            if status[i] == self.EXACT:
                print(f"\033[1;37;42m{guess[i]}\033[0m", end="")
            elif status[i] == self.CLOSE:
                print(f"\033[1;37;43m{guess[i]}\033[0m", end="")
            else:
                print(f"\033[1;37;41m{guess[i]}\033[0m", end="")
        print()

    def start(self):
        """
        Starts the main game loop.

        This method handles the gameplay, including receiving guesses, validating them,
        and providing feedback. It also tracks the number of guesses and determines
        the game's end condition.
        """
        print(f"\033[1;37;42mThis is WORDLE\033[0m")
        print(
            f"You have {self.guesses} tries to guess the {self.wordsize}-letter word I'm thinking of"
        )

        for _ in range(self.guesses):
            guess = self.get_guess()

            if guess in self.guessed_words:
                print(f"You have already guessed {guess}. Try a different word.")
                continue
            self.guessed_words.add(guess)  # Add guess to the set of guessed words

            if not self.is_valid_word(guess):
                print("Not a valid word. Try again.")
                continue

            # Check the guess and update the game state
            score, status = self.check_word(guess)
            print(f"Guess {_ + 1}: ", end="")
            self.print_word(guess, status)

            if score == self.EXACT * self.wordsize:
                print("You won!")
                return

        print(f"The word was {self.choice}.")


def main():
    wordsize = input("Enter desired word size (5-8) to start: ")
    try:
        wordsize = int(wordsize)
        validation_cache = {}  # Initialize the cache
        game = WordleGame(wordsize, validation_cache)
        game.start()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
