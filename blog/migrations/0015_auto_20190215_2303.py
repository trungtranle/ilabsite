# Generated by Django 2.1.3 on 2019-02-16 06:03

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('blog', '0014_auto_20190215_1950'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPeopleRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_person_relationship', to='blog.BlogPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='First name')),
                ('job_title', models.CharField(blank=True, max_length=254, verbose_name='Job title')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'People',
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.AddField(
            model_name='blogpeoplerelationship',
            name='people',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_blog_relationship', to='blog.People'),
        ),
    ]
