# Generated by Django 4.1.1 on 2022-09-27 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
