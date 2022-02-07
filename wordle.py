from tinge import colored, success
import itertools
import argparse
import random


class Wordle:
    def __init__(self, num_letters, max_guesses):
        print("Welcome to WorldCLI!")
        self.guess_count = 0
        self.max_guesses = max_guesses
        self.num_letters = num_letters
        self.absent_letters = []
        self.word_list = list(itertools.chain(
            open("2of12.txt", "r").read().splitlines()))
        self.word_list = [x for x in self.word_list if (
            len(x) == num_letters) & ("-" not in x)]
        self.word = random.choice(self.word_list)
        self.word_letters = list(map(''.join, zip(*[iter(self.word)]*1)))
        self.guess_results = []

    def guess_word(self, guess):
        guess = guess.lower()
        if self.guess_count <= self.max_guesses:
            if guess not in self.word_list:
                self.print_guess(self.guess_results)
                if len(guess) < self.num_letters:
                    print("Too short!")
                elif len(guess) > self.num_letters:
                    print("Too long!")
                else:
                    print("Invalid guess!")

            elif (guess in self.word_list) & (guess != self.word):
                self.guess_count += 1
                guess_letters = list(map(''.join, zip(*[iter(guess)]*1)))
                for l in guess_letters:
                    gidx = guess_letters.index(l)
                    if l in self.word_letters:
                        lidx = self.word_letters.index(l)
                        if lidx == gidx:
                            self.guess_results.append((l.upper(), 'green'))
                        else:
                            self.guess_results.append((l.upper(), 'yellow'))
                    else:
                        self.absent_letters.append(l.upper())
                        self.guess_results.append((l.upper(), 'white'))
                self.guess_results.append(("\n", 'white'))
                self.print_guess(self.guess_results)

            elif guess == self.word:
                for l in guess:
                    self.guess_results.append((l.upper(), 'green'))
                self.print_guess(self.guess_results)

                print(colored("\nYou got it!", "green"))

    def print_guess(self, guess_results):
        print("", end="\r\r")
        [print(colored(x[0], x[1]), end="") for x in guess_results]

    def request_absent_letters(self):
        self.absent_letters = list(dict.fromkeys(self.absent_letters))
        self.absent_letters.sort()
        print("".join(self.absent_letters))


def parse_args(args=None):
    p = argparse.ArgumentParser()
    p.add_argument('-g', '--guesses', default=6, type=int,
                   help='Maximum number of guesses to allow')
    p.add_argument('-l', '--length', default=5, type=int,
                   help='Length of word to guess')

    args = p.parse_args(args)

    return p, args


def main(args=None):
    p, args = parse_args(args)
    game = Wordle(args.length, args.guesses)

    success = False
    while game.guess_count < args.guesses:
        try:
            guess = input(f"\nGuess {game.guess_count + 1}: ")
            game.guess_word(guess)
            if game.word == guess:
                success = True
                break

        except (KeyboardInterrupt, EOFError):
            print()
            print("Interrupted, giving up...")
            break

    if not success:
        print(colored("\nGame over punk!", "red"))
        print(f"The word was: {game.word}")


if __name__ == "__main__":
    # init wordle
    main()
