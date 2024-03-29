# Generated by Django 2.2.6 on 2019-10-24 20:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('insert_tsd', models.DateTimeField(default=datetime.datetime(2019, 10, 24, 20, 49, 42, 113220, tzinfo=utc))),
                ('origin', models.CharField(choices=[('bbc', 'BBC')], max_length=50)),
                ('bp1', models.TextField()),
                ('bp2', models.TextField()),
                ('bp3', models.TextField()),
                ('bp4', models.TextField()),
                ('bp5', models.TextField()),
            ],
        ),
    ]
