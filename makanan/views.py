from django.shortcuts import render, redirect
from makanan.forms import MakananForm, KategoriForm
from makanan.models import Makanan, Kategori

def show_makanan(request):
    makanan = Makanan.objects.all()
    context = {'makanan': makanan}
    return render(request, 'makanan/show_makanan.html', context)

def create_makanan(request):
    form = MakananForm(request.POST)

    if form.is_valid() and request.method == 'POST':
        makanan_entry = form.save(commit=False)
        makanan_entry.restoran = request.user.restoran
        makanan_entry.save()
        return redirect('makanan:create_makanan')
    
    context = {'form': form}
    return render(request, 'create/create_makanan.html', context)

def show_makanan_by_id(request, id):
    makanan = Makanan.objects.get(pk=id)
    context = {'makanan': makanan} 
    return render(request, 'makanan/show_makanan_by_id.html', context)