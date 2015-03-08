from rest_framework import serializers
from app.models import Band

__author__ = 'Hannah'


class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
