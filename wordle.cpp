#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstdlib>
#include <ctime>
#include <unordered_map>

// each text file contains 1000 words
constexpr int LISTSIZE = 1000;

// values for colors and score (EXACT == right letter, right place; CLOSE == right letter, wrong place; WRONG == wrong letter)
constexpr int EXACT = 2;
constexpr int CLOSE = 1;
constexpr int WRONG = 0;

// ANSI color codes for boxed in letters
constexpr char GREEN[] = "\e[38;2;255;255;255;1m\e[48;2;106;170;100;1m";
constexpr char YELLOW[] = "\e[38;2;255;255;255;1m\e[48;2;201;180;88;1m";
constexpr char RED[] = "\e[38;2;255;255;255;1m\e[48;2;220;20;60;1m";
constexpr char RESET[] = "\e[0;39m";

std::string get_guess(int wordsize);                                             // get user's guess
int check_word(std::string guess, std::vector<int> &status, std::string choice); // check guess against the word, update status array
void print_word(std::string guess, int wordsize, std::vector<int> status);       // print the guess with the correct letters boxed in

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        std::cout << "Usage: ./wordle wordsize" << std::endl;
        return 1;
    }

    // open correct file, each file has exactly LISTSIZE words
    int wordsize = std::stoi(argv[1]);
    if (wordsize < 5 || wordsize > 8)
    {
        std::cout << "Error: wordsize must be either 5, 6, 7, or 8" << std::endl;
        return 1;
    }

    std::string wl_filename = std::to_string(wordsize) + ".txt";
    std::ifstream wordlist(wl_filename);
    if (!wordlist)
    {
        std::cout << "Error opening file " << wl_filename << "." << std::endl;
        return 1;
    }

    // load word file into a vector of size LISTSIZE
    std::vector<std::string> options(LISTSIZE);

    for (int i = 0; i < LISTSIZE; i++)
    {
        wordlist >> options[i];
    }

    // pseudorandomly select a word for the current game
    srand(time(nullptr));
    std::string choice = options[rand() % LISTSIZE];

    // allow one more guess than the length of the word
    int guesses = wordsize + 1;
    bool won = false;

    std::cout << GREEN << "This is WORDLE" << RESET << std::endl;
    std::cout << "You have " << guesses << " tries to guess the " << wordsize << "-letter word I'm thinking of" << std::endl;

    // main game loop, one iteration for each guess
    for (int i = 0; i < guesses; i++)
    {
        // obtain user's guess
        std::string guess = get_guess(wordsize);

        // array to hold guess status, initially set to zero
        std::vector<int> status(wordsize, 0);

        // Calculate score for the guess
        int score = check_word(guess, status, choice);

        std::cout << "Guess " << i + 1 << ": ";

        // print the guess
        print_word(guess, wordsize, status);

        // if the user guessed the word, break out of the loop
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

    return 0;
}

std::string get_guess(int wordsize)
{
    std::string guess;

    // loop until the user enters a word of the correct length
    do
    {
        std::cout << "Input a " << wordsize << "-letter word: ";
        std::cin >> guess;
    } while (guess.length() != wordsize);

    return guess;
}

int check_word(const std::string guess, std::vector<int> &status, const std::string choice)
{
    int score = 0;
    std::unordered_map<char, int> letter_counts;

    // Count the letters in the choice
    for (char c : choice)
    {
        letter_counts[c]++;
    }

    // First pass for exact matches
    for (int i = 0; i < guess.size(); ++i)
    {
        if (guess[i] == choice[i])
        {
            status[i] = EXACT;
            score += EXACT;
            letter_counts[guess[i]]--;
        }
    }

    // Second pass for close matches
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

void print_word(std::string guess, int wordsize, std::vector<int> status)
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