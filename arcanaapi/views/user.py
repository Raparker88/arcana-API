"""View module for handling requests about rareusers"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from arcanaapi.models import Tarotuser
from rest_framework.decorators import action


class Users(ViewSet):
    """Users"""
    def list(self, request):
        """Handle GET requests to users resource
        Returns:
            Response -- JSON serialized list of users
        """
        tarotusers = Tarotuser.objects.all()
        serializer = TarotUserSerializer(
            tarotusers, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handles GET requests to users resource for single User
        Written for User Profile View
        Returns:
            Response -- JSON serielized rareuser instance
        """
        try:
            tarotuser = Tarotuser.objects.get(pk=pk)

            serializer = TarotUserSerializer(tarotuser, many=False, context={'request': request})

            return Response(serializer.data)

        except Tarotuser.DoesNotExist:
            return Response(
                {'message': 'User does not exist.'},
                status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        """Handle PUT and PATCH requests for user details"""

        tarotuser = Tarotuser.objects.get(pk = pk)

        if "profile_image" in request.data:

            format, imgstr = request.data["profile_image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'"profile_image"-{uuid.uuid4()}.{ext}')
            tarotuser.profile_image = data
            

        if "bio" in request.data:

            tarotuser.bio = request.data["bio"]

        tarotuser.save()

        serializer = TarotUserSerializer(tarotuser, context={'request': request})
        

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    @action(methods=['get'], detail=False)
    def current_user(self, request):

        tarotuser = Tarotuser.objects.get(user=request.auth.user)
        
        serializer = TarotUserSerializer(current_user, context={'request': request})

        return Response(serializer.data)



class TarotUserSerializer(serializers.ModelSerializer):
    """JSON serializer for Tarotuser info in profile detail view"""
    class Meta:
        model = Tarotuser
        fields = ("id", "bio",  "full_name", "profile_image", "username")
