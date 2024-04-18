from django.urls import path, include
from .views import news

urlpatterns = [
    path('', news.news_view , name='main_page')
]
