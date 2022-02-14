import requests
import unicodedata


def remove_accents(input_str):
    return ''.join(c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn')


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
    link = "https://raw.githubusercontent.com/fserb/pt-br/master/dicio"
    f = requests.get(link).text
    f = remove_accents(f)

    return [line for line in f.rsplit() if len(line) == 5]


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
    words = get_initial_word_list()
    print('Possible solutions: ' + str(len(words)))
    letter_freq = get_letter_freq(words)
    good_pick = most_probable_guess(words, letter_freq, 0)
    print(good_pick)


if __name__ == "__main__":
    main()
