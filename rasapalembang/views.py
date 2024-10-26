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
        restoran = random.sample(restoran, 4)
    else:
        restoran = random.sample(restoran, restoran_length)

    if minuman_length > 3:
        minuman = random.sample(minuman, 4)
    else:
        minuman = random.sample(minuman, minuman_length)

    current_time = timezone.localtime().time()
    restoran_list = []
    minuman_list = []

    for item in restoran:
        gambar_url = None
        if hasattr(item, 'gambar') and item.gambar:
            gambar_url = str(item.gambar.url).replace('%3A', ':/')

        jam_buka = item.jam_buka
        jam_tutup = item.jam_tutup

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

        restoran_list.append(
            {
                "restoran": item,
                "gambar_url": gambar_url,
                "status": status,
                "jam_buka": jam_buka.strftime("%H:%M"),
                "jam_tutup": jam_tutup.strftime("%H:%M"),
            }
        )

    for item in minuman:
        gambar_url = None
        if hasattr(item, 'gambar') and item.gambar:
            gambar_url = str(item.gambar.url).replace('%3A', ':/')

        minuman_list.append(
            {
                "minuman": item,
                "gambar_url": gambar_url,
            }
        )

    return render(request, "landing/index.html", {
        "restoran": restoran_list,
        "minuman":  minuman_list,
    })
