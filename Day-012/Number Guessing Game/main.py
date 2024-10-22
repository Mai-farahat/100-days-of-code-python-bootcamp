# Number Guessing Game Objectives:

# Include an ASCII art logo
import random
from art import logo

EASY_ATTEMPTS = 10
HARD_ATTEMPTS = 5


def set_difficulty():
    temp = input("Choose a difficulty. Type 'easy' or 'hard': ")
    if temp == 'easy':
        return EASY_ATTEMPTS
    else:
        return HARD_ATTEMPTS


def check_answer(guess, answer, turns):
    """checks answer against guess. Returns the number of turns remaining."""
    if guess > answer:
        print("Too high.")
        return turns - 1
    elif guess < answer:
        print("Too low.")
        return turns - 1
    else:
        print(f"You got it! The answer was {answer}.")


def game():
    print(logo)
    print("Welcome to the Number Guessing Game!\nI'm thinking of a number between 1 and 100.")
    actual_answer = random.randint(1, 100)
    print(f"Pssst, the correct answer is {actual_answer}")

    turns = set_difficulty()
    guess = 0
    while guess != actual_answer:
        print(f"You have {turns} attempts remaining to guess the number.")
        guess = int(input("Make a guess: "))

        turns = check_answer(guess, actual_answer, turns)

        if turns == 0:
            print("You've run out of guesses, you lose.")
            return
        elif guess != actual_answer:
            print("Guess again.")


game()
