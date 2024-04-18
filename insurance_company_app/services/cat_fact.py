import requests


class CatFactService:
    @staticmethod
    def get_random_fact():
        return requests.get('https://catfact.ninja/fact').json()