import base64
import json
import requests
import time

__author__ = 'Hannah'

# Standardize private variables
_TRACK_LIMIT = 25
_TRACKS_PER_PAGE = 25

# TODO: Inject onto front-end
REDIRECT_URI = 'http://localhost:8000/spotify/authorize'

# API endpoints
_TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'
_GET_TRACKS_ENDPOINT = 'https://api.spotify.com/v1/me/tracks'

# oAuth information
_CLIENT_ID = ''
_CLIENT_SECRET = ''


def accumulate_artists(request):

    total_tracks = []
    offset = 0

    # Accumulate paginated tracks from user's Spotify library
    end_of_results = False
    while not end_of_results:
        # Add tracks from result
        results = get_tracks_paged(request, _TRACKS_PER_PAGE, offset)
        tracks = results['items']
        total_tracks.extend(tracks)

        # Get number of tracks received and update offset
        num_of_tracks = len(tracks)
        offset += num_of_tracks

        # Check if reached end of user's library
        end_of_results = num_of_tracks >= _TRACK_LIMIT

    unique_artists = {}

    # Record unique artists from tracks
    for track in total_tracks:
        # TODO: Simplify
        unique_artists[track['track']['artists'][0]['name']] = True

    return list(unique_artists.keys())


def get_tracks_paged(request, limit, offset):

    assert request.session.__contains__('token'), "Cannot get paged track results from Spotify: token not found!"
    response = requests.get(_GET_TRACKS_ENDPOINT,
                        headers={
                            'Authorization': 'Bearer {}'.format(request.session.__getitem__('token')['access_token'])
                        },
                        params={
                            'limit': limit,
                            'offset': offset
                        })

    tracks = json.loads(response.text)
    return tracks


def refresh_token(request):

    assert request.session.__contains__('refresh_token'), "Cannot refresh Spotify token: Refresh token not found!"

    # Payload
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': request.session.__getitem__('refresh_token')
    }

    # Headers
    auth_str = '{}:{}'.format(_CLIENT_ID, _CLIENT_SECRET)
    encoded_authorization = (base64.b64encode(auth_str.encode('ascii'))).decode('UTF-8')
    headers = {
        'Authorization': 'Basic {}'.format(encoded_authorization)
    }

    # Refresh token
    __request_token__(request, payload, headers)


def new_token(request):
    # Build payload for token request
    payload = {
        'client_id': _CLIENT_ID,
        'client_secret': _CLIENT_SECRET,
        'code': request.query_params.get('code', None),
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }

    # Request token
    __request_token__(request, payload)


def __request_token__(request, payload, headers={}):
    # TODO: error handling
    response = requests.post(_TOKEN_ENDPOINT, data=payload, headers=headers)

    # Store token and timestamp in session
    token = json.loads(response.text)
    request.session.__setitem__('token', token)
    request.session.__setitem__('last_token_refresh', time.time())

    # If refresh token exists, store it (since we only receive it once!)
    if 'refresh_token' in token:
        request.session.__setitem__('refresh_token', token['refresh_token'])
