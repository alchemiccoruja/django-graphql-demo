# Generated by Django 3.1.2 on 2020-10-20 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(default='Fahrenheit', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('value', models.FloatField(max_length=50)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='temperature.temperature')),
            ],
        ),
    ]
