# Generated by Django 4.1.7 on 2023-05-04 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_clinic_workhour_a_alter_clinic_workhour_b'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='slot',
            field=models.CharField(max_length=10),
        ),
    ]