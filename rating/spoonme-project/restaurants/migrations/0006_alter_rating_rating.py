# Generated by Django 4.0.1 on 2022-03-25 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_alter_rating_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
    ]
