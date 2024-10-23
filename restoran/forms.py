from django import forms
from .models import Restoran

class RestoranForm(forms.ModelForm):
    class Meta:
        model = Restoran
        fields = ['nama', 'alamat', 'jam_buka', 'jam_tutup', 'nomor_telepon', 'gambar']
