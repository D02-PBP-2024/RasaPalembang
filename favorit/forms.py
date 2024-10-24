from django.forms import ModelForm
from favorit.models import Favorit


class FavoritForm(ModelForm):
    class Meta:
        model = Favorit
        fields = ["catatan", "makanan", "minuman", "restoran"]
