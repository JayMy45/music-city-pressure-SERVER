from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from mcpressureapi.models import Progress

class ProgressView(ViewSet):

    def list(self, request):
        """Get request to get all progress

        Returns:
            Response -- JSON serialized list of progress
        """

        progress = Progress.objects.all()
        serialized = ProgressSerializer(progress, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Progress
        fields = ('id','label', )