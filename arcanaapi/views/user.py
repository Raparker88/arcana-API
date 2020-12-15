"""View module for handling requests about rareusers"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from arcanaapi.models import Tarotuser, Sign, Subscription, Reading, Card
from rest_framework.decorators import action
from django.db.models import Q
from .reading import ReadingSerializer


class Users(ViewSet):
    """Users"""
    def list(self, request):
        """Handle GET requests to users resource
        Returns:
            Response -- JSON serialized list of users
        """
        tarotusers = Tarotuser.objects.all()

        #support query param to search by username or full name
        name = self.request.query_params.get('name', None)

        if name is not None:
            tarotusers = []
            users = User.objects.filter(Q(username__contains = name) | Q(first_name__contains = name) | 
            Q(last_name__contains = name))
            
            for user in users:
                tarotuser = Tarotuser.objects.get(pk = user.id)
                tarotusers.append(tarotuser)

        #define value on unmapped property subscribed for each user
        current_user = Tarotuser.objects.get(user=request.auth.user)
        for user in tarotusers:

            try:
                # Determine if the currentuser is subscribed
                subscription = Subscription.objects.get(
                    user=user, follower=current_user)
                user.subscribed = True
            except Subscription.DoesNotExist:
                user.subscribed = False
                


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

            #define value on unmapped property subscribed for the user
            current_user = Tarotuser.objects.get(user=request.auth.user)

            try:
                # Determine if the currentuser is subscribed
                subscription = Subscription.objects.get(
                    user=tarotuser, follower=current_user)
                tarotuser.subscribed = True
            except Subscription.DoesNotExist:
                tarotuser.subscribed = False

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
        
        serializer = TarotUserSerializer(tarotuser, context={'request': request})

        return Response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscription(self, request, pk=None):
        """Managing users subscribing to other user"""

        if request.method == "POST":
            tarotuser = Tarotuser.objects.get(pk=pk)
            current_user = Tarotuser.objects.get(user=request.auth.user)
            

            try:
                # Determine if the user is already subscribed
                subscription = Subscription.objects.get(
                    user=tarotuser, follower=current_user)
                return Response(
                    {'message': 'user already follows this user.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except Subscription.DoesNotExist:
                # The user is not signed up.
                subscription = Subscription()
                subscription.user = tarotuser
                subscription.follower = current_user
                subscription.save()

                return Response({}, status=status.HTTP_201_CREATED)

        # User wants to unsubscribe
        elif request.method == "DELETE":
    
            try:
                tarotuser = Tarotuser.objects.get(pk=pk)
            except Tarotuser.DoesNotExist:
                return Response(
                    {'message': 'user does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the authenticated user
            current_user = Tarotuser.objects.get(user=request.auth.user)

            try:
                # Try to delete the subscription
                subscription = Subscription.objects.get(
                    follower=current_user, user=tarotuser)
                subscription.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            except Subscription.DoesNotExist:
                return Response(
                    {'message': 'Not currently subscribed to user.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        # If the client performs a request with a method of
        # anything other than POST or DELETE, tell client that
        # the method is not supported
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        """Managing GET requests to return a users subscriptions"""

        if request.method == "GET":
            
            current_user = Tarotuser.objects.get(user=request.auth.user)
            
            subscriptions = current_user.subscriptions.all()
            subscribed_readings=[]
            for subscription in subscriptions:
                tarotuser = Tarotuser.objects.get(pk = subscription.user_id)
                readings = Reading.objects.filter(tarotuser = tarotuser)
                for reading in readings:
                    subscribed_readings.append(reading)
                

            serializer = ReadingSerializer(subscribed_readings, many=True, context={'request': request})

            return Response(serializer.data)
            

        #if the client performs a request other than GET
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('id', 'name', 'card_image', 'explanation', 'inverted_explanation')
        depth = 1

class SignSerializer(serializers.ModelSerializer):
    """JSON serializer for astrological sign"""

    class Meta:
        model = Sign
        fields = ("name",)

class TarotUserSerializer(serializers.ModelSerializer):
    """JSON serializer for Tarotuser info in profile detail view"""

    astrology = SignSerializer(many=False)
    card_of_day = CardSerializer(many=False)

    class Meta:
        model = Tarotuser
        fields = ("id", "bio",  "full_name", "profile_image", "username", 
        "astrology", "subscribed", "card_of_day")
