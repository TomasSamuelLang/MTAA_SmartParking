# Generated by Django 2.1.7 on 2019-03-17 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartParkingServer', '0004_auto_20190317_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkin_lot',
            name='actualparkedcars',
            field=models.IntegerField(default=0),
        ),
    ]