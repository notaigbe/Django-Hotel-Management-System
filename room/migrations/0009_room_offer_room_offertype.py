# Generated by Django 4.1.4 on 2022-12-29 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0008_remove_room_statusduration'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='offer',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='offerType',
            field=models.CharField(choices=[('order-1', 'ORDER 1'), ('order-2', 'ORDER 2')], default='order-1', max_length=20),
        ),
    ]