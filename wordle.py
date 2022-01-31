import logging


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
    logging.debug("valid_words called: \ngrey list: {}\nyellow_list: {}\ngreen_list: {}"
                  .format(grey_list, yellow_list, green_list))
    valid_words = []
    for word in words:
        position = 0
        good_word = True
        for letter in word:
            logging.debug("checking: {}".format(letter))
            if position in green_list:
                logging.debug("found position in green list")
                if letter != green_list[position]:
                    good_word = False
            elif position in yellow_list:
                logging.debug("found position in yellow list")
                for yellow_letter in yellow_list[position]:
                    if letter == yellow_letter:
                        logging.debug("failed yellow letter")
                        good_word = False
            if letter in grey_list and letter not in green_list and letter not in yellow_list:
                logging.debug("letter: {} grey list {}".format(letter, grey_list))
                logging.debug("failed grey list")
                good_word = False
            position += 1
        if good_word:
            yellow_check = True
            for yellow_value in yellow_list.values():
                for yellow_letter in yellow_value:
                    logging.debug(yellow_letter)
                    if yellow_letter not in word:
                        logging.debug("failed yellow check")
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
    return sorted(results.items(), key=lambda item: item[1], reverse=True)


def output_words(official_words, all_words, grey_list, yellow_list={}, green_list={}):
    possible_words = valid_words(official_words, grey_list, yellow_list, green_list)
    best_letters = most_common_letters(possible_words)
    best_words = best_word_sort(possible_words, best_letters)
    print("Possible words: {}".format(best_words[0:10]))
    best_words = best_word_sort(all_words, best_letters)
    print("Best words: {}".format(best_words[0:10]))


if __name__ == '__main__':
    offical_words = load_words('official_words.txt')
    all_words = load_words('all_words.txt')

    result_char_list = ["x", "g", "y"]
    guess = 'start'

    grey_list = []
    green_list = {}
    yellow_list = {}

    while guess not in ['', 'quit', 'q']:
        output_words(offical_words, all_words, grey_list, yellow_list, green_list)

        while True:
            guess = input("Which word did you use? ").lower()
            if len(guess) != 5 or not guess.isalpha():
                if guess in ['', 'quit', 'q']:
                    exit()
                print("please enter a 5 letter word")
                continue
            break

        while True:
            status = input("What was the result? (x=grey g=green y=yellow) ").lower()
            matched_list = [characters in result_char_list for characters in status]
            if len(status) != 5 or not all(matched_list):
                if status in ['', 'quit', 'q']:
                    exit()
                print("please enter 5 letters using x, g, y (xxgyx)")
                continue
            break
        logging.info("guess: {} status: {}".format(guess, status))

        for i in range(0, len(status)):
            logging.info("i: {}, status[i]: {}".format(i, status[i]))
            if status[i] == 'x':
                grey_list.append(guess[i])
            elif status[i] == 'g':
                green_list[i] = guess[i]
                logging.info("set greenlist[i] to: {}".format(green_list))
            elif status[i] == 'y':
                if i in yellow_list.keys():
                    yellow_list[i].append(guess[i])
                else:
                    yellow_list[i] = [guess[i]]

        # print("grey_list: {}".format(grey_list))
        # print("green_list: {}".format(green_list))
        # print("yellow_list: {}".format(yellow_list))
