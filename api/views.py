
from rest_framework import viewsets

from .serializer import TweetSerializer
from .models import Tweet


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('Time')
    serializer_class = TweetSerializer