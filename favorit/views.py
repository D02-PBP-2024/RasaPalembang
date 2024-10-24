from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Favorit
from .forms import FavoritForm 
from django.contrib import messages


@login_required
def show_favorit(request):
    """
    Menampilkan daftar favorit untuk pengguna yang sedang login.
    """
    favorit_show = Favorit.objects.filter(user=request.user)
    return render(request, 'favorit/favorit_show.html', {'favorit_show': favorit_show})


@login_required
def add_favorit(request):
    """
    Menambahkan makanan, minuman, atau restoran ke dalam daftar favorit.
    """
    if request.method == 'POST':
        form = FavoritForm(request.POST)
        if form.is_valid():
            favorit = form.save(commit=False)
            favorit.user = request.user  # Set pengguna yang sedang login
            favorit.save()
            messages.success(request, 'Favorit berhasil ditambahkan.')
            return redirect('show_favorit')
    else:
        form = FavoritForm()

    return render(request, 'favorit/add_favorit.html', {'form': form})


@login_required
def edit_favorit(request, favorit_id):
    """
    Mengedit catatan favorit yang sudah ada.
    """
    favorit = get_object_or_404(Favorit, id=favorit_id, user=request.user)

    if request.method == 'POST':
        form = FavoritForm(request.POST, instance=favorit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Favorit berhasil diperbarui.')
            return redirect('show_favorit')
    else:
        form = FavoritForm(instance=favorit)

    return render(request, 'favorit/edit_favorit.html', {'form': form})


@login_required
def delete_favorit(request, favorit_id):
    """
    Menghapus favorit dari daftar.
    """
    favorit = get_object_or_404(Favorit, id=favorit_id, user=request.user)
    if request.method == 'POST':
        favorit.delete()
        messages.success(request, 'Favorit berhasil dihapus.')
        return redirect('show_favorit')

    return render(request, 'favorit/delete_favorit.html', {'favorit': favorit})
