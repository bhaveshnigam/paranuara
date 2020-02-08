from django.core.management.base import BaseCommand, CommandError
from civilisation import models as civilisation_models


class Command(BaseCommand):
    help = 'Clean up all the data from the system.'

    def handle(self, *args, **options):
        civilisation_models.Company.objects.all().delete()
        civilisation_models.Citizen.objects.all().delete()
        civilisation_models.CitizenTag.objects.all().delete()
        civilisation_models.FoodItem.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data from the system'))
