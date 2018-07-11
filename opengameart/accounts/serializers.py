from rest_framework import serializers
from .models import ArtUser, ArtPost
from arts.serializers import ArtSerializer


class ArtUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'user_id',
            'location',
            'birth_date',
            'description',
            'art_direction',
            'user_avatar',
            'get_username',  # this is the method from model
        )
        model = ArtUser

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('user')
        user = ArtUserSerializer.create(ArtUserSerializer(), validated_data=user_data)
        art = ArtSerializer.create(ArtSerializer(), validated_data=validated_data.pop('art'))
        art_post, created = ArtPost.objects.update_or_create(user=user, art=art)
        return art_post


class ArtPostSerializer(serializers.ModelSerializer):
    """  Post which will be published """
    user = ArtUserSerializer(required=True)
    art = ArtSerializer(required=True)

    class Meta:
        model = ArtPost
        fields = ('user', 'art')

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('user')
        user = ArtUserSerializer.create(ArtUserSerializer(), validated_data=user_data)
        art = ArtSerializer.create(ArtSerializer(), validated_data=validated_data.pop('art'))
        art_post, created = ArtPost.objects.update_or_create(user=user, art=art)
        return art_post
