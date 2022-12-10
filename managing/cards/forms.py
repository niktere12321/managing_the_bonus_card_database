from django import forms
from django.contrib.auth import get_user_model

from .models import Cards, Pay

User = get_user_model()


class CardsForm(forms.ModelForm):
    duration = forms.ChoiceField(choices=Cards.DURATION)
    quantity = forms.IntegerField(label='Количество', min_value=1)

    class Meta:
        model = Cards
        fields = ('card_series', )

    def clean(self):
        data = self.cleaned_data
        if len(data.get('card_series')) != 9:
            raise forms.ValidationError('Код банка должен быть девятизначный')
        return data


class PayForm(forms.ModelForm):

    class Meta:
        model = Pay
        exclude = ('card',)
