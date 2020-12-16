"""View module for handling requests about readings"""
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from arcanaapi.models import Sign
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

@permission_classes((AllowAny, ))
class Signs(ViewSet):


    def list(self, request):
        """Handle GET operations for readings"""

        signs = Sign.objects.all()
        
        serializer = SignSerializer(
            signs, many=True, context={'request': request})
        return Response(serializer.data)

class SignSerializer(serializers.ModelSerializer):
    """JSON serializer for signs"""

    class Meta:
        model = Sign
        fields = ('id', 'name')
    
