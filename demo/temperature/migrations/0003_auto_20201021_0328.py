# Generated by Django 3.1.2 on 2020-10-21 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temperature', '0002_temperature_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentmeasurement',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='temperature',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='create date'),
        ),
    ]
