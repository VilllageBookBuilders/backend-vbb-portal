# Generated by Django 3.0.10 on 2021-04-12 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20210412_0909'),
        ('program', '0012_auto_20210412_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headmastersprogramassociation',
            name='headmaster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='program_headmaster', to='users.Headmaster'),
        ),
        migrations.AlterField(
            model_name='program',
            name='headmasters',
            field=models.ManyToManyField(through='program.HeadmastersProgramAssociation', to='users.Headmaster'),
        ),
    ]
