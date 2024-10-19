from django.contrib.auth.models import User
from restoran.models import Restoran
from django.db import models
import uuid


class Ulasan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    nilai = models.PositiveIntegerField()
    deskripsi = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restoran = models.ForeignKey(Restoran, on_delete=models.CASCADE)
