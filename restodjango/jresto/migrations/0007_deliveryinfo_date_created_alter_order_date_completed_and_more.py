# Generated by Django 4.1.7 on 2023-09-21 06:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jresto', '0006_alter_orderitem_date_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryinfo',
            name='date_created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='date_completed',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='date_completed',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
