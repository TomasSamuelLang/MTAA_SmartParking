# Generated by Django 2.1.7 on 2019-04-03 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartParkingServer', '0009_auto_20190402_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.CharField(max_length=300),
        ),
    ]
