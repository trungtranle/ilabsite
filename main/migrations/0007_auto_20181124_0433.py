# Generated by Django 2.1.3 on 2018-11-24 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20181124_0425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='referance_range',
            field=models.TextField(blank=True, null=True, verbose_name='Reference range'),
        ),
    ]
