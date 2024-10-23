from authentication.models import User
from restoran.models import Restoran
from django.db import models
import uuid


class Forum(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    topik = models.CharField(max_length=255)
    pesan = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restoran = models.ForeignKey(Restoran, on_delete=models.CASCADE)


class Balasan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    pesan = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balasan = models.ForeignKey(Balasan, on_delete=models.CASCADE)
