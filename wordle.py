import random


class WordList:
    LISTSIZE = 1000

    def __init__(self, wordsize):
        self.wl_filename = f"{wordsize}.txt"
        self.options = []
        self.load_word_list()

    def load_word_list(self):
        try:
            with open(self.wl_filename, "r") as wordlist:
                self.options = [
                    wordlist.readline().strip() for _ in range(self.LISTSIZE)
                ]
        except IOError:
            raise RuntimeError(f"Error opening file {self.wl_filename}.")

    def get_random_word(self):
        return random.choice(self.options)


class WordleGame:
    EXACT = 2
    CLOSE = 1
    WRONG = 0

    def __init__(self, wordsize):
        if wordsize < 5 or wordsize > 8:
            raise ValueError("Error: wordsize must be either 5, 6, 7, or 8")
        self.wordsize = wordsize
        self.wordList = WordList(wordsize)
        self.choice = self.wordList.get_random_word()
        self.guesses = wordsize + 1

    def get_guess(self):
        guess = ""
        while len(guess) != self.wordsize:
            guess = input(f"Input a {self.wordsize}-letter word: ")
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
        won = False

        for i in range(self.guesses):
            guess = self.get_guess()
            score, status = self.check_word(guess)

            print(f"Guess {i + 1}: ", end="")
            self.print_word(guess, status)

            if score == self.EXACT * self.wordsize:
                won = True
                break

        if won:
            print("You won!")
        else:
            print(f"The word was {self.choice}.")


def main():
    wordsize = input("Enter desired word size (5-8) to start: ")
    try:
        wordsize = int(wordsize)
        game = WordleGame(wordsize)
        game.start()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()