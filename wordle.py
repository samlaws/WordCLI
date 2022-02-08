import random
import string
import argparse
import itertools
import pandas as pd
from tinge import colored
from pandas.api.types import CategoricalDtype


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
                    print("\nToo short!")
                elif len(guess) > self.num_letters:
                    print("\nToo long!")
                else:
                    print("\nInvalid guess!")

            elif (guess in self.word_list) & (guess != self.word):
                self.guess_count += 1
                guess_letters = list(map(''.join, zip(*[iter(guess)]*1)))
                guess_index = 0
                for l in guess_letters:
                    gidx = guess_letters.index(l)

                    if l in self.word_letters:
                        lidx = self.word_letters.index(l)
                        if len([x for x in guess_letters if x == l]) == 1:
                            if lidx == gidx:
                                self.guess_results.append((l.upper(), 'green'))
                            else:
                                self.guess_results.append(
                                    (l.upper(), 'yellow'))
                        elif len([x for x in guess_letters if x == l]) > 1:
                            lidxs = [index for index, element in enumerate(
                                self.word_letters) if element == l]
                            gidxs = [index for index, element in enumerate(
                                guess_letters) if element == l]
                            gidx = gidxs[guess_index]

                            try:
                                lidxs_guess_indexed = lidxs[guess_index]
                            except IndexError:
                                lidxs_guess_indexed = lidx
                            if lidxs_guess_indexed == gidxs[guess_index]:
                                self.guess_results.append((l.upper(), 'green'))
                            elif gidx == lidxs[0]:
                                self.guess_results.append(
                                    (l.upper(), 'yellow'))
                            else:
                                self.guess_results.append((l.upper(), 'white'))
                            guess_index += 1
                    else:
                        self.absent_letters.append(l.upper())
                        self.guess_results.append((l.upper(), 'white'))
                self.guess_results.append(("\n", 'white'))
                self.print_guess(self.guess_results)

            elif guess == self.word:
                for l in guess:
                    self.guess_results.append((l.upper(), 'green'))
                self.print_guess(self.guess_results)

                print(colored("\n\nYou got it!", "green"))

    def print_guess(self, guess_results):
        print("", end="\r\r")
        alphabet = list(string.ascii_uppercase)
        guess_results_copy = guess_results.copy()
        for letter in alphabet:
            guess_results_copy.append((letter, "white"))
        guess_df = pd.DataFrame(
            guess_results_copy, columns=["letter", "status"])
        guess_df.drop_duplicates(inplace=True)
        sorted_guesses = self.sort_guesses(guess_df)

        [print(colored(x[0], x[1]), end="") for x in guess_results]
        print()
        [print(colored(x[0], x[1]), end="") for x in sorted_guesses]
        print()

    def sort_guesses(self, guess_df):
        cat_size_order = CategoricalDtype(
            ["white", "yellow", "green"],
            ordered=True
        )
        guess_df['status'] = guess_df['status'].astype(cat_size_order)
        guess_df = guess_df.sort_values(by="status", ascending=False)
        guess_df.drop_duplicates(subset="letter", keep="first", inplace=True)
        guess_df = guess_df[guess_df["letter"] != "\n"]
        guess_df_sorted = guess_df.sort_values(by="letter", ascending=True)
        sorted_guesses = list(guess_df_sorted.to_records(index=False))
        return sorted_guesses

    def request_absent_letters(self):
        self.absent_letters = list(dict.fromkeys(self.absent_letters))
        self.absent_letters.sort()


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
        print(colored("Game over punk!", "red"))
        print(f"The word was: {game.word}")


if __name__ == "__main__":
    # init wordle
    main()
