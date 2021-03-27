# Generated by Django 3.0.10 on 2021-03-20 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210320_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newslettersubscriber',
            name='subscriber_type',
            field=models.CharField(choices=[(100, 'STUDENT'), (200, 'MENTOR'), (300, 'TEACHER'), (400, 'DIRECTOR'), (500, 'ADVISOR'), (600, 'HEADMASTER')], default=20, max_length=254),
        ),
    ]
