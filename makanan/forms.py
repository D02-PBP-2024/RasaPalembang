from django.forms import ModelForm
from django import forms
from makanan.models import Makanan

class MakananForm(ModelForm):
    class Meta:
        model = Makanan
        fields = ['nama', 'harga', 'deskripsi', 'gambar', 'kalori', 'restoran', 'kategori']
        widgets = {
            'kategori': forms.CheckboxSelectMultiple(),  # Set kategori jadi checkbox
        }