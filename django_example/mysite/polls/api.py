from rest_framework.decorators import api_view

__author__ = 'Hannah'

from .models import Poll
from .serializers import PollSerializer

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

#class PollList(generics.):
 #   polls = Poll.objects.all()
  #  serialized_polls = PollSerializer(polls)
   # return Response(serialized_polls.data)

@api_view(['GET'])
def poll_list(request):
    polls = Poll.objects.all()
    serializer = PollSerializer(polls, many=True)
    return Response(serializer.data)
