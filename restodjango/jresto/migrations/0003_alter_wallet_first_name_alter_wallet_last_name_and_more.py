# Generated by Django 4.1.7 on 2023-05-30 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jresto', '0002_rename_sidedishes_sidedish_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='first_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='last_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='middle_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]