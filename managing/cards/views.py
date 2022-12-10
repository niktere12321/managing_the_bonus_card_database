from datetime import datetime

import pytz
from celery_task.task import change_status_card
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from .filters import CardsFilter
from .forms import CardsForm, PayForm
from .models import Cards, Pay

User = get_user_model()


class Index(FilterView):
    """Просмотр всех карт"""
    model = Cards
    paginate_by = 30
    filterset_class = CardsFilter
    template_name = 'cards/index.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class GetResult(generic.DetailView):
    """Просмотр информации карты"""
    model = Cards
    template_name = 'cards/get_informathion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.status != Cards.OVERDUE:
            context["card_open"] = True
        context["pays"] = Pay.objects.filter(card=self.object.pk)
        return context


class EditCard(UpdateView):
    model = Cards
    fields = ['status']
    template_name = 'cards/edit.html'

    def get_form(self, *args, **kwargs):
        form = super(EditCard, self).get_form(*args, **kwargs)
        form.fields['status'].choices = [
            (Cards.NOT_ACTIVATED, 'не активирована'),
            (Cards.ACTIVATED, 'активирована'),
        ]
        return form

    def get_success_url(self, **kwargs):
        if kwargs is not None:
            return reverse_lazy('cards:get_informathion', args=[self.object.pk])
        else:
            return reverse_lazy('cards:index')


class CreateCard(CreateView):
    model = Cards
    form_class = CardsForm
    template_name = 'cards/create.html'
    success_url = reverse_lazy('cards:index')

    def form_valid(self, form):
        form.instance.status = Cards.NOT_ACTIVATED
        form.instance.date_card_end = datetime.today() + relativedelta(months=int(self.request.POST.get('duration')))
        form.instance.user = self.request.user
        quantity = int(self.request.POST.get('quantity'))
        series_id = self.request.POST.get('card_series')
        self.object = self.generate_card_numbers(quantity, series_id, form)
        return super().form_valid(form)

    def generate_card_numbers(self, quantity, series_id, form):
        """Генерирует указанное количество уникальных номеров банковской карты"""
        last_number = Cards.objects.filter(card_series=series_id).first()
        last_number_card = 0
        if last_number is not None:
            last_number_card = int(last_number.number_card) + 1
        for i in range(quantity):
            str_number = str(last_number_card+i)
            form.instance.number_card = (16-len(str_number)) * '0' + str_number
            card_object = Cards.objects.create(
                number_card=form.instance.number_card,
                user=form.instance.user,
                status=form.instance.status,
                date_card_end=form.instance.date_card_end,
                card_series=form.instance.card_series,
            )
            moscow_tz = pytz.timezone(settings.TIME_ZONE)
            moscow_dt = moscow_tz.localize(card_object.date_card_end)
            change_status_datetime = moscow_dt.astimezone(pytz.UTC)
            change_status_card.apply_async(
                (card_object.pk, ),
                eta=change_status_datetime
            )
            if i+1 == quantity:
                return card_object


class CreatePay(CreateView):
    model = Pay
    form_class = PayForm
    template_name = 'cards/create.html'

    def form_valid(self, form):
        form.instance.card = get_object_or_404(Cards, pk=self.kwargs.get('pk'))
        return super(CreatePay, self).form_valid(form)

    def get_success_url(self, **kwargs):
        if kwargs is not None:
            return reverse_lazy('cards:get_informathion', args=[self.kwargs.get('pk')])
        else:
            return reverse_lazy('cards:index')


class DeleteCard(DeleteView):
    model = Cards
    template_name = 'cards/delete.html'
    success_url = reverse_lazy('cards:index')