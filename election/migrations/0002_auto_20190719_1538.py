# Generated by Django 2.2.2 on 2019-07-19 15:38

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electionconfig',
            name='block_time_generation',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='electionconfig',
            name='guess_rate',
            field=models.DecimalField(decimal_places=4, default=Decimal('0.4'), max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.0001')), django.core.validators.MaxValueValidator(Decimal('0.9999'))]),
        ),
        migrations.AlterField(
            model_name='electionconfig',
            name='min_votes_in_block',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='electionconfig',
            name='min_votes_in_last_block',
            field=models.IntegerField(default=5),
        ),
    ]