# Generated by Django 3.2.4 on 2021-07-06 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mulima_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_born',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
