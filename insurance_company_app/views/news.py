from django.shortcuts import render
from ..services import random_joke, cat_fact


def news_view(request):
    funny_joke = random_joke.RandomJokeService.get_random_joke()
    cat_facts = cat_fact.CatFactService.get_random_fact()
    return render(request, 'insurance/news.html', {'joke': funny_joke, 'cat_facts': cat_facts})
