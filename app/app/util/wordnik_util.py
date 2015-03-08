from wordnik import swagger
from wordnik.WordApi import WordApi

__author__ = 'Hannah'

# Wordnik API credentials
_API_URL = 'http://api.wordnik.com/v4'
_API_KEY = ''
_CLIENT = swagger.ApiClient(_API_KEY, _API_URL)

# Wordnik APIs
_WORD_API = WordApi(_CLIENT)


# TODO: Investigate multiple words per request
def get_parts_of_speech(word):

    parts_of_speech = {}

    # TODO: Determine how to handle None part of speech (does this only include names?)
    # Accumulate unique parts of speech (i.e. noun, verb, etc.)
    definitions = get_word_definitions(word)
    for definition in definitions:
        parts_of_speech[definition.partOfSpeech] = True

    return parts_of_speech.keys()


def get_word_definitions(word):
    # TODO: Error handling
    result = _WORD_API.getDefinitions(word)

    # TODO: Make this more specific
    # Handle invalid words
    if None == result:
        raise Exception('% is not a valid word!'.format(word))

    return result
