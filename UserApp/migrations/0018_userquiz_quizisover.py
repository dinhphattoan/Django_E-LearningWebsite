# Generated by Django 5.0 on 2024-01-09 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0017_remove_tmp_userquizquestionanswer_listquestionanswer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquiz',
            name='quizisover',
            field=models.BooleanField(default=False),
        ),
    ]
