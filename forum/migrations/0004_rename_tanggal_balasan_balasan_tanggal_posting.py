# Generated by Django 5.1.2 on 2024-10-24 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_balasan_tanggal_balasan_forum_tanggal_posting_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='balasan',
            old_name='tanggal_balasan',
            new_name='tanggal_posting',
        ),
    ]
