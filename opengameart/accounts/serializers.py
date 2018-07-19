from rest_framework import serializers
from .models import ArtUser, ArtPost, RELATIONSHIP_BLOCKED, RELATIONSHIP_FOLLOWING
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
        :param validated_data: data containing all the details of art user
        :return: returns a successfully created art user post
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
        :param validated_data: data containing all the details of art user
        :return: returns a successfully created art user post
        """
        user_data = validated_data.pop('user')
        user = ArtUserSerializer.create(ArtUserSerializer(), validated_data=user_data)
        art = ArtSerializer.create(ArtSerializer(), validated_data=validated_data.pop('art'))
        art_post, created = ArtPost.objects.update_or_create(user=user, art=art)
        return art_post


class ArtRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtUser
        fields = (
            'get_following',
            'get_followers',
            'get_friends',
            'get_blocking',
            'get_blocked',
        )

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        user_followers = [i for i in instance.get_followers()]
        user_following = [i for i in instance.get_following()]
        user_friends = [i for i in instance.get_friends()]
        user_blocking = [i for i in instance.get_blocking()]
        user_blocked = [i for i in instance.get_blocked()]
        representation_data = super().to_representation(instance)
        representation_data['get_following'] = ArtUserSerializer(user_following, many=True).data
        representation_data['get_followers'] = ArtUserSerializer(user_followers, many=True).data
        representation_data['get_friends'] = ArtUserSerializer(user_friends, many=True).data
        representation_data['get_blocking'] = ArtUserSerializer(user_blocking, many=True).data
        representation_data['get_blocked'] = ArtUserSerializer(user_blocked, many=True).data
        return representation_data

    # def to_internal_value(self, data):
    #     pass
