# Generated by Django 4.1.1 on 2022-10-11 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_update_at_alter_post_create_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file_upload',
            field=models.FileField(blank=True, upload_to='blog/files/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='post',
            name='head_image',
            field=models.ImageField(blank=True, upload_to='blog/images/%Y/%m/%d/'),
        ),
    ]