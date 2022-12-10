from django.contrib import admin

from .models import Cards, Pay


class CardsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'card_series',
        'number_card',
        'status',
        'date_card_start',
        'date_card_end',
    )


class PayAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'card',
        'amount',
        'pub_date',
    )
    list_filter = ('card',)


admin.site.register(Pay, PayAdmin)
admin.site.register(Cards, CardsAdmin)
