from rest_framework import serializers
from src.likes.models import Likes


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ('id',
                  'liked')
