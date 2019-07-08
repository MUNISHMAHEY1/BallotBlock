# Generated by Django 2.2.2 on 2019-07-08 14:11

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectionConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='Generic Election', max_length=100)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('block_time_generation', models.IntegerField(default=15)),
                ('guess_rate', models.DecimalField(decimal_places=4, default=Decimal('0.3'), max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.0001')), django.core.validators.MaxValueValidator(Decimal('0.9999'))])),
                ('min_votes_in_block', models.IntegerField(default=50)),
                ('min_votes_in_last_block', models.IntegerField(default=50)),
                ('attendance_rate', models.DecimalField(decimal_places=2, default=Decimal('0.5'), max_digits=3, validators=[django.core.validators.MinValueValidator(Decimal('0.01')), django.core.validators.MaxValueValidator(Decimal('0.99'))])),
                ('locked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, unique=True)),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Elector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='election.Position')),
            ],
        ),
    ]
