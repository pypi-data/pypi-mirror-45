# Generated by Django 2.0.4 on 2018-05-03 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_textract', '0002_auto_20180502_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='transcription',
            field=models.TextField(blank=True, default=''),
        ),
    ]
