from django.urls import path  
from .views import *  

urlpatterns = [  
    path('webhook/', TelegramBotView.as_view(), name='telegram_webhook'),  # Set the path for your webhook  
]