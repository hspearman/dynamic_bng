import uuid

__author__ = 'Hannah'

from django.db import models

# class Word(models.Model):
#     id = models.IntegerField()
#     word = models.CharField()
#     # TODO: Make this an enum
#     part_of_speech = models.CharField()

class Band(models.Model):
    # TODO: UUID field?
    # id = models.UUIDField()
    id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    name = models.CharField()
    quote = models.CharField()
    quote_source=models.CharField()