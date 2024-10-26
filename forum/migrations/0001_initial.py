# Generated by Django 5.1.2 on 2024-10-26 17:26

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restoran', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('topik', models.CharField(max_length=255)),
                ('pesan', models.TextField()),
                ('tanggal_posting', models.DateTimeField(auto_now_add=True)),
                ('restoran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restoran.restoran')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Balasan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pesan', models.TextField()),
                ('tanggal_posting', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.forum')),
            ],
        ),
    ]
