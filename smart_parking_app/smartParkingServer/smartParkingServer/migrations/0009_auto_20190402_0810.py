# Generated by Django 2.1.7 on 2019-04-02 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartParkingServer', '0008_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favourite_parking_lot',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartParkingServer.User'),
        ),
    ]
