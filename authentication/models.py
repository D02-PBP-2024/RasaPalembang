from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    PERAN_CHOICES = [
        ('pengulas', 'Pengulas'),
        ('pemilik_restoran', 'Pemilik Restoran'),
    ]

    nama = models.CharField(max_length=255)
    peran = models.CharField(max_length=20, choices=PERAN_CHOICES)
    poin = models.IntegerField(default=0)
    deskripsi = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.nama
