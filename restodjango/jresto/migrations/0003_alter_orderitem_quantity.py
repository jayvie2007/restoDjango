# Generated by Django 4.1.7 on 2023-08-30 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jresto', '0002_order_alter_customerfeedback_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]