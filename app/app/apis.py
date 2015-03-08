import random

from django.http import JsonResponse

from django.shortcuts import redirect

from app.models import Band
from app.serializers import BandSerializer
from app.util.band_util import generate_band_with_token, get_random_quote, get_random_quote_source
from app.util.spotify_util import new_token

__author__ = 'Hannah'

from rest_framework.decorators import api_view
from rest_framework.response import Response

# TODO: Add exception handler so details aren't sent back to users
# Generate a random band name
@api_view(['POST'])
def bands_random(request):
    result = {
        'name': '',
        'quote': ''
    }

    # If authorized, parse user's Spotify library
    if request.session.__contains__('token'):
        result = generate_band_with_token(request)

    # Otherwise, pick a pre-generated band name
    else:
        sample_names = ['Wavves', 'The Front Bottoms', 'Animal Collective', 'Tame Impala', 'Wilco']
        result['name'] = sample_names[random.randint(0, len(sample_names) - 1)]
        result['quote'] = get_random_quote()
        result['quote_source'] = get_random_quote_source()

    # Serialize the output
    band = Band(name=result['name'], quote=result['quote'], quote_source=result['quote_source'])
    serializer = BandSerializer(band)

    # TODO: Remove origin header when hosted
    return Response(serializer.data, headers={'Access-Control-Allow-Origin': '*'})


# Authorize access to user's Spotify account
@api_view(['GET'])
def spotify_authorize(request):
    # TODO: Prevent cross origin attacks
    # state = request.query_params.get('state', None)
    new_token(request)

    # Redirect user back to homepage
    return redirect('/')


# Check if user authorized access to Spotify
def spotify_is_authorized(request):
    # Check if user authorized Spotify access
    is_authorized = request.session.__contains__('token')
    response = {
        'is_authorized': is_authorized
    }

    return JsonResponse(response)