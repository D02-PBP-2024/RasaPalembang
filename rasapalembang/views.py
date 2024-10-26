from restoran.models import Restoran
from django.shortcuts import render
from minuman.models import Minuman
from django.utils import timezone
import random


def landing(request):
    restoran = list(Restoran.objects.all())
    minuman = list(Minuman.objects.all())

    restoran_length = len(restoran)
    minuman_length = len(minuman)

    if restoran_length > 3:
        restoran_list = random.sample(restoran, 4)
    else:
        restoran_list = random.sample(restoran, restoran_length)

    if minuman_length > 3:
        minuman_list = random.sample(minuman, 4)
    else:
        minuman_list = random.sample(minuman, minuman_length)

    current_time = timezone.localtime().time()
    restoran_with_status = []

    for restoran in restoran_list:
        jam_buka = restoran.jam_buka
        jam_tutup = restoran.jam_tutup

        if jam_buka < jam_tutup:
            if jam_buka <= current_time <= jam_tutup:
                status = "Buka"
            else:
                status = "Tutup"
        else:
            if current_time >= jam_buka or current_time <= jam_tutup:
                status = "Buka"
            else:
                status = "Tutup"

        restoran_with_status.append(
            {
                "restoran": restoran,
                "status": status,
                "jam_buka": jam_buka.strftime("%H:%M"),
                "jam_tutup": jam_tutup.strftime("%H:%M"),
            }
        )

    return render(request, "landing/index.html", {
        "restoran": restoran_with_status,
        "minuman":  minuman_list,
    })
