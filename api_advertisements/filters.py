from django_filters import rest_framework as filters

from api_advertisements.models import Advertisement, Tag


class AdvertisementFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name='tag__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    date__from = filters.DateTimeFilter(field_name='created', lookup_expr='gt')
    date__to = filters.DateTimeFilter(field_name='created', lookup_expr='lt')
    price__min = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__max = filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        fields = ('tag', 'created', 'price',)
        model = Advertisement
