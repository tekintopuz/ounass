# Generated by Django 4.0 on 2021-12-25 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_myadcreative'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myadcreative',
            name='object_story_spec',
            field=models.JSONField(blank=True, null=True),
        ),
    ]