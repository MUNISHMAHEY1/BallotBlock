# Generated by Django 2.2.2 on 2019-07-09 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voted',
            name='system_signature',
            field=models.TextField(blank=True, null=True),
        ),
    ]
