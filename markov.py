"""Generate Markov text from text files."""

from random import choice
import sys


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    long_text = ""

    for f in file_path:
        with open(f) as text_file:
            long_text += text_file.read()
            #long_text = long_text.replace("\n", " ")
            #words = long_text.split()

    return long_text


def combine_strings(text1, text2):
    """ Concatenate text (string) from two files. """

    return text1 + text2


def make_chains(text_string, n_grams):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    words = text_string.split()  # creates list from text_string
    words.append(None)  # add none at end of list to indicate stopping point

    #Looping through up and including last pair
    for i in range(len(words)-n_grams):
        extract_words = words[i:i+n_grams]
        state = tuple(extract_words)  # creates tuple of bigram
        transition = words[i + n_grams]  # creates value of word following bigram
        chains[state] = chains.get(state, [])  # checks if bigram in dict, creates empty list if not
        chains[state].append(transition)  # adds to transition list

    return chains


def make_text(chains, n_grams):
    """Return text from chains."""

    words = []
    start_key = pull_cap(chains)
    words.extend(start_key)
    new_key = start_key

    while True:
        combo_list = chains[new_key]
        transition = choice(combo_list)

        if (transition is None):
            break
        elif (end_punc(transition) is True):
            words.append(transition)
            break

        words.append(transition)
        extract_words = list(new_key[1:])
        extract_words.append(transition)
        new_key = tuple(extract_words)

        # if new_key not in chains:
        #     break

    return " ".join(words)


def pull_cap(chains):
    """ Generates start key until first word is capitalized. """
    while True:
        start_key = choice(chains.keys())

        if start_key[0].title() == start_key[0]:
            return start_key


def end_punc(transition):
    """Determines if value ends in (. ! ?)"""
    punctuation = set([".", "!", "?"])

    #last_word = new_key[-1]

    if transition[-1] in punctuation:
        return True
    else:
        return False


input_path = sys.argv[1:]
#sys.argv is a list of files (e.g., python markov.py green-eggs.txt gettysburg.txt)

n_grams = 2

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, n_grams)

# Produce random text
random_text = make_text(chains, n_grams)

print random_text
