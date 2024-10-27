from django import forms
from .models import Restoran
from django.utils.html import strip_tags

class RestoranForm(forms.ModelForm):
    class Meta:
        model = Restoran
        fields = ['nama', 'alamat', 'jam_buka', 'jam_tutup', 'nomor_telepon', 'gambar']

    def clean_nama(self):
        nama = self.cleaned_data['nama']
        return strip_tags(nama)

    def clean_alamat(self):
        alamat = self.cleaned_data['alamat']
        return strip_tags(alamat)

    def clean_nomor_telepon(self):
        nomor_telepon = self.cleaned_data['nomor_telepon']
        return strip_tags(nomor_telepon)
