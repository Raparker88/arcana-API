"""View module for handling requests about readings"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from arcanaapi.models import Reading, Tarotuser, Cardreading, Position

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
                        card_id: int,
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

        try:
            reading.save()
            serializer = ReadingSerializer(reading, context={'request': request})

            #iterate cards layed out for this reading and save relationships to database
            cards = request.data["cards"]
            for card in cards:

                position = Position.objects.get(pk = card["position_id"])
                cardreading = Cardreading()
                cardreading.card = card
                cardreading.reading = reading
                cardreading.postion = position
                cardreading.inverted = card["inverted"]
                cardreading.save()

            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class CardReadingSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for cards in a reading"""

    class Meta:
        model = Cardreading
        url = serializers.HyperlinkedIdentityField(
            view_name='card',
            lookup_field='id'
        )
        fields = ('id', 'card_id', 'position_id', 'inverted')

class ReadingSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for readings"""

    cardreadings = CardReadingSerializer(many=True)

    class Meta:
        model = Reading
        url = serializers.HyperlinkedIdentityField(
            view_name='reading',
            lookup_field='id'
        )
        fields = ('id', 'tarotuser_id', 'date_created', 'name', 'layout_id',
        'shared', 'cardreadings')
        depth = 1
