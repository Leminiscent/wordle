import random
import requests


class WordList:
    LISTSIZE = 1000

    def __init__(self, wordsize, cache):
        self.wl_filename = f"{wordsize}.txt"
        self.options = []
        self.cache = cache
        self.load_word_list()

    def load_word_list(self):
        try:
            with open(self.wl_filename, "r") as wordlist:
                for _ in range(self.LISTSIZE):
                    word = wordlist.readline().strip()
                    self.options.append(word)
                    self.cache[word] = True  # Add to cache
        except IOError:
            raise RuntimeError(f"Error opening file {self.wl_filename}.")


class WordleGame:
    EXACT = 2
    CLOSE = 1
    WRONG = 0

    def __init__(self, wordsize, cache):
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
        guess = ""
        while len(guess) != self.wordsize:
            guess = input(f"Input a {self.wordsize}-letter word: ").strip().lower()
        return guess

    def check_word(self, guess):
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
        Check if a word is valid by querying the dictionary API.
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
        for i in range(self.wordsize):
            if status[i] == self.EXACT:
                print(f"\033[1;37;42m{guess[i]}\033[0m", end="")
            elif status[i] == self.CLOSE:
                print(f"\033[1;37;43m{guess[i]}\033[0m", end="")
            else:
                print(f"\033[1;37;41m{guess[i]}\033[0m", end="")
        print()

    def start(self):
        print(f"\033[1;37;42mThis is WORDLE\033[0m")
        print(
            f"You have {self.guesses} tries to guess the {self.wordsize}-letter word I'm thinking of"
        )

        for _ in range(self.guesses):
            guess = self.get_guess()

            if guess in self.guessed_words:
                print("You have already guessed this word. Try a different word.")
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
