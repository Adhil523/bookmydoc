# Generated by Django 4.1.7 on 2023-05-04 10:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='d',
            field=models.DateField(default=datetime.datetime(2018, 5, 3, 0, 0)),
        ),
    ]