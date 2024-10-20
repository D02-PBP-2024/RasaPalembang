from django.forms import ModelForm
from restoran.models import Restoran


class RestoranForm(ModelForm):
    class Meta:
        model = Restoran
        fields = ["nama", "alamat", "jam_operasional", "nomor_telepon", "user"]
