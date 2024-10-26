from restoran.models import Restoran
from django.shortcuts import render
from minuman.models import Minuman
from makanan.models import Makanan
from django.utils import timezone
from django.db.models import Q
import random


def landing(request):
    restoran = list(Restoran.objects.all())
    makanan = list(Makanan.objects.all())
    minuman = list(Minuman.objects.all())

    restoran_length = len(restoran)
    makanan_length = len(makanan)
    minuman_length = len(minuman)

    if restoran_length > 3:
        restoran = random.sample(restoran, 4)
    else:
        restoran = random.sample(restoran, restoran_length)

    if makanan_length > 3:
        makanan = random.sample(makanan, 4)
    else:
        makanan = random.sample(makanan, makanan_length)

    if minuman_length > 3:
        minuman = random.sample(minuman, 4)
    else:
        minuman = random.sample(minuman, minuman_length)

    current_time = timezone.localtime().time()
    restoran_list = []

    for item in restoran:
        gambar_url = None
        if hasattr(item, "gambar") and item.gambar:
            gambar_url = str(item.gambar.url).replace("%3A", ":/")

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

    return render(
        request,
        "landing/index.html",
        {
            "restoran": restoran_list,
            "makanan": makanan,
            "minuman": minuman,
        },
    )


def cari(request):
    keyword = request.GET.get("q")

    restoran = Restoran.objects.none()
    makanan = Makanan.objects.none()
    minuman = Minuman.objects.none()

    if keyword:
        restoran = Restoran.objects.filter(nama__icontains=keyword)
        makanan = Makanan.objects.filter(
            Q(nama__icontains=keyword) | Q(deskripsi__icontains=keyword)
        )
        minuman = Minuman.objects.filter(
            Q(nama__icontains=keyword) | Q(deskripsi__icontains=keyword)
        )

    return render(
        request,
        "cari/index.html",
        {
            "restoran": restoran,
            "makanan": makanan,
            "minuman": minuman,
            "keyword": keyword,
        },
    )
