# Generated by Django 5.1.2 on 2024-10-25 20:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('favorit', '0001_initial'),
        ('makanan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorit',
            name='makanan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='makanan.makanan'),
        ),
    ]
