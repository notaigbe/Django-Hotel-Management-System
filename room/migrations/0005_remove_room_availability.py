# Generated by Django 4.1.4 on 2022-12-27 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0004_room_availability'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='availability',
        ),
    ]