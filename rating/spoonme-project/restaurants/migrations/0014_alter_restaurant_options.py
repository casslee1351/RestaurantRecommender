# Generated by Django 4.1 on 2022-09-06 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0013_rename_type_restaurant_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='restaurant',
            options={'ordering': ('name',)},
        ),
    ]
