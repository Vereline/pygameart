from rest_framework import serializers
from .models import Art, ArtComment


class ArtCommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'author',
            'author_id',
            'author_avatar',
            'text',
            'created_date',
            'approved_comment',
        )
        model = ArtComment


class ArtSerializer(serializers.ModelSerializer):
    comments = ArtCommentSerializer(many=True)

    class Meta:
        fields = (
            'id',
            'title',
            'description',
            'creation_date',
            'likes',
            'file_path',
            'file',
            'comments'
        )
        model = Art
