# Generated by Django 4.2.10 on 2024-05-05 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0013_remove_education_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='end_date',
            field=models.DateField(max_length=7),
        ),
        migrations.AlterField(
            model_name='education',
            name='start_date',
            field=models.DateField(max_length=7),
        ),
    ]
