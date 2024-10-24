from authentication.models import User
from restoran.models import Restoran
from makanan.models import Makanan
from minuman.models import Minuman
from django.db import models
import uuid


class Favorit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    catatan = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    makanan = models.ForeignKey(Makanan, on_delete=models.CASCADE, blank=True, null=True)
    minuman = models.ForeignKey(Minuman, on_delete=models.CASCADE, blank=True, null=True)
    restoran = models.ForeignKey(Restoran, on_delete=models.CASCADE, blank=True, null=True)
