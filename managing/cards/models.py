from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Cards(models.Model):
    DURATION = (
        (1, '1 месяц'),
        (6, '6 месяцев'),
        (12, '1 год'),
    )
    NOT_ACTIVATED = 'не активирована'
    ACTIVATED = 'активирована'
    OVERDUE = 'просрочена'
    CARD_STATUS = [
        (NOT_ACTIVATED, 'не активирована'),
        (ACTIVATED, 'активирована'),
        (OVERDUE, 'просрочена')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_series = models.CharField(max_length=9)
    number_card = models.CharField(max_length=16)
    status = models.CharField(
        max_length=20,
        choices=CARD_STATUS,
        default=NOT_ACTIVATED,
    )
    date_card_start = models.DateTimeField(auto_now=True)
    date_card_end = models.DateTimeField()

    class Meta:
        ordering = ('-date_card_start',)
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return self.number_card


class Pay(models.Model):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    amount = models.IntegerField()
    pub_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return str(self.amount)