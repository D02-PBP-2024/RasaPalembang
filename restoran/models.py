from authentication.models import User
from django.db import models
import uuid


class Restoran(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    nama = models.CharField(max_length=255)
    alamat = models.CharField(max_length=255)
    jam_buka = models.TimeField(default="08:00")  
    jam_tutup = models.TimeField(default="22:00")
    nomor_telepon = models.CharField(max_length=15, blank=True, null=True)
    gambar = models.ImageField(upload_to='gambar_restoran/', blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nama
