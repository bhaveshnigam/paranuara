from django.core.validators import validate_comma_separated_integer_list
from django.db import models


class Company(models.Model):
    """Model to store each company of the paranuara civilisation."""
    company_index = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)


class CitizenTag(models.Model):
    """Model to store citizen tags."""
    name = models.CharField(max_length=25)


class FoodItem(models.Model):
    """Model to store food items"""
    FOOD_TYPE_FRUIT = 'fruit'
    FOOD_TYPE_VEGETABLE = 'vegetable'
    FOOD_TYPE_CHOICES = (
        (FOOD_TYPE_FRUIT, 'Fruit'),
        (FOOD_TYPE_VEGETABLE, 'Vegetable'),
    )
    name = models.CharField(max_length=25)
    food_type = models.CharField(
        default=FOOD_TYPE_FRUIT, choices=FOOD_TYPE_CHOICES, max_length=15, blank=True
    )


class Citizen(models.Model):
    """Model to store each citizen of paranuara civilisation."""
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
    )
    _id = models.CharField(max_length=25, unique=True)
    index = models.IntegerField()
    guid = models.UUIDField(unique=True)
    has_died = models.BooleanField(default=False)
    balance = models.CharField(max_length=25)
    picture = models.URLField()
    age = models.IntegerField()
    eye_color = models.CharField(max_length=25)
    name = models.CharField(max_length=25)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=25)
    address = models.CharField(max_length=100)
    about = models.TextField()
    registered = models.DateTimeField()
    tags = models.ManyToManyField(CitizenTag)
    friends_csv = models.CharField(max_length=100, validators=[validate_comma_separated_integer_list])
    greeting = models.TextField()
    favourite_food = models.ManyToManyField(FoodItem)

    def get_friends(self):
        return Citizen.objects.filter(index__in=self.friends_csv.split(','))
