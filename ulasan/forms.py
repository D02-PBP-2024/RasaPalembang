from django.forms import ModelForm
from ulasan.models import Ulasan


class UlasanForm(ModelForm):
    class Meta:
        model = Ulasan
        fields = ["nilai", "deskripsi"]
