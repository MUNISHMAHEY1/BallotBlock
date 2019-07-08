# Generated by Django 2.2.2 on 2019-07-08 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('election', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_val', models.CharField(default=None, max_length=200, null=True)),
                ('elector', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='election.Elector')),
            ],
        ),
        migrations.CreateModel(
            name='CandidateVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('candidate', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='election.Candidate')),
            ],
        ),
    ]
