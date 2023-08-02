# Generated by Django 4.1.7 on 2023-08-01 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jresto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customadmin',
            name='uid',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='uid',
            field=models.CharField(editable=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='drink',
            name='product_id',
            field=models.CharField(default='drink__d7ca22b8', max_length=16),
        ),
        migrations.AlterField(
            model_name='food',
            name='product_id',
            field=models.CharField(default='food__fd066168', max_length=16),
        ),
        migrations.AlterField(
            model_name='side',
            name='product_id',
            field=models.CharField(default='side__1562489e', max_length=16),
        ),
    ]