# Generated by Django 3.1 on 2021-05-20 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Summarize', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiosummarizemodel',
            name='audioDescription',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='audiosummarizemodel',
            name='audioName',
            field=models.CharField(default='Meeting Audio', max_length=255),
        ),
    ]
