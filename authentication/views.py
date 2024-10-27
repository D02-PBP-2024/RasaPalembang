from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from authentication.forms import CreateUserForm, UserForm
from django.contrib.auth.forms import AuthenticationForm
from authentication.models import User
from django.contrib import messages
from django.core import serializers

from restoran.models import Restoran
from ulasan.models import Ulasan
import datetime
import django


def signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Akun Anda telah berhasil dibuat! Silakan login.")
            return redirect("login")
    return render(request, "authentication/signup/index.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            django.contrib.auth.login(request, user)
            response = HttpResponseRedirect("/")
            response.set_cookie("last_login", str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    return render(request, "authentication/login/index.html", {"form": form})


def logout(request):
    django.contrib.auth.logout(request)
    response = HttpResponseRedirect("/")
    response.delete_cookie("last_login")
    return response


@login_required(login_url="/login")
def profile(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponse(b"UPDATED", status=200)

    user = User.objects.filter(username=request.user.username)

    return HttpResponse(
        serializers.serialize("json", user), content_type="application/json"
    )


def detail_profile(request, username):
    user = get_object_or_404(User, username=username)

    ulasan_all = Ulasan.objects.all()
    ulasan = ulasan_all.filter(user=user)
    restoran = Restoran.objects.filter(user=user)

    list_restoran = []
    for resto in restoran:
        bintang = 0
        banyak_ulasan = 0
        for item in ulasan_all.filter(restoran=resto):
            bintang += item.nilai
            banyak_ulasan += 1

        if banyak_ulasan == 0:
            bintang = 0
        else:
            bintang = bintang / banyak_ulasan

        list_restoran.append({
            "id": resto.id,
            "nama": resto.nama,
            "alamat": resto.alamat,
            "jam_buka": resto.jam_buka,
            "jam_tutup": resto.jam_tutup,
            "nomor_telepon": resto.nomor_telepon,
            "gambar": resto.gambar.url if resto.gambar else "",
            "rata_bintang": bintang,
        })


    return render(
        request,
        "authentication/detail_profile/index.html",
        {"profile": user, "ulasan": ulasan, "restoran": list_restoran},
    )
