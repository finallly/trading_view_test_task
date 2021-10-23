from django.urls import path
from rest_framework.authtoken import views

from .views import TransactionCreateView, TransactionCancelView, TransactionConfirmView

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
    )
]
