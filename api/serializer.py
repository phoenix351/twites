from .models import Tweet
from rest_framework import serializers

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = '__all__' #menampilkan semua field pada class Album

