# Generated by Django 5.0 on 2024-01-05 07:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0010_alter_userquiz_joindate_alter_userquiz_startdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquiz',
            name='joindate',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 5, 7, 29, 4, 959053, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='userquiz',
            name='startdate',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 5, 7, 29, 4, 959053, tzinfo=datetime.timezone.utc)),
        ),
    ]