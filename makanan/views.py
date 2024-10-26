import json
from django.shortcuts import render, redirect, get_object_or_404
from makanan.forms import MakananForm
from makanan.models import Makanan, Kategori
from restoran.models import Restoran
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse


def show_makanan(request):
    makanan = Makanan.objects.all()
    paginator = Paginator(makanan, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    list_kategori = Kategori.objects.all()
    context = {
        "makanan_list": makanan,
        "page_obj": page_obj,
        "total_page": paginator.num_pages,
        "list_kategori": list_kategori,
    }
    return render(request, "makanan/show/show_makanan.html", context)


@login_required(login_url="/login")
def tambah_makanan(request):
    # Pengecekan apakah user adalah pemilik_restoran
    if request.user.peran != "pemilik_restoran":
        return redirect("makanan:show_makanan")

    restoran = Restoran.objects.filter(user=request.user)

    if request.method == "POST":
        form = MakananForm(request.POST, request.FILES)
        if form.is_valid():
            makanan = form.save(commit=False)
            makanan.save()
            return redirect("makanan:show_makanan")
    else:
        form = MakananForm()

    context = {
        "form": form,
        "restoran": restoran,
    }
    return render(request, "makanan/tambah/tambah_makanan.html", context)


def detail_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)
    list_kategori = Kategori.objects.filter(makanan=makanan)
    restoran = Restoran.objects.get(pk=makanan.restoran.id)

    context = {"makanan": makanan, "list_kategori": list_kategori, "restoran": restoran}
    return render(request, "makanan/detail/detail_makanan.html", context)


@login_required(login_url="/login")
def edit_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)

    # Pengecekan apakah user adalah pemilik_restoran
    if (
        request.user.peran != "pemilik_restoran"
        or request.user != makanan.restoran.user
    ):
        return redirect("makanan:edit_makanan")

    # Tambahkan `request.FILES` untuk menangani file gambar
    form = MakananForm(request.POST or None, request.FILES or None, instance=makanan)

    if form.is_valid() and request.method == "POST":
        form.save()  # Simpan gambar baru atau update field lainnya
        return redirect("makanan:detail_makanan", id=id)

    context = {"form": form, "makanan": makanan}
    return render(request, "makanan/edit_makanan/edit_makanan.html", context)


@login_required(login_url="/login")
def delete_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)

    # Pengecekan apakah user adalah pemilik_restoran
    if (
        request.user.peran != "pemilik_restoran"
        or request.user != makanan.restoran.user
    ):
        return redirect("makanan:delete_makanan")

    makanan.delete()
    return redirect("makanan:show_makanan")


def filter_by_kategori(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Ambil data JSON dari request body
            kategori_id = data.get(
                "kategori_id"
            )  # Dapatkan kategori ID dari request body, default empty list

            # Filter makanan berdasarkan kategori yang dipilih
            if len(kategori_id) > 0:
                makanan_list = Makanan.objects.filter(kategori__id__in=kategori_id)
            else:
                makanan_list = Makanan.objects.all()

            # Persiapkan data makanan untuk dikirim kembali sebagai response JSON\
            makanan_data = []
            for makanan in makanan_list:
                makanan = {
                    "id": makanan.id,
                    "nama": makanan.nama,
                    "gambar": makanan.gambar.url if makanan.gambar else "",
                    "harga": makanan.harga,
                    "kalori": makanan.kalori,
                    "deskripsi": makanan.deskripsi,
                    "restoran": makanan.restoran.nama,
                }
                if makanan not in makanan_data:
                    makanan_data.append(makanan)

            # Kirim response JSON ke frontend
            return JsonResponse({"makanan": makanan_data})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
