# Generated by Django 2.1.3 on 2018-11-24 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_test_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True),
        ),
    ]
