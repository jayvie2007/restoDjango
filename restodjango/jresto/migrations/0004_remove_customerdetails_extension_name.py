# Generated by Django 4.1.7 on 2023-08-01 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jresto', '0003_customerdetails_save_password_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerdetails',
            name='extension_name',
        ),
    ]
