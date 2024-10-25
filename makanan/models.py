from restoran.models import Restoran
from django.db import models
import uuid

class Kategori(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    nama = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nama
    
class Makanan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    nama = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    deskripsi = models.TextField(blank=True)
    gambar = models.ImageField(upload_to='gambar_makanan/', blank=True, null=True)
    kalori = models.IntegerField(blank=True, null=True)

    restoran = models.ForeignKey(Restoran, on_delete=models.CASCADE)
    kategori = models.ManyToManyField(Kategori, related_name='makanan')
    
    def __str__(self):
        return self.nama