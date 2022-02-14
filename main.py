import requests
import unicodedata


def remove_accents(input_str):
    return ''.join(c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn')


def get_initial_word_list():
    link = "https://raw.githubusercontent.com/fserb/pt-br/master/dicio"
    f = requests.get(link).text
    f = remove_accents(f)

    return [line for line in f.rsplit() if len(line) == 5]


def main():
    words = get_initial_word_list()


if __name__ == "__main__":
    main()
