from rest_framework import serializers
from . import models

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = (
            'id', 
            'title',
            'content',
            'picture_1',
            'picture_2',
            'picture_3',
            'picture_4',
            'picture_5',
            'created_at',
            'updated_at',
            )
