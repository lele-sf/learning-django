# Generated by Django 5.0.1 on 2024-03-24 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='prepation_time',
            new_name='preparation_time',
        ),
    ]
