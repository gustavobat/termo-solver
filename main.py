from math import log2
import os
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

    file_name = "word_list.txt"
    if not os.path.exists(file_name):
        with open(file_name, 'wb') as fout:
            url = "https://raw.githubusercontent.com/fserb/pt-br/e61813bae8897d299cd95047dbe578c1e3ffd00e/tf"
            response = requests.get(url, stream=True)
            response.raise_for_status()
            for block in response.iter_content(4096):
                fout.write(block)
            fout.close()

    f = open(file_name, "r").read()
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


def get_word_entropy(word, words):
    n_words = float(len(words))
    entropy = 0.
    for a0 in range(3):
        for a1 in range(3):
            for a2 in range(3):
                for a3 in range(3):
                    for a4 in range(3):
                        answer = [a0, a1, a2, a3, a4]
                        remaining_words = words.copy()
                        remaining_words = apply_answer(remaining_words, answer, word)
                        n_remaining_words = float(len(remaining_words))
                        prob = n_remaining_words / n_words
                        entropy += -1 * prob * safe_log2(prob)
    print("Word: " + word + ", entropy: " + str(entropy))
    return entropy


def main():
    words, freq = get_initial_word_list()
    print(len(words))
    copy_words = words.copy()
    for i in range(len(words)):
        if freq[i] < 10000:
            copy_words.remove(words[i])

    print(len(copy_words))
    #weight = [0.0] * len(words)

    # for i in range(len(words)):
    #    weight[i] = 0.01 if freq[i] < 3000 else 1.0
    words = copy_words
    best_initial_pick = ''
    best_initial_pick_entropy = 0.
    for word in words:
        entropy = get_word_entropy(word, words)
        if entropy > best_initial_pick_entropy:
            best_initial_pick = words
            best_initial_pick_entropy = entropy
    print("Best initial word: " + best_initial_pick)


if __name__ == "__main__":
    main()
