# Generated by Django 2.0 on 2020-12-30 16:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('voting', '0003_auto_20180605_0842'),
    ]

    operations = [
        migrations.CreateModel(
            name='Census',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adscripcion', models.CharField(blank=True, max_length=20, null=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('voter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('voting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voting.Voting')),
            ],
        ),
        migrations.CreateModel(
            name='CensusGroupByVoter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CensusGroupByVoting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voting', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='voting.Voting')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='censusgroupbyvoting',
            unique_together={('voting',)},
        ),
        migrations.AlterUniqueTogether(
            name='censusgroupbyvoter',
            unique_together={('voter',)},
        ),
        migrations.AlterUniqueTogether(
            name='census',
            unique_together={('voting', 'voter')},
        ),
    ]
