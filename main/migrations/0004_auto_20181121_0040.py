# Generated by Django 2.1.3 on 2018-11-21 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20181121_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_requirement',
            name='edited',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='contact_requirement',
            name='added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
