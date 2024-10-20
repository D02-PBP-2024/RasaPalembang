from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RestoranForm
from .models import Restoran


def restoran(request):
    restoran_list = Restoran.objects.all()
    return render(request, "restoran/index.html", {"restoran_list": restoran_list})


@login_required(login_url="/login")
def tambah_restoran(request):
    if request.method == "POST":
        form = RestoranForm(request.POST)
        if form.is_valid():
            restoran = form.save(commit=False)
            restoran.user = request.user
            restoran.save()
            return redirect("restoran:restoran")
    else:
        form = RestoranForm()

    return render(request, "tambah/index.html", {"form": form})


@login_required(login_url="/login")
def ubah_restoran(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    if request.user != restoran.user:  # Pastikan yang mengedit adalah pemilik
        return HttpResponseRedirect(reverse("restoran:restoran"))

    form = RestoranForm(request.POST or None, instance=restoran)
    if form.is_valid():
        form.save()
        return redirect("restoran:restoran")
    return render(request, "ubah/index.html", {"form": form})


@login_required(login_url="/login")
def hapus_restoran(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    if request.user != restoran.user:  # Pastikan yang menghapus adalah pemilik
        return HttpResponseRedirect(reverse("restoran:restoran"))

    if request.method == "POST":
        restoran.delete()
        return redirect("restoran:restoran")
    else:
        return HttpResponseRedirect(reverse("restoran:restoran"))
