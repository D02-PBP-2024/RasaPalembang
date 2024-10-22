from django.forms import ModelForm
from makanan.models import Makanan

class MakananForm(ModelForm):
    class Meta:
        model = Makanan
        fields = ['nama', 'harga', 'deskripsi', 'gambar', 'kalori', 'restoran', 'kategori']