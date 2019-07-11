# Generated by Django 2.2.2 on 2019-07-11 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_voted_system_signature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatevote',
            name='candidate',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='election.Candidate'),
        ),
        migrations.AlterField(
            model_name='voted',
            name='elector',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='election.Elector'),
        ),
    ]
