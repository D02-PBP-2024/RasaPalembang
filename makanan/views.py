from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from makanan.models import Makanan, Kategori
from makanan.forms import MakananForm
from restoran.models import Restoran
from django.http import JsonResponse
import json
from django.utils.html import strip_tags


def show_makanan(request):
    makanan = Makanan.objects.all()
    list_kategori = Kategori.objects.all()

    return render(
        request,
        "makanan/show/index.html",
        {"makanan": makanan, "list_kategori": list_kategori},
    )


@login_required(login_url="/login")
def tambah_makanan(request):
    if request.user.peran != "pemilik_restoran":
        return redirect("makanan:show_makanan")
    
    restoran = Restoran.objects.filter(user=request.user)

    if request.method == "POST":
        form = MakananForm(request.POST, request.FILES)
        if form.is_valid():
            makanan = form.save(commit=False)
            makanan.nama = strip_tags(makanan.nama)
            makanan.deskripsi = strip_tags(makanan.deskripsi)
            makanan.save()
            form.save_m2m()
            return redirect("makanan:show_makanan")
    else:
        form = MakananForm()

    context = {
        "form": form,
        "restoran": restoran,
    }
    return render(request, "makanan/tambah/index.html", context)


def detail_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)
    list_kategori = Kategori.objects.filter(makanan=makanan)
    restoran = Restoran.objects.get(pk=makanan.restoran.id)
    mengubah = restoran.user == request.user

    context = {
        "makanan": makanan,
        "list_kategori": list_kategori,
        "restoran": restoran,
        "mengubah": mengubah,
    }
    return render(request, "makanan/detail/index.html", context)


@login_required(login_url="/login")
def ubah_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)
    restoran = Restoran.objects.filter(user=request.user)
    kategori = Kategori.objects.filter(makanan=makanan)

    if (
        request.user.peran != "pemilik_restoran"
        or request.user != makanan.restoran.user
    ):
        return redirect("makanan:ubah_makanan")

    form = MakananForm(request.POST or None, request.FILES or None, instance=makanan)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("makanan:detail_makanan", id=id)

    context = {
        "form": form,
        "makanan": makanan,
        "restoran": restoran,
        "selected_kategori": kategori,
    }
    return render(request, "makanan/ubah/index.html", context)


@login_required(login_url="/login")
def hapus_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)

    # Pengecekan apakah user adalah pemilik_restoran
    if (
        request.user.peran != "pemilik_restoran"
        or request.user != makanan.restoran.user
    ):
        return redirect("makanan:hapus_makanan")

    makanan.delete()
    return redirect("makanan:show_makanan")


def filter_by_kategori(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            kategori_id = data.get("kategori_id")

            if len(kategori_id) > 0:
                makanan_list = Makanan.objects.filter(kategori__id__in=kategori_id)
            else:
                makanan_list = Makanan.objects.all()

            makanan_data = []
            for makanan in makanan_list:
                makanan = {
                    "id": makanan.id,
                    "nama": makanan.nama,
                    "gambar": makanan.gambar.url,
                    "harga": makanan.harga,
                    "kalori": makanan.kalori,
                    "deskripsi": makanan.deskripsi,
                    "restoran": makanan.restoran.nama,
                }
                if makanan not in makanan_data:
                    makanan_data.append(makanan)

            return JsonResponse({"makanan": makanan_data})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
