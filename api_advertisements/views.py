from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from api_advertisements.filters import AdvertisementFilter
from api_advertisements.models import Advertisement, Tag, Photo
from api_advertisements.serializers import (
    AdvertisementSerializer, TagSerializer, PhotoSerializer, AdvertisementShortSerializer)


class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertisementFilter

    def perform_create(self, serializer):
        tag = Tag.objects.filter(slug__in=self.request.data.getlist('tag'))
        photo = get_object_or_404(Photo, pk=self.request.data.get('photo'))
        serializer.save(tag=tag, photo=photo, view_counter=0)

    def perform_update(self, serializer):
        kwargs = {}
        tag = self.request.data.getlist('tag')
        if tag:
            kwargs['tag'] = Tag.objects.filter(slug__in=tag)
        photo = self.request.data.get('photo')
        if photo:
            kwargs['photo'] = get_object_or_404(Photo, pk=photo)

        serializer.save(**kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_counter()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AdvertisementShortViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = AdvertisementShortSerializer

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Advertisement, pk=self.kwargs.get('pk'))


class TagViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class PhotoViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    pagination_class = PageNumberPagination
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.save(image=self.request.data.get('image'))
