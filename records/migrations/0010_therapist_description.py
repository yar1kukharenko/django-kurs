# Generated by Django 4.2.2 on 2023-07-04 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0009_feelings_rename_queries_events_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapist',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]