# Generated by Django 4.1.7 on 2023-09-01 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jresto', '0004_order_total_bill'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('barangay', models.CharField(max_length=100)),
                ('zip_code', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('contact_number', models.IntegerField()),
            ],
        ),
    ]
