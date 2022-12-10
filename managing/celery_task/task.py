from cards.models import Cards
from managing.celery import app


@app.task
def change_status_card(pk):
    """Изменение статуса"""
    card = Cards.objects.get(id=pk)
    card.status = Cards.OVERDUE
    card.save()