# Generated by Django 4.1.4 on 2022-12-27 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_rename_dependees_dependants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='roomType',
            field=models.CharField(choices=[('King', 'King'), ('Luxury', 'Luxury'), ('Normal', 'Normal'), ('Economy', 'Economy')], max_length=20),
        ),
    ]