# Generated by Django 4.1.7 on 2023-05-30 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jresto', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Sidedishes',
            new_name='Sidedish',
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='extension_name',
            field=models.CharField(default='', max_length=50, null=True),
        ),
    ]
