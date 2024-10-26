# Generated by Django 5.1.2 on 2024-10-26 17:26

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('makanan', '0001_initial'),
        ('minuman', '0001_initial'),
        ('restoran', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('catatan', models.TextField()),
                ('makanan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='makanan.makanan')),
                ('minuman', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='minuman.minuman')),
                ('restoran', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restoran.restoran')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
