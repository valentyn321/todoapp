# Generated by Django 3.0.2 on 2020-01-16 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='number_of_todos',
        ),
    ]
