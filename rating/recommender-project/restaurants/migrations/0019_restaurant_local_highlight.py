# Generated by Django 4.1 on 2022-09-23 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0018_lunchbuddies'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='local_highlight',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
