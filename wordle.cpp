#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <array>
#include <string>
#include <random>
#include <unordered_map>

class WordList
{
private:
    static constexpr int LISTSIZE = 1000;
    std::array<std::string, LISTSIZE> options;
    std::string wl_filename;

    void loadWordList()
    {
        std::ifstream wordlist(wl_filename);
        if (!wordlist)
        {
            throw std::runtime_error("Error opening file " + wl_filename + ".");
        }
        for (int i = 0; i < LISTSIZE; i++)
        {
            wordlist >> options[i];
        }
    }

public:
    WordList(int wordsize)
    {
        std::ostringstream filename_stream;
        filename_stream << wordsize << ".txt";
        wl_filename = filename_stream.str();
        loadWordList();
    }

    std::string getRandomWord()
    {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> distr(0, LISTSIZE - 1);
        return options[distr(gen)];
    }
};

class WordleGame
{
private:
    static constexpr int EXACT = 2;
    static constexpr int CLOSE = 1;
    static constexpr int WRONG = 0;
    static constexpr char GREEN[] = "\e[38;2;255;255;255;1m\e[48;2;106;170;100;1m";
    static constexpr char YELLOW[] = "\e[38;2;255;255;255;1m\e[48;2;201;180;88;1m";
    static constexpr char RED[] = "\e[38;2;255;255;255;1m\e[48;2;220;20;60;1m";
    static constexpr char RESET[] = "\e[0;39m";

    int wordsize;
    int guesses;
    WordList wordList;
    std::string choice;

    std::string getGuess()
    {
        std::
            string guess;
        do
        {
            std::cout << "Input a " << wordsize << "-letter word: ";
            std::cin >> guess;
        } while (guess.length() != wordsize);
        return guess;
    }

    int checkWord(const std::string &guess, std::vector<int> &status)
    {
        int score = 0;
        std::unordered_map<char, int> letter_counts;
        for (char c : choice)
        {
            letter_counts[c]++;
        }

        for (int i = 0; i < guess.size(); ++i)
        {
            if (guess[i] == choice[i])
            {
                status[i] = EXACT;
                score += EXACT;
                letter_counts[guess[i]]--;
            }
        }

        for (int i = 0; i < guess.size(); ++i)
        {
            if (status[i] != EXACT && letter_counts[guess[i]] > 0)
            {
                status[i] = CLOSE;
                score += CLOSE;
                letter_counts[guess[i]]--;
            }
        }
        return score;
    }

    void printWord(const std::string &guess, const std::vector<int> &status)
    {
        for (int i = 0; i < wordsize; i++)
        {
            if (status[i] == EXACT)
            {
                std::cout << GREEN << guess[i] << RESET;
            }
            else if (status[i] == CLOSE)
            {
                std::cout << YELLOW << guess[i] << RESET;
            }
            else
            {
                std::cout << RED << guess[i] << RESET;
            }
        }
        std::cout << std::endl;
    }

public:
    WordleGame(int wordsize) : wordsize(wordsize), wordList(wordsize)
    {
        if (wordsize < 5 || wordsize > 8)
        {
            throw std::invalid_argument("Error: wordsize must be either 5, 6, 7, or 8");
        }
        choice = wordList.getRandomWord();
        guesses = wordsize + 1;
    }

    void start()
    {
        std::cout << GREEN << "This is WORDLE" << RESET << std::endl;
        std::cout << "You have " << guesses << " tries to guess the " << wordsize << "-letter word I'm thinking of" << std::endl;
        bool won = false;

        for (int i = 0; i < guesses; i++)
        {
            std::string guess = getGuess();
            std::vector<int> status(wordsize, 0);
            int score = checkWord(guess, status);

            std::cout << "Guess " << i + 1 << ": ";
            printWord(guess, status);

            if (score == EXACT * wordsize)
            {
                won = true;
                break;
            }
        }

        if (won)
        {
            std::cout << "You won!" << std::endl;
        }
        else
        {
            std::cout << "The word was " << choice << "." << std::endl;
        }
    }
};

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        std::cout << "Usage: ./wordle wordsize" << std::endl;
        return 1;
    }
    try
    {
        int wordsize = std::stoi(argv[1]);
        WordleGame game(wordsize);
        game.start();
    }
    catch (const std::exception &e)
    {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}