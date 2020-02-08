import datetime
import json
import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from civilisation import models as civilisation_models


class Command(BaseCommand):
    help = 'Load civilisation data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep_old_data',
            action='store_true',
            help='Keep up old imported data',
        )

    def read_json_file(self, file_path):
        with open(file_path) as json_file:
            return json.load(json_file)

    def load_company_data(self):
        company_json_file = os.path.join(settings.BASE_DIR, 'resources', 'companies.json')
        company_json_data = self.read_json_file(company_json_file)
        for company_data in company_json_data:
            civilisation_models.Company.objects.create(
                name=company_data["company"],
                company_index=company_data["index"] + 1  # Since companies are provided as zero index array
            )

    def load_people_data(self):
        people_json_data = self.read_json_file(
            os.path.join(settings.BASE_DIR, 'resources', 'people.json')
        )
        vegetables = self.read_json_file(
            os.path.join(settings.BASE_DIR, 'resources', 'third_party', 'vegetables.json')
        )["vegetables"]
        fruits = self.read_json_file(
            os.path.join(settings.BASE_DIR, 'resources', 'third_party', 'fruits.json')
        )["fruits"]
        for individual in people_json_data:
            company = civilisation_models.Company.objects.filter(
                company_index=individual['company_id'],
            ).first()
            registered_timestamp = datetime.datetime.strptime(
                individual['registered'], "%Y-%m-%dT%H:%M:%S %z"
            )
            csv_friends = ','.join([str(friend['index']) for friend in individual['friends']])

            citizen = civilisation_models.Citizen.objects.create(
                _id=individual["_id"],
                index=individual["index"],
                guid=individual["guid"],
                has_died=individual["has_died"],
                balance=individual['balance'],
                picture=individual["picture"],
                age=individual["age"],
                eye_color=individual["eyeColor"],
                name=individual["name"],
                gender=(
                    civilisation_models.Citizen.GENDER_MALE
                    if individual["gender"] == 'male' else civilisation_models.Citizen.GENDER_FEMALE
                ),
                company=company,
                email=individual["email"],
                phone=individual["phone"],
                address=individual["address"],
                about=individual["about"],
                registered=registered_timestamp,
                greeting=individual["greeting"],
                friends_csv=csv_friends
            )
            for tag in individual['tags']:
                tag_object, created = civilisation_models.CitizenTag.objects.get_or_create(
                    name=tag
                )
                citizen.tags.add(tag_object)
            for food_item in individual['favouriteFood']:
                if food_item in vegetables:
                    food_type = civilisation_models.FoodItem.FOOD_TYPE_VEGETABLE
                elif food_item in fruits:
                    food_type = civilisation_models.FoodItem.FOOD_TYPE_FRUIT
                else:
                    self.stdout.write(
                        self.style.NOTICE('Unable to classify either as fruit or vegetable: %s' % food_item)
                    )
                    food_type = ''

                food_item_object, created = civilisation_models.FoodItem.objects.get_or_create(
                    name=food_item,
                    food_type=food_type
                )
                citizen.favourite_food.add(food_item_object)

    def handle(self, *args, **options):
        if not options.get('keep_old_data', False):
            self.stdout.write(self.style.NOTICE('Proceeding to clean all of the old data'))
            call_command('clear_data')

        self.stdout.write(self.style.NOTICE('Proceeding to import company data'))
        self.load_company_data()
        self.stdout.write(self.style.NOTICE('Proceeding to import people data'))
        self.load_people_data()
        self.stdout.write(self.style.SUCCESS('Data imported'))
