from restoran.models import Restoran
from django.shortcuts import render
from minuman.models import Minuman
from django.utils import timezone
import random


def landing(request):
    restoran_list = random.sample(list(Restoran.objects.all()), 4)
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

    minuman = random.sample(list(Minuman.objects.all()), 4)

    return render(request, "landing/index.html", {
        "restoran": restoran_with_status,
        "minuman": minuman,
    })
