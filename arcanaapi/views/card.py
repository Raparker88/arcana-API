from django.http.response import HttpResponseServerError
from django.core.exceptions import ValidationError
import random
from random import shuffle
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from arcanaapi.models import Card

class Cards(ViewSet):

    def list(self, request):
        """Handles GET request for cards"""
        cards = Card.objects.all()
        
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

"""Basic Serializer for cards"""
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('id', 'name', 'card_image', 'explanation', 'inverted_explanation')
        depth = 1