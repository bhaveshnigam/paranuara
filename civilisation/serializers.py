from rest_framework import serializers

from civilisation.models import Citizen, CitizenTag, FoodItem


class CitizenMinimalSerializer(serializers.ModelSerializer):
    """Serializer with essential information about a citizen """

    class Meta:
        model = Citizen
        fields = ('name', 'has_died', 'picture', 'age', 'gender', 'email', 'phone', 'address', 'about')


class CitizenSerializer(serializers.ModelSerializer):
    """Serializer to provide all information about the """
    company_name = serializers.CharField(source='company.name')
    tags = serializers.SerializerMethodField()
    favourite_food = serializers.SerializerMethodField()
    gender = serializers.CharField(source='get_gender_display')

    class Meta:
        model = Citizen
        fields = ('name', 'has_died', 'balance', 'picture', 'age', 'eye_color', 'gender',
                  'company_name', 'email', 'phone', 'address', 'about', 'registered', 'tags', 'greeting',
                  'favourite_food')

    def get_tags(self, obj):
        return obj.tags.values_list('name', flat=True)

    def get_favourite_food(self, obj):
        return obj.favourite_food.values_list('name', flat=True)


class CitizenCrucialInformationSerializer(serializers.ModelSerializer):
    """Serializer to provide crucial information about the citizen"""

    class Meta:
        model = Citizen
        fields = ('name', 'age', 'address', 'phone')


class CitizenFavouriteFoodOverviewSerializer(serializers.ModelSerializer):
    """Serializer to provide favourite food overview for a citizen."""
    username = serializers.CharField(source='name')
    fruits = serializers.SerializerMethodField()
    vegetables = serializers.SerializerMethodField()

    class Meta:
        model = Citizen
        fields = ('username', 'age', 'fruits', 'vegetables')

    def get_fruits(self, obj):
        return obj.favourite_food.filter(food_type=FoodItem.FOOD_TYPE_FRUIT).values_list('name', flat=True)

    def get_vegetables(self, obj):
        return obj.favourite_food.filter(food_type=FoodItem.FOOD_TYPE_VEGETABLE).values_list('name', flat=True)
