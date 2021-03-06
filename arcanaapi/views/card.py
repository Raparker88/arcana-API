"""view module for handling requests about cards"""

from django.http.response import HttpResponseServerError
from django.core.exceptions import ValidationError
import random
from random import shuffle
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from arcanaapi.models import Card

class Cards(ViewSet):

    def list(self, request):
        """Handles GET request for cards"""
        cards = list(Card.objects.all())
        shuffle(cards)
        
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

"""Basic Serializer for cards"""
class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('id', 'name', 'card_image', 'explanation', 'inverted_explanation', 'inverted')
        depth = 1