from django.forms import ModelForm
from makanan.models import Makanan, Kategori

class MakananForm(ModelForm):
    class Meta:
        model = Makanan
        fields = ['nama', 'harga', 'deskripsi', 'gambar', 'kalori']

class KategoriForm(ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama']