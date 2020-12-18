"""View module for handling requests about positions"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from arcanaapi.models import Position


class Positions(ViewSet):


    def list(self, request):
        """Handle GET operations for positions"""


        # Support filtering by layout id
        layout = self.request.query_params.get('layout', None)
        
        positions = Position.objects.filter(layout__id = layout)

        serializer = PositionSerializer(
            positions, many=True, context={'request': request})
        return Response(serializer.data)

class PositionSerializer(serializers.ModelSerializer):
    """JSON serializer for positions"""


    class Meta:
        model = Position
       
        fields = ('id', 'name', 'explanation')
      