# Generated by Django 2.1.7 on 2019-04-20 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartParkingServer', '0011_auto_20190420_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='image',
            field=models.ImageField(max_length=255, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.CharField(max_length=255),
        ),
    ]