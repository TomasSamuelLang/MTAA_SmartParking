# Generated by Django 2.1.7 on 2019-04-20 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartParkingServer', '0014_auto_20190421_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.CharField(max_length=9999),
        ),
    ]