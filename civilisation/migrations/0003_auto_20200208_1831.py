# Generated by Django 3.0.3 on 2020-02-08 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('civilisation', '0002_auto_20200208_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='food_type',
            field=models.CharField(blank=True, choices=[('fruit', 'Fruit'), ('vegetable', 'Vegetable')], default='fruit', max_length=15),
        ),
    ]
