from django.shortcuts import render, redirect, get_object_or_404
from makanan.forms import MakananForm
from makanan.models import Makanan, Kategori
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def show_makanan(request):
    makanan = Makanan.objects.all()
    paginator = Paginator(makanan, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'makanan_list': makanan,
        'page_obj': page_obj,
        'total_page': paginator.num_pages,
        }
    return render(request, 'makanan/show/show_makanan.html', context)

@login_required(login_url="/login")
def tambah_makanan(request):
    # Pengecekan apakah user adalah pemilik_restoran
    if request.user.peran != 'pemilik_restoran':
        return redirect("makanan:show_makanan")

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
    return render(request, "makanan/tambah/tambah_makanan.html", context)

def detail_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)
    list_kategori = Kategori.objects.filter(makanan=makanan)
    context = {'makanan': makanan, 'list_kategori': list_kategori}
    return render(request, 'makanan/detail/detail_makanan.html', context)

@login_required(login_url="/login")
def edit_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)

    # Pengecekan apakah user adalah pemilik_restoran
    if request.user.peran != 'pemilik_restoran' or request.user != makanan.restoran.user:
        return redirect("makanan:edit_makanan")

    # Tambahkan `request.FILES` untuk menangani file gambar
    form = MakananForm(request.POST or None, request.FILES or None, instance=makanan)

    if form.is_valid() and request.method == 'POST':
        form.save()  # Simpan gambar baru atau update field lainnya
        return redirect('makanan:detail_makanan', id=id)
    
    context = {'form': form, 'makanan': makanan}
    return render(request, 'makanan/edit_makanan/edit_makanan.html', context)

@login_required(login_url="/login")
def delete_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)

    # Pengecekan apakah user adalah pemilik_restoran
    if request.user.peran != 'pemilik_restoran' or request.user != makanan.restoran.user:
        return redirect("makanan:delete_makanan")
    
    makanan.delete()
    return redirect("makanan:show_makanan")

def filter_by_kategori(request, kategori_id):
    kategori = get_object_or_404(Kategori, pk=kategori_id)
    makanan_list = Makanan.objects.filter(kategori=kategori)
    
    context = {
        'kategoris': Kategori.objects.all(),
        'makanan_list': makanan_list,
        'selected_kategori': kategori
    }

    return render(request, 'makanan/show_makanan.html', context)