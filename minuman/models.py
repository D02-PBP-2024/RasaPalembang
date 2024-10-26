from restoran.models import Restoran
from django.db import models
import uuid


class Minuman(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    UKURAN_CHOICES = [
        ("KECIL", "K"),
        ("SEDANG", "S"),
        ("BESAR", "B"),
    ]

    nama = models.CharField(max_length=255)
    harga = models.IntegerField()
    deskripsi = models.TextField(blank=True)
    gambar = models.ImageField(upload_to="gambar_minuman/", blank=True, null=True)
    ukuran = models.CharField(max_length=6, choices=UKURAN_CHOICES)
    tingkat_kemanisan = models.IntegerField(blank=True, null=True)

    restoran = models.ForeignKey(Restoran, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama
