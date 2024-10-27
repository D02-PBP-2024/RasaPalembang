from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from favorit.forms import FavoritForm
from restoran.models import Restoran
from favorit.models import Favorit
from makanan.models import Makanan
from minuman.models import Minuman


@login_required(login_url="/login")
def show_favorit(request):
    """
    Menampilkan daftar favorit untuk pengguna yang sedang login.
    """
    favorit = Favorit.objects.filter(user=request.user)
    return render(request, "favorit/favorit/index.html", {"favorit": favorit})


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
        return redirect("favorit:show_favorit")

    return render(request, "favorit/hapus/index.html", {"favorit": favorit})


@login_required(login_url="/login")
def add_to_favorites(request, item_type, item_id):
    """
    Menambahkan makanan, minuman, atau restoran ke daftar favorit pengguna yang sedang login.
    """
    # Cek tipe item dan dapatkan objek item berdasarkan item_type dan item_id
    if item_type == "makanan":
        item = get_object_or_404(Makanan, id=item_id)
        favorit, created = Favorit.objects.get_or_create(
            user=request.user, makanan=item
        )
    elif item_type == "minuman":
        item = get_object_or_404(Minuman, id=item_id)
        favorit, created = Favorit.objects.get_or_create(
            user=request.user, minuman=item
        )
    elif item_type == "restoran":
        item = get_object_or_404(Restoran, id=item_id)
        favorit, created = Favorit.objects.get_or_create(
            user=request.user, restoran=item
        )
    else:
        return redirect("home")

    # Arahkan kembali ke halaman yang memanggil atau ke halaman favorit
    return redirect("favorit:show_favorit")
