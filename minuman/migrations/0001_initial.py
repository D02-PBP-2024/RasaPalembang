# Generated by Django 5.1.2 on 2024-10-25 20:49

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restoran', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Minuman',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=255)),
                ('harga', models.IntegerField()),
                ('deskripsi', models.TextField(blank=True)),
                ('gambar', models.ImageField(blank=True, null=True, upload_to='gambar_minuman/')),
                ('ukuran', models.CharField(choices=[('KECIL', 'K'), ('SEDANG', 'S'), ('BESAR', 'B')], max_length=6)),
                ('tingkat_kemanisan', models.IntegerField(blank=True, null=True)),
                ('restoran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restoran.restoran')),
            ],
        ),
    ]
