from rest_framework import serializers

from api_advertisements.models import Tag, Advertisement, Photo


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Tag


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Photo


class AdvertisementSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    photo = PhotoSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Advertisement
        extra_kwargs = {'view_counter': {'required': False}}


class AdvertisementShortSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'description', 'created', 'price',)
        model = Advertisement
