from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from favorit.forms import FavoritForm
from django.contrib import messages
from favorit.models import Favorit


@login_required(login_url="/login")
def show_favorit(request):
    """
    Menampilkan daftar favorit untuk pengguna yang sedang login.
    """
    favorit = Favorit.objects.filter(user=request.user)
    return render(request, "favorit/favorit/index.html", {"favorit": favorit})


@login_required(login_url="/login")
def tambah_favorit(request):
    """
    Menambahkan makanan, minuman, atau restoran ke dalam daftar favorit.
    """
    if request.method == "POST":
        form = FavoritForm(request.POST)
        if form.is_valid():
            favorit = form.save(commit=False)
            favorit.user = request.user  # Set pengguna yang sedang login
            favorit.save()
            messages.success(request, "Favorit berhasil ditambahkan.")
            return redirect("favorit:show_favorit")
    else:
        form = FavoritForm()

    return render(request, "favorit/tambah/index.html", {"form": form})


@login_required(login_url="/login")
def ubah_favorit(request, favorit_id):
    """
    Mengedit catatan favorit yang sudah ada.
    """
    favorit = get_object_or_404(Favorit, id=favorit_id, user=request.user)

    if request.method == "POST":
        form = FavoritForm(request.POST, instance=favorit)
        if form.is_valid():
            form.save()
            messages.success(request, "Favorit berhasil diperbarui.")
            return redirect("favorit:show_favorit")
    else:
        form = FavoritForm(instance=favorit)

    return render(request, "favorit/ubah/index.html", {"form": form})


@login_required(login_url="/login")
def hapus_favorit(request, favorit_id):
    """
    Menghapus favorit dari daftar.
    """
    favorit = get_object_or_404(Favorit, id=favorit_id, user=request.user)

    if request.method == "POST":
        favorit.delete()
        messages.success(request, "Favorit berhasil dihapus.")
        return redirect("favorit:show_favorit")

    return render(request, "favorit/hapus/index.html", {"favorit": favorit})
