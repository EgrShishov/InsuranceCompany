from django.shortcuts import render, get_object_or_404
from ..services import random_joke, cat_fact
from ..models.news import News


def home(request):
    news = News.objects.all().order_by('publish_date').first()
    funny_joke = random_joke.RandomJokeService.get_random_joke()
    cat_facts = cat_fact.CatFactService.get_random_fact()
    context = {
        'news': news,
        'joke': funny_joke,
        'cat_facts': cat_facts
    }
    return render(request, 'insurance/home.html', context)


def index(request):
    news = News.objects.all()
    funny_joke = random_joke.RandomJokeService.get_random_joke()
    cat_facts = cat_fact.CatFactService.get_random_fact()
    context = {
        'news': news,
        'joke': funny_joke,
        'cat_facts': cat_facts
    }
    return render(request, 'insurance/news.html', context)


def details(request, id):
    news = get_object_or_404(News, id=id)
    context = {
        'details': news
    }
    return render(request, 'insurance/news_details.html', context)
