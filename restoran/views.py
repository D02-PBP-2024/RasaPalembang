from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RestoranForm
from .models import Restoran
from django.utils import timezone

def restoran(request):
    current_time = timezone.localtime().time()
    restoran_list = Restoran.objects.all()
    restoran_with_status = []

    for restoran in restoran_list:
        jam_buka = restoran.jam_buka
        jam_tutup = restoran.jam_tutup

        if jam_buka < jam_tutup:
            if jam_buka <= current_time <= jam_tutup:
                status = "Open now"
            else:
                status = "Closed now"
        else:
            if current_time >= jam_buka or current_time <= jam_tutup:
                status = "Open now"
            else:
                status = "Closed now"

        restoran_with_status.append({
            'restoran': restoran,
            'status': status,
            'jam_buka': jam_buka.strftime("%H:%M"), 
            'jam_tutup': jam_tutup.strftime("%H:%M") 
        })

    return render(request, "restoran/index.html", {"restoran_with_status": restoran_with_status})



@login_required(login_url="/login")
def tambah_restoran(request):
    # Pastikan yang menambah restoran adalah user dengan role pemilik_restoran
    if request.user.peran != "pemilik_restoran":
        return redirect("restoran:restoran")

    if request.method == "POST":
        form = RestoranForm(request.POST, request.FILES)
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

    form = RestoranForm(request.POST or None, request.FILES or None, instance=restoran)
    if form.is_valid():
        form.save()
        return redirect("restoran:restoran")
    return render(request, "ubah/index.html", {"form": form})


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
    return render(request, 'detail/index.html', {'restoran': restoran})
