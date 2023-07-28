# Generated by Django 4.1.7 on 2023-07-27 09:38

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('jresto', '0006_alter_customerdetails_date_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uid', models.CharField(default='', max_length=8)),
                ('middle_name', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='customuser_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customuser_set', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Side',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=8)),
                ('name', models.CharField(default='', max_length=25)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('price', models.IntegerField(default=0)),
                ('description', models.CharField(default='', max_length=100)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_updated', models.DateField(default='', editable=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Sidedish',
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='date_updated',
            field=models.DateField(default='', editable=False),
        ),
        migrations.AlterField(
            model_name='drink',
            name='date_updated',
            field=models.DateField(default='', editable=False),
        ),
        migrations.AlterField(
            model_name='drink',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='food',
            name='date_created',
            field=models.DateField(default=datetime.date.today, editable=False),
        ),
        migrations.AlterField(
            model_name='food',
            name='date_updated',
            field=models.DateField(default='', editable=False),
        ),
        migrations.AlterField(
            model_name='food',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]