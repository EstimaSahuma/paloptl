# Generated by Django 3.0.8 on 2021-01-12 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0003_auto_20201204_1945'),
        ('budget', '0006_auto_20210112_1647'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='budget',
            unique_together={('country', 'year')},
        ),
    ]
