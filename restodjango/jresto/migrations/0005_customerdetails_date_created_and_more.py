# Generated by Django 4.1.7 on 2023-05-30 05:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jresto', '0004_remove_wallet_first_name_remove_wallet_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerdetails',
            name='date_created',
            field=models.DateField(default=datetime.date(2023, 5, 30), editable=False),
        ),
        migrations.AddField(
            model_name='customerdetails',
            name='date_updated',
            field=models.DateField(default=datetime.date(2023, 5, 30)),
        ),
        migrations.AddField(
            model_name='drink',
            name='date_created',
            field=models.DateField(default=datetime.date(2023, 5, 30), editable=False),
        ),
        migrations.AddField(
            model_name='drink',
            name='date_updated',
            field=models.DateField(default=datetime.date(2023, 5, 30)),
        ),
        migrations.AddField(
            model_name='food',
            name='date_created',
            field=models.DateField(default=datetime.date(2023, 5, 30), editable=False),
        ),
        migrations.AddField(
            model_name='food',
            name='date_updated',
            field=models.DateField(default=datetime.date(2023, 5, 30)),
        ),
        migrations.AddField(
            model_name='sidedish',
            name='date_created',
            field=models.DateField(default=datetime.date(2023, 5, 30), editable=False),
        ),
        migrations.AddField(
            model_name='sidedish',
            name='date_updated',
            field=models.DateField(default=datetime.date(2023, 5, 30)),
        ),
        migrations.AlterField(
            model_name='food',
            name='name',
            field=models.CharField(max_length=25),
        ),
    ]
