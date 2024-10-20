from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Restoran
from .forms import RestoranForm

def show_restoran(request):
    restoran_list = Restoran.objects.all()
    return render(request, 'restoran/index.html', {'restoran_list': restoran_list})

@login_required
def create_restoran(request):
    if request.method == 'POST':
        form = RestoranForm(request.POST)
        if form.is_valid():
            restoran = form.save(commit=False)
            restoran.user = request.user 
            restoran.save()
            return redirect('show_restoran')
    else:
        form = RestoranForm()
    return render(request, 'create/index.html', {'form': form})

@login_required
def edit_restoran(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    if request.user != restoran.user:  # Pastikan yang mengedit adalah pemilik
        return HttpResponseRedirect(reverse('show_restoran'))

    form = RestoranForm(request.POST or None, instance=restoran)
    if form.is_valid():
        form.save()
        return redirect('show_restoran')
    return render(request, 'edit/index.html', {'form': form})

@login_required
def delete_restoran(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    if request.user != restoran.user:  # Pastikan yang menghapus adalah pemilik
        return HttpResponseRedirect(reverse('show_restoran'))

    if request.method == 'POST':
        restoran.delete()
        return redirect('show_restoran')
    else:
        return HttpResponseRedirect(reverse('show_restoran'))
