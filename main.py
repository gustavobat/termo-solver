import requests
import unicodedata


def remove_accents(input_str):
    return ''.join(c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn')


def has_no_repeated_letter(word):
    for i in range(len(word)):
        if word.count(word[i]) > 1:
            return False
    return True


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
        letter_freq[letter] = [0] * 5

    for word in words:
        for i in range(5):
            letter = word[i]
            letter_freq[letter][i] += 1

    for i in range(5):
        for letter in letters:
            letter_freq[letter][i] = float(letter_freq[letter][i]) / float(n_words)

    return letter_freq


def main():
    words = get_initial_word_list()


if __name__ == "__main__":
    main()
