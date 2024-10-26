from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from minuman.forms import MinumanForm
from restoran.models import Restoran
from minuman.models import Minuman


def show_minuman(request):
    minuman = Minuman.objects.all()

    return render(request, "minuman/show/index.html", {"minuman": minuman})


def detail_minuman(request, id):
    minuman = Minuman.objects.get(pk=id)
    restoran = Restoran.objects.get(pk=minuman.restoran.id)
    mengubah = restoran.user == request.user

    return render(
        request,
        "minuman/detail/index.html",
        {
            "minuman": minuman,
            "restoran": restoran,
            "mengubah": mengubah,
        },
    )


@login_required(login_url="login")
def tambah_minuman(request):
    if request.user.peran != "pemilik_restoran":
        return HttpResponseNotFound()
    restoran = Restoran.objects.filter(user=request.user)
    if request.method == "POST":
        form = MinumanForm(request.POST, request.FILES)
        if form.is_valid():
            minuman = form.save(commit=False)
            minuman.save()
            return redirect("minuman:show_minuman")
    else:
        form = MinumanForm()

    context = {
        "form": form,
        "restoran": restoran,
    }
    return render(request, "minuman/tambah/index.html", context)


@login_required(login_url="login")
def ubah_minuman(request, id):
    minuman = Minuman.objects.get(pk=id)
    restoran = Restoran.objects.filter(user=request.user)

    if request.user.peran != "pemilik_restoran":
        return HttpResponseNotFound()
    elif minuman.restoran not in restoran:
        return HttpResponseNotFound()

    if request.method == "POST":
        form = MinumanForm(request.POST, request.FILES, instance=minuman)
        if form.is_valid():
            form.save()
            return redirect("minuman:detail_minuman", id=id)
    else:
        form = MinumanForm(instance=minuman)

    context = {
        "form": form,
        "minuman": minuman,
        "restoran": restoran,
    }
    return render(request, "minuman/ubah/index.html", context)


@login_required(login_url="login")
def hapus_minuman(request, id):
    minuman = Minuman.objects.get(pk=id)
    restoran = Restoran.objects.filter(user=request.user)

    if request.user.peran != "pemilik_restoran":
        return HttpResponseNotFound()
    elif minuman.restoran not in restoran:
        return HttpResponseNotFound()

    minuman.delete()
    return redirect("minuman:show_minuman")


def show_minuman_by_sort(request):
    order = request.GET.get("order", None)

    if order == "termurah":
        minuman = Minuman.objects.all().order_by("harga")
    elif order == "termahal":
        minuman = Minuman.objects.all().order_by("-harga")
    else:
        minuman = Minuman.objects.all()

    minuman_all = []
    for item in minuman:
        minuman_all.append(
            {
                "id": item.id,
                "nama": item.nama,
                "harga": item.harga,
                "restoran": item.restoran.nama,
                "gambar": item.gambar.url,
            }
        )

    return JsonResponse({"minuman": minuman_all})
