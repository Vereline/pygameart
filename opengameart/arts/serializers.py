from rest_framework import serializers
from .models import Art


class ArtSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'description',
            'creation_date',
            'likes',
            'file_path',
            'file'
        )
        model = Art
