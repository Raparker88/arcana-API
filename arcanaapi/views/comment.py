"""View module for handling requests about comments"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from arcanaapi.models import Reading, Tarotuser, Comment
from .user import TarotUserSerializer


class Comments(ViewSet):


    def list(self, request):
        """Handle GET operations for comments"""


        # Support filtering by reading
        reading = self.request.query_params.get('reading', None)
        
        comments = Comment.objects.filter(reading__id = reading)

        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)


    
    def create(self, request):
        """Handle POST operations for readings"""

        """
            {
                reading_id: int,
                comment: ""
            }
        """

        tarotuser = Tarotuser.objects.get(user=request.auth.user)
        reading = Reading.objects.get(pk = request.data["reading_id"])
        comment = Comment()

        comment.tarotuser = tarotuser
        comment.comment = request.data["comment"]
        comment.reading = reading

        
        comment.save()
        serializer = CommentSerializer(comment, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single commment"""

        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Payment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
class TarotUserSerializer(serializers.ModelSerializer):
    """JSON serializer for tarotusers related to comments"""
    

    class Meta:
        model = Tarotuser
       
        fields = ('id', 'username')
        

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    
    tarotuser = TarotUserSerializer(many=False)

    class Meta:
        model = Comment
       
        fields = ('id', 'tarotuser', 'tarotuser_id', 'date_created', 'reading_id', 'comment')
        depth = 1
        
      
