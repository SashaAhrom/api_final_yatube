# Generated by Django 2.2.16 on 2022-02-08 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20220208_0908'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_following',
        ),
    ]
