# Generated by Django 2.0 on 2021-01-06 10:58

from django.db import migrations, models
import voting.models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_auto_20201228_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='voting',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, validators=[voting.models.validate_start_date]),
        ),
    ]
