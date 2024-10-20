from django.shortcuts import render, redirect, get_object_or_404
from makanan.forms import MakananForm, KategoriForm
from makanan.models import Makanan, Kategori
from restoran.models import Restoran
from django.urls import reverse

def show_makanan(request):
    makanan = Makanan.objects.all()
    context = {'makanan': makanan}
    return render(request, 'makanan/show_makanan.html', context)

def tambah_makanan(request):
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
    }
    return render(request, "tambah/tambah_makanan.html", context)

def show_makanan_by_id(request, id):
    makanan = get_object_or_404(Makanan, pk=id)
    context = {'makanan': makanan}
    return render(request, 'makanan/show_makanan_by_id.html', context)

def edit_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)
    form = MakananForm(request.POST or None, instance=makanan)

    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('makanan:show_makanan_by_id', id=id)
    
    context = {'form': form}
    return render(request, 'makanan/edit_makanan.html', context)

def delete_makanan(request, id):
    makanan = Makanan.objects.get(pk=id)
    makanan.delete()
    return redirect("makanan:show_makanan")

def show_kategori(request):
    kategori = Kategori.objects.all()  # Mengambil semua kategori
    context = {'kategori': kategori}
    return render(request, 'kategori/show_kategori.html', context)

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
    return render(request, "kategori/tambah_kategori.html", context)

def edit_kategori(request, id):
    kategori = get_object_or_404(Kategori, pk=id)
    form = KategoriForm(request.POST or None, instance=kategori)

    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('makanan:show_kategori')

    context = {'form': form}
    return render(request, 'kategori/edit_kategori.html', context)

def delete_kategori(request, id):
    kategori = get_object_or_404(Kategori, pk=id)
    kategori.delete()
    return redirect("makanan:show_kategori")