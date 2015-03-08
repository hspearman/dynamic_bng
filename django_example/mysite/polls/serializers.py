__author__ = 'Hannah'

from .models import Poll
from rest_framework import serializers

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = (
           'question',
        )
