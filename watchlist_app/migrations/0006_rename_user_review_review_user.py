# Generated by Django 4.1.2 on 2022-11-17 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0005_review_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='user',
            new_name='review_user',
        ),
    ]