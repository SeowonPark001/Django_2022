# Generated by Django 4.1.1 on 2022-10-18 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_file_upload_post_head_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='create_at',
            new_name='created_at',
        ),
    ]
