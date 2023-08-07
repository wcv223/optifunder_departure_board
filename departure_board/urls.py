from django.urls import path

from .views import board, api_predictions

urlpatterns = [
    path('', board, name='board'),
    path('api/predictions/', api_predictions, name='api_predictions'),
]
