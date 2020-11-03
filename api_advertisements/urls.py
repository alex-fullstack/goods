from rest_framework.routers import DefaultRouter

from api_advertisements.views import AdvertisementViewSet, TagViewSet, PhotoViewSet, AdvertisementShortViewSet

router = DefaultRouter()
router.register('advertisements', AdvertisementViewSet)
router.register(r'advertisements/short', AdvertisementShortViewSet, basename='short')
router.register('photos', PhotoViewSet)
router.register('tags', TagViewSet)
