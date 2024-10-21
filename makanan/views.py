from django.shortcuts import render, redirect, get_object_or_404
from makanan.forms import MakananForm, KategoriForm
from makanan.models import Makanan, Kategori
from restoran.models import Restoran
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden

def show_makanan(request):
    makanan = Makanan.objects.all()
    context = {'makanan': makanan}
    return render(request, 'makanan/show_makanan/show_makanan.html', context)

@login_required(login_url="/login")
def tambah_makanan(request):
    # Pengecekan apakah user adalah pemilik_restoran
    if request.user.peran != 'pemilik_restoran':
        return redirect("makanan:show_makanan")

    if request.method == "POST":
        form = MakananForm(request.POST, request.FILES)
        if form.is_valid():
            makanan = form.save(commit=False)
            makanan.restoran = request.user.restoran  # Mengaitkan makanan dengan restoran milik user
            makanan.save()
            return redirect("makanan:show_makanan")
    else:
        form = MakananForm()

    context = {
        "form": form,
    }
    return render(request, "makanan/tambah/tambah_makanan.html", context)

def show_makanan_by_id(request, id):
    makanan = get_object_or_404(Makanan, pk=id)
    context = {'makanan': makanan}
    return render(request, 'makanan/show_makanan/show_makanan_by_id.html', context)

@login_required(login_url="/login")
def edit_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)

    # Pengecekan apakah user adalah pemilik_restoran
    if request.user.peran != 'pemilik_restoran' or request.user != makanan.restoran.user:
        return redirect("makanan:edit_makanan")

    form = MakananForm(request.POST or None, instance=makanan)

    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('makanan:show_makanan_by_id', id=id)
    
    context = {'form': form}
    return render(request, 'makanan/edit_makanan/edit_makanan.html', context)

@login_required(login_url="/login")
def delete_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)

    # Pengecekan apakah user adalah pemilik_restoran
    if request.user.peran != 'pemilik_restoran' or request.user != makanan.restoran.user:
        return redirect("makanan:delete_makanan")
    
    makanan.delete()
    return redirect("makanan:show_makanan")

def show_kategori(request):
    kategori = Kategori.objects.all()
    context = {'kategori': kategori}
    return render(request, 'makanan/kategori/show_kategori.html', context)

def tambah_kategori(request):
    if request.method == "POST":
        form = KategoriForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('makanan:show_kategori')
    else:
        form = KategoriForm()

    context = {
        "form": form,
    }
    return render(request, "makanan/kategori/tambah_kategori.html", context)

def edit_kategori(request, id):
    kategori = get_object_or_404(Kategori, pk=id)

    # Pengecekan apakah user adalah pemilik_restoran
    if request.user.peran != 'pemilik_restoran':
        return HttpResponseForbidden("Anda tidak memiliki akses untuk mengedit kategori ini.")
    
    form = KategoriForm(request.POST or None, instance=kategori)

    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('makanan:show_kategori')

    context = {'form': form}
    return render(request, 'makanan/kategori/edit_kategori.html', context)

def delete_kategori(request, id):
    kategori = get_object_or_404(Kategori, pk=id)

    # Pengecekan apakah user adalah pemilik_restoran
    if request.user.peran != 'pemilik_restoran':
        return HttpResponseForbidden("Anda tidak memiliki akses untuk menghapus kategori ini.")
    
    kategori.delete()
    return redirect("makanan:show_kategori")