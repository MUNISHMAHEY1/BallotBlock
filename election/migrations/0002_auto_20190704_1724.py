# Generated by Django 2.2.2 on 2019-07-04 17:24

import datetime
from django.db import migrations, models
import election.models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electionconfig',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 4, 17, 24, 42, 778734), validators=[election.models.present_or_future_date_endtime]),
        ),
        migrations.AlterField(
            model_name='electionconfig',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 4, 17, 24, 42, 778704), validators=[election.models.present_or_future_date_starttime]),
        ),
    ]
