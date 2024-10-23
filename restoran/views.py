from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from restoran.forms import RestoranForm
from restoran.models import Restoran
from ulasan.models import Ulasan
from django.urls import reverse


def restoran(request):
    restoran_list = Restoran.objects.all()
    return render(request, "restoran/restoran/index.html", {"restoran_list": restoran_list})


@login_required(login_url="/login")
def tambah_restoran(request):
    # Pastikan yang menambah restoran adalah user dengan role pemilik_restoran
    if request.user.peran != "pemilik_restoran":
        return redirect("restoran:restoran")

    if request.method == "POST":
        form = RestoranForm(request.POST)
        if form.is_valid():
            restoran = form.save(commit=False)
            restoran.user = request.user
            restoran.save()
            return redirect("restoran:restoran")
    else:
        form = RestoranForm()

    return render(request, "restoran/tambah/index.html", {"form": form})


@login_required(login_url="/login")
def ubah_restoran(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    if request.user != restoran.user:  # Pastikan yang mengedit adalah pemilik
        return HttpResponseRedirect(reverse("restoran:restoran"))

    form = RestoranForm(request.POST or None, instance=restoran)
    if form.is_valid():
        form.save()
        return redirect("restoran:restoran")
    return render(request, "restoran/ubah/index.html", {"form": form})


@login_required(login_url="/login")
def hapus_restoran(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    if request.user != restoran.user:  
        return HttpResponseRedirect(reverse("restoran:restoran"))

    if request.method == "POST":
        restoran.delete()
        return redirect("restoran:restoran")
    else:
        return HttpResponseRedirect(reverse('restoran:restoran'))

def lihat_restoran(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    mengulas = False

    if request.user.is_authenticated and request.user.peran == 'pengulas':
        mengulas = not Ulasan.objects.filter(restoran=restoran, user=request.user).exists()

    return render(request, 'restoran/detail/index.html', {
        'restoran': restoran,
        'mengulas': mengulas,
    })
