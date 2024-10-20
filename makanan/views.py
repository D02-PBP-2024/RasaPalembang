from django.shortcuts import render, redirect, get_object_or_404
from makanan.forms import MakananForm, KategoriForm
from makanan.models import Makanan, Kategori
from restoran.models import Restoran
from django.http import HttpResponseRedirect
from django.urls import reverse

def show_makanan(request):
    makanan = Makanan.objects.all()
    context = {'makanan': makanan}
    return render(request, 'makanan/show_makanan.html', context)

def tambah_makanan(request):
    restoran = Restoran.objects.filter(user=request.user)
    if request.method == "POST":
        form = MakananForm(request.POST, request.FILES)
        if form.is_valid():
            minuman = form.save(commit=False)
            minuman.save()
            return redirect("minuman:show_minuman")
    else:
        form = MakananForm()

    context = {
        "form": form,
        "restoran": restoran,
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