from django.urls import path
from rest_framework.authtoken import views

from .views import TransactionCreateView, TransactionCancelView, TransactionConfirmView, CreateAccountView, TopUserView

tag = 'transaction'

urlpatterns = [
    path(
        'auth/', views.obtain_auth_token,
    ),
    path(
        f'{tag}/create/', TransactionCreateView.as_view()
    ),
    path(
        f'{tag}/cancel/', TransactionCancelView.as_view()
    ),
    path(
        f'{tag}/confirm/', TransactionConfirmView.as_view()
    ),
    path(
        f'account/create/', CreateAccountView.as_view()
    ),
    path(
        f'account/top/', TopUserView.as_view()
    )
]
