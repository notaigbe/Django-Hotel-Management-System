# Generated by Django 4.1.4 on 2022-12-26 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Dependees',
            new_name='Dependants',
        ),
    ]