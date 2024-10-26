from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from restoran.forms import RestoranForm
from restoran.models import Restoran
from makanan.models import Makanan
from minuman.models import Minuman
from django.utils import timezone
from ulasan.models import Ulasan
from django.db.models import Avg
from django.urls import reverse
from .forms import RestoranForm
from .models import Restoran


def get_gambar_url(item):
    return (
        str(item.gambar.url).replace("%3A", ":/")
        if hasattr(item, "gambar") and item.gambar
        else None
    )


def get_restoran_status(jam_buka, jam_tutup, current_time):
    if jam_buka < jam_tutup:
        return "Buka" if jam_buka <= current_time <= jam_tutup else "Tutup"
    return "Buka" if current_time >= jam_buka or current_time <= jam_tutup else "Tutup"


def restoran(request):
    current_time = timezone.localtime().time()
    restoran_queryset = Restoran.objects.all()
    restoran_list = []
    sort_by = request.GET.get("sort", "default")

    for item in restoran_queryset:
        gambar_url = get_gambar_url(item)
        jam_buka = item.jam_buka
        jam_tutup = item.jam_tutup

        ulasan = Ulasan.objects.filter(restoran=item)
        rata_bintang = ulasan.aggregate(Avg("nilai"))["nilai__avg"] or 0

        status = get_restoran_status(jam_buka, jam_tutup, current_time)

        restoran_list.append(
            {
                "restoran": item,
                "gambar_url": gambar_url,
                "status": status,
                "jam_buka": jam_buka.strftime("%H:%M"),
                "jam_tutup": jam_tutup.strftime("%H:%M"),
                "rata_bintang": round(rata_bintang, 1),
                "ulasan_terbaik": ulasan.order_by("-nilai")[:2],
            }
        )

    if sort_by == "rating":
        restoran_list.sort(key=lambda x: x["rata_bintang"], reverse=True)

    paginator = Paginator(restoran_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "restoran/restoran/index.html",
        {"page_obj": page_obj, "sort_by": sort_by},
    )


@login_required(login_url="/login")
def tambah_restoran(request):
    if request.user.peran != "pemilik_restoran":
        return redirect("restoran:restoran")

    if request.method == "POST":
        form = RestoranForm(request.POST, request.FILES)
        if form.is_valid():
            restoran = form.save(commit=False)
            restoran.user = request.user
            restoran.save()
            return redirect("restoran:restoran")
    else:
        form = RestoranForm()

    return render(request, "restoran/tambah/index.html", {"form": form})


@login_required(login_url="/login")
def ubah_restoran(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    if request.user != restoran.user:  # Pastikan yang mengedit adalah pemilik
        return HttpResponseRedirect(reverse("restoran:restoran"))

    form = RestoranForm(request.POST or None, request.FILES or None, instance=restoran)
    if form.is_valid():
        form.save()
        return redirect("restoran:restoran")
    return render(request, "restoran/ubah/index.html", {"form": form})


@login_required(login_url="/login")
def hapus_restoran(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    if request.user != restoran.user:
        return HttpResponseRedirect(reverse("restoran:restoran"))

    if request.method == "POST":
        restoran.delete()
        return redirect("restoran:restoran")
    else:
        return HttpResponseRedirect(reverse("restoran:restoran"))


def lihat_restoran(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    makanan = Makanan.objects.filter(restoran=restoran)
    minuman = Minuman.objects.filter(restoran=restoran)

    restoran_list = {
        "restoran": restoran,
        "gambar_url": get_gambar_url(restoran),
    }

    makanan_list = [
        {
            "makanan": item,
            "gambar_url": get_gambar_url(item),
        }
        for item in makanan
    ]

    minuman_list = [
        {
            "minuman": item,
            "gambar_url": get_gambar_url(item),
        }
        for item in minuman
    ]

    mengulas = (
        request.user.is_authenticated
        and request.user.peran == "pengulas"
        and not Ulasan.objects.filter(restoran=restoran, user=request.user).exists()
    )

    current_time = timezone.localtime().time()
    jam_buka = restoran.jam_buka
    jam_tutup = restoran.jam_tutup

    if jam_buka < jam_tutup:
        status = "Buka" if jam_buka <= current_time <= jam_tutup else "Tutup"
    else:
        status = (
            "Buka" if current_time >= jam_buka or current_time <= jam_tutup else "Tutup"
        )

    return render(
        request,
        "restoran/detail/index.html",
        {
            "restoran": restoran_list,
            "makanan": makanan_list,
            "minuman": minuman_list,
            "mengulas": mengulas,
            "status": status,
        },
    )
