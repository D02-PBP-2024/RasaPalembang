from django.forms import ModelForm
from minuman.models import Minuman


class MinumanForm(ModelForm):
    class Meta:
        model = Minuman
        fields = [
            "nama",
            "harga",
            "deskripsi",
            "gambar",
            "ukuran",
            "tingkat_kemanisan",
            "restoran",
        ]
