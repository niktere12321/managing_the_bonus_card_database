from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'cards'


urlpatterns = [
    path('get-result/<int:pk>/', login_required(views.GetResult.as_view()), name='get_informathion'),
    path('edit-card/<int:pk>/', login_required(views.EditCard.as_view()), name='edit_card'),
    path('create/', login_required(views.CreateCard.as_view()), name='create_card'),
    path('delete/<int:pk>/', login_required(views.DeleteCard.as_view()), name='delete_card'),
    path('create-pay/<int:pk>/', login_required(views.CreatePay.as_view()), name='create_pay'),
    path('', login_required(views.Index.as_view()), name='index'),
]
