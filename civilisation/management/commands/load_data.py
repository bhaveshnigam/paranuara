import datetime
import json

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

    def stdout_write(self, message, style):
        if not settings.TEST_MODE:
            self.stdout.write(style(message))

    def read_json_file(self, file_path):
        """Reads a JSON file from the provided file path file."""
        with open(file_path) as json_file:
            return json.load(json_file)

    def load_company_data(self):
        """Loads the company data from resources/companies.json file."""
        company_json_data = self.read_json_file(settings.RESOURCE_FILES['company_data'])
        for company_data in company_json_data:
            civilisation_models.Company.objects.create(
                name=company_data["company"],
                company_index=company_data["index"] + 1  # Since companies are provided as zero index array
            )

    def get_vegetable_data(self):
        """
            Get the classification data list for vegetables.
            Source: https://github.com/dariusk/corpora/blob/master/data/foods/vegetables.json
        """
        return self.read_json_file(settings.RESOURCE_FILES['vegetable_data'])["vegetables"]

    def get_fruits_data(self):
        """
            Get the classification data list for fruits.
            Source: https://github.com/dariusk/corpora/blob/master/data/foods/fruits.json
        """
        return self.read_json_file(settings.RESOURCE_FILES['fruit_data'])["fruits"]

    def load_people_data(self):
        """Loads the people data from resources/people.json file."""
        people_json_data = self.read_json_file(settings.RESOURCE_FILES['people_data'])
        vegetables = self.get_vegetable_data()
        fruits = self.get_fruits_data()
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
        """Execute command"""
        if not options.get('keep_old_data', False):
            self.stdout_write('Proceeding to clean all of the old data', self.style.WARNING)
            call_command('clear_data')

        self.stdout_write('Proceeding to import company data', self.style.WARNING)
        self.load_company_data()
        self.stdout_write('Proceeding to import people data', self.style.WARNING)
        self.load_people_data()
        self.stdout_write('Data imported', self.style.SUCCESS)
