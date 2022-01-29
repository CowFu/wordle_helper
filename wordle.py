import logging


logging.basicConfig(level=logging.ERROR)


# loads words from file specified
def load_words(wordsfile):
    with open(wordsfile) as word_file:
        valid_words = set(word_file.read().split())
    logging.debug("load_words loaded: {}".format(len(valid_words)))
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
                if letter == yellow_list[position]:
                    good_word = False
            if letter in grey_list:
                good_word = False
            position += 1
        if good_word:
            yellow_check = True
            for yellow_letter in yellow_list.values():
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
            results[word] += best_letters[letter]
    return sorted(results.items(), key=lambda item: item[1], reverse=True)


def output_words(english_words, grey_list, yellow_list={}, green_list={}):
    possible_words = valid_words(english_words, grey_list, yellow_list, green_list)
    best_letters = most_common_letters(possible_words)
    best_words = best_word_sort(possible_words, best_letters)
    print("Best words: {}".format(best_words[0:10]))


if __name__ == '__main__':
    offical_words = load_words('official_words.txt')
    all_words = load_words('all_words.txt')

    grey_list = []
    green_list = {}
    yellow_list = {}

    output_words(offical_words, grey_list, yellow_list, green_list)
    output_words(all_words, grey_list + list(green_list.values()), yellow_list)
