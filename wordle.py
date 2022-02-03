import logging
from random import sample
import os

os.system("")
logging.basicConfig(level=logging.INFO)


# loads words from file specified
def load_words(wordsfile):
    try:
        with open(wordsfile) as word_file:
            valid_words = set(word_file.read().split())
        logging.debug("load_words loaded: {}".format(len(valid_words)))
    except FileNotFoundError:
        logging.error("Could not find word file {}".format(wordsfile))
    else:
        return valid_words


# checks to see which words are valid given a grey, yellow and green list
def valid_words(words, grey_list, yellow_list, green_list):
    logging.debug(
        "valid_words called: \ngrey list: {}\nyellow_list: {}\ngreen_list: {}".format(
            grey_list, yellow_list, green_list
        )
    )
    valid_words = []
    for word in words:
        position = 0
        good_word = True
        for letter in word:
            if position in green_list:
                if letter != green_list[position]:
                    good_word = False
            elif position in yellow_list:
                for yellow_letter in yellow_list[position]:
                    if letter == yellow_letter:
                        good_word = False
            if (
                letter in grey_list
                and letter not in green_list
                and letter not in yellow_list
            ):
                good_word = False
            position += 1
        if good_word:
            yellow_check = True
            for yellow_value in yellow_list.values():
                for yellow_letter in yellow_value:
                    logging.debug(yellow_letter)
                    if yellow_letter not in word:
                        yellow_check = False
            if yellow_check:
                valid_words.append(word)
    return valid_words


# look through every word and find the most used letters returns a dict of letters
# as keys and number of appearences as values
def most_common_letters(english_words):
    alpha_dict = {}
    for word in english_words:
        for letter in word:
            if letter in alpha_dict:
                alpha_dict[letter] = alpha_dict[letter] + 1
            else:
                alpha_dict[letter] = 1
    return dict(sorted(alpha_dict.items(), key=lambda item: item[1], reverse=True))


# sorts a list of words by their "scrabble" value. Given the value is in the dict
# passed to the function
def best_word_sort(words, best_letters):
    results = {}
    for word in words:
        results[word] = 0
        word_set = set(word)
        for letter in word_set:
            if letter not in best_letters:
                best_letters[letter] = 0
            results[word] += best_letters[letter]
    results = sorted(results.items(), key=lambda item: item[1], reverse=True)
    return results[0:5]


def output_words(official_words, all_words, grey_list, yellow_list={}, green_list={}):
    possible_words = valid_words(official_words, grey_list, yellow_list, green_list)
    best_letters = most_common_letters(possible_words)
    best_words = best_word_sort(possible_words, best_letters)
    # print(*(a[0] for a in best_words))
    print("Possible words: {}".format(list(a[0] for a in best_words)))
    best_words = best_word_sort(all_words, best_letters)
    print("Best words: {}".format(list(a[0] for a in best_words)))


def user_guess():
    while True:
        guess = input("Enter a word: ").lower()
        if len(guess) != 5 or not guess.isalpha():
            if guess in ["", "quit", "q"]:
                exit()
            print("please enter a 5 letter word")
            continue
        break
    return guess


def game():
    answer = sample(list(offical_words), 1)
    answer = answer[0]
    logging.debug("word is: {}".format(answer))
    guess = ""
    while guess != answer:
        answer_left = list(answer)
        guess = user_guess()
        used_guess = [False, False, False, False, False]
        feedback = list(guess)

        position = 0
        for letter in guess:
            # green answers
            if guess[position] == answer[position]:
                feedback[position] = "\033[1;32;40m " + letter
                answer_left[position] = ""
                used_guess[position] = True
                logging.debug("{} set to green".format(letter))
            position += 1
        # yellow answers
        position = 0
        logging.debug("{}".format(used_guess))
        for letter in guess:
            logging.debug("answer left: {}".format(answer_left))
            if letter in answer_left and not used_guess[position]:
                feedback[position] = "\u001b[33m " + letter
                answer_left[answer_left.index(letter)] = ""
                logging.debug("{} set to yellow".format(letter))
                used_guess[position] = True
            # grey answers
            elif not used_guess[position]:
                feedback[position] = "\u001b[0m " + letter
                logging.debug("{} set to grey".format(letter))
            position += 1

        for i in feedback:
            print(i, end="")
        print("\u001b[0m")  # resets console color


def wordle_helper(
    output_words,
    user_guess,
    offical_words,
    all_words,
    result_char_list,
    game_choice,
    grey_list,
    green_list,
    yellow_list,
    game_mode=False,
    game_guess="",
):
    while game_choice not in ["", "quit", "q"]:
        output_words(offical_words, all_words, grey_list, yellow_list, green_list)

        if game_mode:
            guess = game_guess
        else:
            guess = user_guess()

        while True:
            status = input("What was the result? (x=grey g=green y=yellow) ").lower()
            matched_list = [characters in result_char_list for characters in status]
            if len(status) != 5 or not all(matched_list):
                if status in ["", "quit", "q"]:
                    exit()
                print("please enter 5 letters using x, g, y (xxgyx)")
                continue
            break
        logging.debug("guess: {} status: {}".format(guess, status))
        if status == "ggggg":
            break
        for i in range(0, len(status)):
            logging.debug("i: {}, status[i]: {}".format(i, status[i]))
            if status[i] == "x":
                grey_list.append(guess[i])
            elif status[i] == "g":
                green_list[i] = guess[i]
                logging.debug("set greenlist[i] to: {}".format(green_list))
            elif status[i] == "y":
                if i in yellow_list.keys():
                    yellow_list[i].append(guess[i])
                else:
                    yellow_list[i] = [guess[i]]
        if game_mode:
            break


if __name__ == "__main__":
    offical_words = load_words("official_words.txt")
    all_words = load_words("all_words.txt")

    result_char_list = ["x", "g", "y"]
    print("1. Play \u001b[33mWordle\u001b[0m")
    print("2. Wordle Helper")
    print("enter 'q' or 'quit' to quit")
    game_choice = input()

    grey_list = []
    green_list = {}
    yellow_list = {}

    if game_choice == "1":
        play_again = True
        while play_again:
            game()
            print("would you like to play again?\n1. yes\n2. no")
            play_again_str = input()
            if play_again_str not in ["yes", "y", "1"]:
                play_again = False
        exit()

    if game_choice == "2":
        play_again = True
        while play_again:
            wordle_helper(
                output_words,
                user_guess,
                offical_words,
                all_words,
                result_char_list,
                game_choice,
                grey_list,
                green_list,
                yellow_list,
            )
            print("would you like to play again?\n1. yes\n2. no")
            play_again_str = input()
            if play_again_str not in ["yes", "y", "1"]:
                play_again = False
