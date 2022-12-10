import django_filters

from .models import Cards


class CardsFilter(django_filters.FilterSet):
    date_card_start = django_filters.DateFromToRangeFilter()
    date_card_end = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Cards
        fields = [
            'card_series',
            'number_card',
            'date_card_start',
            'date_card_end',
            'status'
        ]
