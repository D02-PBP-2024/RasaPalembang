from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    PERAN_CHOICES = [
        ('pengulas', 'Pengulas'),
        ('pemilik_restoran', 'Pemilik Restoran'),
    ]

    peran = models.CharField(max_length=20, choices=PERAN_CHOICES)
    poin = models.IntegerField(default=0)
    deskripsi = models.TextField(blank=True)
    foto = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username
