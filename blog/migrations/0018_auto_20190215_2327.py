# Generated by Django 2.1.3 on 2019-02-16 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20190215_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='blog.CustomImage'),
        ),
    ]