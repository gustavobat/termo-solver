from math import log2
import requests
import unicodedata


def remove_accents(input_str):
    return ''.join(c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn')


def safe_log2(x):
    return log2(x) if x > 0. else 0.


def has_no_repeated_letter(word):
    for i in range(len(word)):
        if word.count(word[i]) > 1:
            return False
    return True


def filter_green(words, pos, letter):
    return [word for word in words if word[pos] == letter]


def filter_yellow(known_cells, words, pos, letter):
    forbidden_cells = known_cells.copy()
    forbidden_cells.add(pos)
    for word in words:
        for cell in forbidden_cells:
            if word[cell] == letter or word.count(letter) == 0:
                words.remove(word)
                break

    return words


def filter_grey(words, pos, letter):
    return [word for word in words if word[pos] != letter and word.count(letter) == 0]


def apply_answer(words, answer, guess):
    # 0: green
    # 1: grey
    # 2: yellow
    known_cells = set()
    for i in range(5):
        if answer[i] == 0:
            known_cells.add(i)
    for i in range(len(answer)):
        if answer[i] == 0:
            words = filter_green(words, i, guess[i])
        elif answer[i] == 1:
            words = filter_grey(words, i, guess[i])
        elif answer[i] == 2:
            words = filter_yellow(known_cells, words, i, guess[i])

    return words


def most_probable_guess(words, letter_freq, step):
    guess = ''
    guess_prob = 0.
    for word in words:
        word_prob = 1.
        for i in range(5):
            letter = word[i]
            word_prob *= letter_freq[letter][i]
        if word_prob > guess_prob:
            if step == 0 and has_no_repeated_letter(word) or step != 0:
                guess_prob = word_prob
                guess = word
    return guess


def get_initial_word_list():
    link = "https://raw.githubusercontent.com/fserb/pt-br/e61813bae8897d299cd95047dbe578c1e3ffd00e/tf"
    f = requests.get(link).text
    f = remove_accents(f)
    return [line.split(',')[0] for line in f.rsplit() if len(line.split(',')[0]) == 5], \
           [int(line.split(',')[1]) for line in f.rsplit() if len(line.split(',')[0]) == 5]


def get_letter_freq(words):
    n_words = len(words)
    letters = "abcdefghijklmnopqrstuvxwyz"
    letter_freq = dict()

    for letter in letters:
        letter_freq[letter] = [0.] * 5

    for word in words:
        for i in range(5):
            letter = word[i]
            letter_freq[letter][i] += 1.

    for i in range(5):
        for letter in letters:
            letter_freq[letter][i] = float(letter_freq[letter][i]) / float(n_words)

    return letter_freq


def main():
    words, freq = get_initial_word_list()
    weight = [0.0] * len(words)

    count = 0
    for i in range(len(words)):
        if freq[i] < 3000:
            weight[i] = 0.01
            count += 1
        else:
            weight[i] = 1.0

    letter_freq = get_letter_freq(words)
    good_pick = most_probable_guess(words, letter_freq, 0)
    print(good_pick)
    answer = [1, 2, 1, 1, 1]
    words = apply_answer(words, answer, good_pick)
    letter_freq = get_letter_freq(words)
    good_pick = most_probable_guess(words, letter_freq, 0)
    print(good_pick)

    # 0: green
    # 1: grey
    # 2: yellow
    answer = [1, 1, 2, 0, 2]
    words = apply_answer(words, answer, good_pick)
    letter_freq = get_letter_freq(words)
    good_pick = most_probable_guess(words, letter_freq, 0)
    print(good_pick)

    answer = [2, 2, 0, 0, 0]
    words = apply_answer(words, answer, good_pick)
    letter_freq = get_letter_freq(words)
    good_pick = most_probable_guess(words, letter_freq, 0)
    print(good_pick)


if __name__ == "__main__":
    main()
