"""View module for handling requests about readings"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from arcanaapi.models import Reading, Tarotuser, Cardreading, Position, Card, Layout


class Readings(ViewSet):


    def list(self, request):
        """Handle GET operations for readings"""

        readings = Reading.objects.all()

        # Support filtering by user
        tarotuser_id = self.request.query_params.get('tarotuser_id', None)
        


        if tarotuser_id is not None:
            tarotuser = Tarotuser.objects.get(pk = tarotuser_id)

            readings = Reading.objects.filter(tarotuser = tarotuser)


        serializer = ReadingSerializer(
            readings, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET request for single reading"""

        try:
            reading = Reading.objects.get(pk=pk)


            serializer = ReadingSerializer(reading, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    
    def create(self, request):
        """Handle POST operations for readings"""

        """
            {
                name: "",
                layout_id: int,
                notes: ""
                cards: [
                    {
                        id: int,
                        inverted: bool,
                        position_id
                    }
                ]
            }
        """

        tarotuser = Tarotuser.objects.get(user=request.auth.user)
        layout = Layout.objects.get(pk=request.data["layout_id"])

        reading = Reading()

        reading.tarotuser = tarotuser
        reading.layout = layout
        reading.notes = request.data["notes"]
        reading.name = request.data["name"]

        
        reading.save()
        serializer = ReadingSerializer(reading, context={'request': request})

        #iterate cards layed out for this reading and save relationships to database
        cards = request.data["cards"]
        for cardObj in cards:

            position = Position.objects.get(pk = int(cardObj["position_id"]))
            card = Card.objects.get(pk = int(cardObj["id"]))
            cardreading = Cardreading()
            cardreading.card = card
            cardreading.reading = reading
            cardreading.position = position
            cardreading.inverted = cardObj["inverted"]
            cardreading.save()

        return Response(serializer.data)

    def patch(self, request, pk=None):
        """Handle patch requests to a users reading"""

        reading = Reading.objects.get(pk = pk)

        reading.notes = request.data['notes']
        reading.name = request.data['name']

        reading.save()

        serializer = ReadingSerializer(reading, context={'request': request})
        

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single reading"""

        try:
            reading = Reading.objects.get(pk=pk)
            reading.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Payment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['put'], detail=True)
    def share(self, request, pk=None):
        """Managing users sharing and unsharing a reading"""

        if request.method == "PUT":
            reading = Reading.objects.get(pk=pk)

            reading.shared = not reading.shared
            reading.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

           
        
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


        
        

class CardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Card

        fields = ('name', 'card_image', 'explanation', 'inverted_explanation')

class CardReadingSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for cards in a reading"""

    card = CardSerializer(many=False)

    class Meta:
        model = Cardreading
        url = serializers.HyperlinkedIdentityField(
            view_name='card',
            lookup_field='id'
        )
        fields = ('id', 'card', 'position_id', 'inverted')

class ReadingSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for readings"""

    cardreadings = CardReadingSerializer(many=True)

    class Meta:
        model = Reading
        url = serializers.HyperlinkedIdentityField(
            view_name='reading',
            lookup_field='id'
        )
        fields = ('id', 'tarotuser_id', 'date_created', 'name', 'notes', 'layout_id', 'comment_count',
        'shared', 'cardreadings')
        depth = 1
