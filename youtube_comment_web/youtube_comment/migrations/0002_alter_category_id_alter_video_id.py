# Generated by Django 4.2 on 2023-05-05 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='video',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
