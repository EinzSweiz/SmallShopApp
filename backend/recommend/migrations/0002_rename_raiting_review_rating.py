# Generated by Django 5.1.2 on 2024-10-25 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='raiting',
            new_name='rating',
        ),
    ]
