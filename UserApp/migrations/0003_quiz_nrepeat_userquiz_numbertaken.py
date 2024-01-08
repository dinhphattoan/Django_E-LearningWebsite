# Generated by Django 5.0 on 2024-01-04 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0002_alter_quiz_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='nrepeat',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='userquiz',
            name='numbertaken',
            field=models.IntegerField(default=0),
        ),
    ]