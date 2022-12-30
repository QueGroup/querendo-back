import json
import os

from django.core.management.base import BaseCommand
from src.profiles.models import Gender


def load_from_json(file_name, JSON_PATH='src/profiles/jsons'):
    with open(os.path.join(JSON_PATH, file_name + '.json'), mode='r', encoding='UTF-8') as infile:

        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        genders = load_from_json('genders')
        for gender in genders:
            new_gender = Gender()
            new_gender.sex = genders[gender]
            new_gender.save()

