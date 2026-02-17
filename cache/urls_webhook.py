from django.urls import path
from .views import WebhookNewsUpdate

urlpatterns = [
    path('news/', WebhookNewsUpdate.as_view(), name='webhook-news'),
]