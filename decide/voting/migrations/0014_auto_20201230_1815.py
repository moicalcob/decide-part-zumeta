# Generated by Django 2.0 on 2020-12-30 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0013_auto_20201230_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='candidates',
            field=models.ManyToManyField(blank=True, related_name='votings', to='voting.Candidate'),
        ),
    ]
