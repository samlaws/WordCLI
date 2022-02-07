from email.policy import default
import streamlit as st
from tinge import colored
import itertools
import re
import random


class Wordle:
    def __init__(self):
        self.word_list = list(itertools.chain(
            open("wordle-answers-alphabetical.txt", "r").read().splitlines(),
            open("wordle-allowed-guesses.txt", "r").read().splitlines()))
        self.word = random.choice(self.word_list)
        self.word_letters = list(map(''.join, zip(*[iter(self.word)]*1)))
        self.guess_count = 0
        self.absent_letters = []

    def guess_word(self, guess):
        guess = guess.lower()
        if self.guess_count <= 5:

            if guess not in self.word_list:
                if len(guess) < 5:
                    print("Too short!")
                elif len(guess) > 5:
                    print("Too long!")
                print("Invalid guess")

            elif (guess in self.word_list) & (guess != self.word):
                self.guess_count += 1
                guess_results = []
                guess_letters = list(map(''.join, zip(*[iter(guess)]*1)))
                for l in guess_letters:
                    gidx = guess_letters.index(l)
                    if l in self.word_letters:
                        lidx = self.word_letters.index(l)
                        if lidx == gidx:
                            guess_results.append((l, 'green'))
                        else:
                            guess_results.append((l, 'yellow'))
                    else:
                        self.absent_letters.append(l)
                        guess_results.append((l, 'white'))
                self.print_guess(guess_results)

            elif guess == self.word:
                print("You got it!")

        else:
            print(colored("Game over punk!", "red"))

    def print_guess(self, guess_results):
        [print(colored(x[0], x[1]), end="") for x in guess_results]

    def request_absent_letters(self):
        self.absent_letters = list(dict.fromkeys(self.absent_letters))
        self.absent_letters.sort()
        print("".join(self.absent_letters))


def main():

    st.title("Wordlit")
    # with st.form("params"):
    #    st.write(
    #        "In Wordlit you can select the length of the words you want to guess!")
    #   word_length = st.slider(min_value=3, max_value=10, value=5,
    #                            label="Select number of letters")
    #    submitted = st.form_submit_button("Generate Wordlit")

    if "game" not in st.session_state:
        st.session_state.game = Wordle()

    for i in range(6):
        key = f"key{i}"
        guess = st.text_input(key=key, label="Guess word: ")
        st.write(guess)
        if len(guess) != 0:
            st.session_state.game.guess_word(guess)


main()
