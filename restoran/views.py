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
from django.db.models import Avg, Min, Max, F
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

def get_harga_range(restoran):
    makanan = Makanan.objects.filter(restoran=restoran)
    minuman = Minuman.objects.filter(restoran=restoran)

    if not makanan.exists() and not minuman.exists():
        return "" 

    avg_harga_makanan = makanan.aggregate(Avg('harga'))['harga__avg'] or 0
    avg_harga_minuman = minuman.aggregate(Avg('harga'))['harga__avg'] or 0

    avg_harga_tertinggi = max(avg_harga_makanan, avg_harga_minuman)

    if avg_harga_tertinggi <= 20000:
        return "$"     
    elif avg_harga_tertinggi <= 40000:
        return "$$"    
    elif avg_harga_tertinggi <= 70000:
        return "$$$"   
    else:
        return "$$$$"   
    
from django.db.models import Avg, F

def restoran(request):
    current_time = timezone.localtime().time()
    restoran_queryset = Restoran.objects.all()
    restoran_list = []
    sort_by = request.GET.get("sort", "default")

    for item in restoran_queryset:
        gambar_url = get_gambar_url(item)
        jam_buka = item.jam_buka
        jam_tutup = item.jam_tutup
        status = get_restoran_status(jam_buka, jam_tutup, current_time)
        ulasan_terbaik = Ulasan.objects.filter(restoran=item).order_by('-nilai')[:2]

        restoran_data.append(
            {
                "restoran": item,
                "status": status,
                "jam_buka": jam_buka.strftime("%H:%M"),
                "jam_tutup": jam_tutup.strftime("%H:%M"),
                "rata_bintang": round(item.rata_bintang or 0, 1),
                "harga_range": get_harga_range(item),
                "ulasan_terbaik": ulasan_terbaik,
            }
        )

    paginator = Paginator(restoran_data, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "restoran/restoran/index.html",
        {"page_obj": page_obj, "sort_by": sort_by, 'order': order},
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
            "restoran": restoran,
            "makanan": makanan,
            "minuman": minuman,
            "mengulas": mengulas,
            "status": status,
        },
    )
