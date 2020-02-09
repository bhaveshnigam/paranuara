import logging
import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from civilisation import models as civilisation_models

TEST_BASE_DIR = os.path.join(settings.BASE_DIR, 'civilisation', 'test_resources')

TEST_RESOURCE_FILES = {
    'company_data': os.path.join(TEST_BASE_DIR, 'companies.json'),
    'people_data': os.path.join(TEST_BASE_DIR, 'people.json'),
    'fruit_data': os.path.join(TEST_BASE_DIR, 'third_party', 'fruits.json'),
    'vegetable_data': os.path.join(TEST_BASE_DIR, 'third_party', 'vegetables.json'),
}


class CivilisationTestCase(TestCase):
    @override_settings(RESOURCE_FILES=TEST_RESOURCE_FILES)
    @override_settings(TEST_MODE=True)
    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)
        call_command('load_data')
        self.client = Client()
        self.company_1 = civilisation_models.Company.objects.get(
            company_index=1
        )
        self.company_4 = civilisation_models.Company.objects.get(
            company_index=4
        )

    def test_get_company_employee(self):
        response = self.client.get(
            reverse('civilisation:company-employees',
                    args=[self.company_1.company_index])
        )
        expected_json = {
            'count': 3,
            'next': None,
            'previous': None,
            'results': [
                {
                    'name': 'Carmella Lambert',
                    'has_died': True, 'balance': '$2,418.59',
                    'picture': 'http://placehold.it/32x32',
                    'age': 61,
                    'eye_color': 'blue',
                    'gender': 'Female',
                    'company_name': 'NETBOOK',
                    'email': 'carmellalambert@earthmark.com',
                    'phone': '+1 (910) 567-3630',
                    'address': '628 Sumner Place, Sperryville, American Samoa, 9819',
                    'about': 'Non duis dolore ad enim. Est id reprehenderit cupidatat tempor excepteur. Cupidatat labore incididunt nostrud exercitation ullamco reprehenderit dolor eiusmod sit exercitation est. Voluptate consectetur est fugiat magna do laborum sit officia aliqua magna sunt. Culpa labore dolore reprehenderit sunt qui tempor minim sint tempor in ex. Ipsum aliquip ex cillum voluptate culpa qui ullamco exercitation tempor do do non ea sit. Occaecat laboris id occaecat incididunt non cupidatat sit et aliquip.\r\n',
                    'registered': '2016-07-13T22:29:07Z',
                    'tags': ['id', 'quis', 'ullamco', 'consequat', 'laborum', 'sint', 'velit'],
                    'greeting': 'Hello, Carmella Lambert! You have 6 unread messages.',
                    'favourite_food': ['orange', 'apple', 'banana', 'strawberry'],
                    '_id': '595eeb9b96d80a5bc7afb106',
                    'guid': '5e71dc5d-61c0-4f3b-8b92-d77310c7fa43', 'index': 0
                },
                {
                    'name': 'Bonnie Bass',
                    'has_died': False,
                    'balance': '$2,119.44',
                    'picture': 'http://placehold.it/32x32',
                    'age': 54,
                    'eye_color': 'blue',
                    'gender': 'Female',
                    'company_name': 'NETBOOK',
                    'email': 'bonniebass@earthmark.com',
                    'phone': '+1 (823) 428-3710',
                    'address': '455 Dictum Court, Nadine, Mississippi, 6499',
                    'about': 'Non voluptate reprehenderit ad elit veniam nulla ut ea ex. Excepteur exercitation aliquip Lorem nisi duis. Ex cillum commodo labore sint non velit aliquip cupidatat sint. Consequat est sint do in eiusmod minim exercitation do consectetur incididunt culpa deserunt. Labore veniam elit duis minim magna et laboris sit labore eu velit cupidatat cillum cillum.\r\n',
                    'registered': '2017-06-08T14:23:18Z',
                    'tags': ['quis', 'sunt', 'sit', 'aliquip', 'pariatur', 'nulla'],
                    'greeting': 'Hello, Bonnie Bass! You have 10 unread messages.',
                    'favourite_food': ['orange', 'banana', 'strawberry', 'beetroot'],
                    '_id': '595eeb9bb3821d9982ea44f9',
                    'guid': '49c04b8d-0a96-4319-b310-d6aa8269adca',
                    'index': 2
                },
                {
                    'name': 'Kathleen Clarke',
                    'has_died': True,
                    'balance': '$2,047.08',
                    'picture': 'http://placehold.it/32x32',
                    'age': 30,
                    'eye_color': 'blue',
                    'gender': 'Female',
                    'company_name': 'NETBOOK',
                    'email': 'kathleenclarke@earthmark.com',
                    'phone': '+1 (888) 523-3982',
                    'address': '195 Ovington Avenue, Bonanza, Indiana, 7131',
                    'about': 'Fugiat incididunt sunt enim commodo laboris ullamco Lorem nulla cupidatat anim id cupidatat. Ut voluptate Lorem occaecat cillum cupidatat officia sit aute ex mollit cupidatat. Et nostrud irure irure minim aliqua magna minim nulla nisi est aliquip duis consequat. Proident nostrud sint reprehenderit voluptate eu enim consequat ipsum est qui eiusmod laboris ipsum adipisicing. Ullamco minim aute sint aute ullamco reprehenderit ea ipsum pariatur nostrud.\r\n',
                    'registered': '2015-11-02T16:32:37Z',
                    'tags': ['consequat', 'mollit', 'deserunt', 'dolore', 'nostrud', 'labore', 'est'],
                    'greeting': 'Hello, Kathleen Clarke! You have 4 unread messages.',
                    'favourite_food': ['apple', 'banana', 'strawberry', 'cucumber'],
                    '_id': '595eeb9b7986ff9babbdf28e',
                    'guid': 'e3adc59a-fc86-4c40-971c-fb0250577642',
                    'index': 10
                }
            ]
        }
        self.assertDictEqual(response.json(), expected_json)

    def test_get_company_with_zero_employees(self):
        response = self.client.get(
            reverse('civilisation:company-employees',
                    args=[self.company_4.company_index])
        )
        expected_json = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        }
        self.assertDictEqual(response.json(), expected_json)

    def test_citizen_mutual_friends(self):
        person_1 = civilisation_models.Citizen.objects.get(index=1)
        person_2 = civilisation_models.Citizen.objects.get(index=2)
        response = self.client.get(
            reverse('civilisation:citizen-mutual-friends',
                    args=[person_1._id, person_2._id])
        )
        expected_json = {
            'mutual_friends': [
                {'about': 'Consectetur aute consectetur dolor '
                          'aliquip dolor sit id. Sint consequat '
                          'anim occaecat ad mollit aliquip ut '
                          'aute eu culpa mollit qui proident eu. '
                          'Consectetur ea et sit exercitation '
                          'aliquip officia ea aute exercitation '
                          'nulla qui sunt labore. Enim veniam '
                          'labore do irure laborum aute '
                          'exercitation consectetur. Voluptate '
                          'adipisicing velit sunt consectetur id '
                          'sint adipisicing elit elit pariatur '
                          'officia amet officia et.\r\n',
                 'address': '492 Stockton Street, Lawrence, Guam, '
                            '4854',
                 'age': 60,
                 'email': 'deckermckenzie@earthmark.com',
                 'gender': 'male',
                 'has_died': False,
                 'name': 'Decker Mckenzie',
                 'phone': '+1 (893) 587-3311',
                 'picture': 'http://placehold.it/32x32'}],
            'person_1': {
                'address': '492 Stockton Street, Lawrence, Guam, 4854',
                'age': 60,
                'name': 'Decker Mckenzie',
                'phone': '+1 (893) 587-3311'},
            'person_2': {
                'address': '455 Dictum Court, Nadine, Mississippi, 6499',
                'age': 54,
                'name': 'Bonnie Bass',
                'phone': '+1 (823) 428-3710'}
        }
        self.assertDictEqual(response.json(), expected_json)

    def test_citizen_mutual_friends_when_person_dont_exist(self):
        response = self.client.get(
            reverse('civilisation:citizen-mutual-friends',
                    args=['random1', 'random2'])
        )
        expected_json = {
            'mutual_friends': [],
            'person_1': {},
            'person_2': {},
        }
        self.assertDictEqual(response.json(), expected_json)

    def test_citizen_favourite_food(self):
        person_3 = civilisation_models.Citizen.objects.get(index=3)
        response = self.client.get(
            reverse('civilisation:citizen-favourite-food',
                    args=[person_3._id])
        )
        expected_json = {
            'age': 30,
            'fruits': ['orange', 'apple'],
            'username': 'Rosemary Hayes',
            'vegetables': ['carrot', 'celery']
        }
        self.assertDictEqual(response.json(), expected_json)

    def test_citizen_favourite_food_when_citizen_doesnt_exist(self):
        response = self.client.get(
            reverse('civilisation:citizen-favourite-food',
                    args=['radndad1'])
        )
        expected_json = {
            'detail': 'Not found.'
        }
        self.assertDictEqual(response.json(), expected_json)
