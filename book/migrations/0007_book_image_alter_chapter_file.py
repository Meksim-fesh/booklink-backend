# Generated by Django 5.1.4 on 2025-03-18 03:21

import book.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0006_chapter_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="image",
            field=models.FileField(
                default=django.utils.timezone.now,
                max_length=256,
                storage=book.models.BookRelatedS3Storage,
                upload_to=book.models.get_image_s3_path,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="chapter",
            name="file",
            field=models.FileField(
                default=django.utils.timezone.now,
                max_length=256,
                storage=book.models.BookRelatedS3Storage,
                upload_to=book.models.get_chapter_s3_path,
            ),
            preserve_default=False,
        ),
    ]
