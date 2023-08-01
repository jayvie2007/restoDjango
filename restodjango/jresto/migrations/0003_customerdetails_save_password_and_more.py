# Generated by Django 4.1.7 on 2023-08-01 03:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jresto', '0002_customerfeedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerdetails',
            name='save_password',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='customerfeedback',
            name='date_created',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
