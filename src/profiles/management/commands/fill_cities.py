import json
import os

from django.core.management.base import BaseCommand
from src.profiles.models import City


def load_from_json(file_name, JSON_PATH='src/profiles/jsons'):
    with open(os.path.join(JSON_PATH, file_name + '.json'), mode='r', encoding='UTF-8') as infile:

        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        cities = load_from_json('cities')
        for city in cities:
            new_city = City()
            new_city.city_name = cities[city]
            new_city.save()

