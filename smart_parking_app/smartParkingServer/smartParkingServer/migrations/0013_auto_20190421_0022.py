# Generated by Django 2.1.7 on 2019-04-20 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartParkingServer', '0012_auto_20190420_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(max_length=999, null=True, upload_to='media/'),
        ),
    ]
