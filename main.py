from math import log2
import os
import requests
import unicodedata


def remove_accents(input_str):
    return ''.join(c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn')


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


def filter_unusual_words(words, freq, threshold):
    filtered_words = list()
    for i in range(len(words)):
        if freq[i] > threshold:
            filtered_words.append(words[i])
    return filtered_words


def filter_green(words, pos, letter):
    return [word for word in words if word[pos] == letter]


def filter_yellow(known_cells, words, pos, letter):
    forbidden_cells = known_cells.copy()
    forbidden_cells.add(pos)
    new_words = list()
    for word in words:
        for cell in forbidden_cells:
            if word[cell] != letter and word.count(letter) != 0:
                new_words.append(word)
                break

    return new_words


def filter_grey(words, pos, letter):
    return [word for word in words if word[pos] != letter and word.count(letter) == 0]


def apply_answer(words, answer, guess):
    # 0: green
    # 1: grey
    # 2: yellow
    words.remove(guess)
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


def safe_log2(x):
    return log2(x) if x > 0. else 0.


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
    words = filter_unusual_words(words, freq, 3000)

    print(len(words))

    pick = ''
    pick_entropy = 0.
    for word in words:
        entropy = get_word_entropy(word, words)
        if entropy > best_initial_pick_entropy:
            best_initial_pick = words
            best_initial_pick_entropy = entropy
    print("Best initial word: " + best_initial_pick)


if __name__ == "__main__":
    main()
