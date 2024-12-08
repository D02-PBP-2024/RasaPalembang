from django.forms import ModelForm
from django import forms
from makanan.models import Makanan
from django.utils.html import strip_tags

class MakananForm(ModelForm):
    class Meta:
        model = Makanan
        fields = ['nama', 'harga', 'deskripsi', 'gambar', 'kalori', 'restoran', 'kategori']
        widgets = {
            'kategori': forms.CheckboxSelectMultiple(),  # Set kategori jadi checkbox
        }

    def clean_nama(self):
        nama = self.cleaned_data.get('nama')
        return strip_tags(nama)
    
    def clean_deskripsi(self):
        deskripsi = self.cleaned_data.get('deskripsi')
        return strip_tags(deskripsi)