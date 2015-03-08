import random
import time
from app.util import spotify_util
from app.util.wordnik_util import get_parts_of_speech

__author__ = 'Hannah'

# TODO: Add more and put into database
sample_quotes = ['{{band}}\'s first album was better than their first album',
                 'I love {{band}}. Their sound is so surreal, and the newest album helped my cat overcome depression.',
                 '{{band}} puts on a killer show-- I broke all three of my tibias!',
                 'I hear {{band}} had ghost writers compose all their songs. But then they hired an exorcist.',
                 'I wanted {{band}} to play at my wedding, but they were booked. My wife and I settled for a German "Yeah Yeah Yeahs" cover band. They called themselves the "Nein Nein Neins"',
                 'The front-man of {{band}} is a total dream boat.']

sample_quote_sources = ['Credible Source',
                        'Your Grandmother',
                        'Old Man Logan',
                        'Michael Scott',
                        'Shadowfax, Lord of All Horses',
                        'Mysterious Stranger']


# Parse user's Spotify account and generate band based on results
def generate_band_with_token(request):
    band = {
        'name': '',
        'quote': ''
    }

    _prepare_token(request)
    artists = spotify_util.accumulate_artists(request)

    # Get band name
    band['name'] = _parse_spotify_library(request, artists)
    if None is band['name']:
        band['name'] = artists[random.randint(0, len(artists) - 1)]

    band['quote'] = get_random_quote()
    band['quote_source'] = get_random_quote_source()

    return band


def _parse_spotify_library(request, artists):
    words_by_category = {}
    total_templates = []

    # Loop through artists
    for artist in artists:
        # Tokenize artist into words (ex. 'The Front Bottoms' = {'The', 'Front', 'Bottoms'})
        unique_words = {}
        _tokenize(unique_words, artist)

        # Categorize parts of speech for words
        for word in unique_words.keys():
            try:
                # Get parts of speech for word
                parts_of_speech = get_parts_of_speech(word)
                unique_words[word]['parts_of_speech'] = parts_of_speech

                # Catalogue word by parts of speech
                for part_of_speech in parts_of_speech:
                    # If category does not exist yet, instantiate it
                    if part_of_speech not in words_by_category:
                        words_by_category[part_of_speech] = {}
                    words_by_category[part_of_speech][word] = True
            # TODO: Make more specific
            # If invalid word, ignore and continue
            except Exception as e:
                i = 0;
                continue

        # Gather set of options for band name templates
        # (ex. 'The Front Bottoms' = [['pronoun'], ['noun', 'adjective'], ['noun']])
        set_of_options = []
        for word in unique_words.keys():
            set_of_options.append(unique_words[word]['parts_of_speech'])

        # Generate possible templates and record
        templates = generate_templates(set_of_options)
        total_templates = total_templates + templates

    # Get random template
    random_index = random.randint(0, len(total_templates))
    random_template = total_templates[random_index]

    # Generate band name based on template
    band_name = ''
    for part_of_speech in random_template:
        options = list(words_by_category[part_of_speech].keys())
        random_index = random.randint(0, len(options) - 1)
        word = options[random_index]
        band_name += word + ' '

    return band_name.title()


# Generate possible templates based on possible parts of speech
# (ex. 'The Front Bottoms' = [['pronoun', 'noun', 'noun'], ['pronoun', 'adjective', 'noun'], ...])
def generate_templates(set_of_options):
    total_templates = []
    total_templates = _internal_generate_templates(set_of_options, [], total_templates)
    return total_templates


def _internal_generate_templates(set_of_options, template_in_progress, total_templates):
    # Get first options and iterate through
    options = set_of_options[0]
    for option in options:
        # Append option to template-in-progress
        template = template_in_progress.copy()
        template.append(option)
        # If more options available, recurse
        if len(set_of_options) > 1:
            remaining_options = set_of_options[1:len(set_of_options)]
            return _internal_generate_templates(remaining_options, template, total_templates)
        # Otherwise, add template to total
        else:
            total_templates.append(template)

    return total_templates


# TODO: Improve intelligence of tokenizing (i.e. BADBADNOTGOOD = [bad, bad, not, good])
# Tokenizes the words in artist names (i.e. The Front Bottoms = [the, front, bottoms])
def _tokenize(unique_words, artist):
    tokens = artist.split(" ")
    for token in tokens:
        unique_words[token.lower()] = {
            'parts_of_speech': []
        }


# Prepare token for Spotify API usage
def _prepare_token(request):
    # Get token (make sure it exists)
    assert request.session.__contains__('token'), "Cannot generate band: User marked as authorized but token not found!"
    token = request.session.__getitem__('token')

    # Check time elapsed since last refresh
    assert request.session.__contains__(
        'last_token_refresh'), "Cannot check for Spotify token refresh: Time of last refresh not found!"
    last_token_refresh = request.session.__getitem__('last_token_refresh')
    now = time.time()

    # Refresh if needed
    should_refresh = (now - last_token_refresh) > token['expires_in']
    if should_refresh:
        spotify_util.refresh_token(request)
        token = request.session.__getitem__('token')


# Get random quote to show example band usage
def get_random_quote():
    return sample_quotes[random.randint(0, len(sample_quotes) - 1)]


# Get random source for quote
def get_random_quote_source():
    return sample_quote_sources[random.randint(0, len(sample_quote_sources) - 1)]
