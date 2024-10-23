from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from minuman.models import Minuman
from minuman.forms import MinumanForm
from restoran.models import Restoran


def show_minuman(request):
    minuman = Minuman.objects.all()
    context = {"minuman": minuman}
    return render(request, "minuman/minuman_all/index.html", context)


def show_minuman_by_id(request, id):
    minuman = Minuman.objects.get(pk=id)
    context = {"minuman": minuman}
    return render(request, "minuman/minuman_by_id/index.html", context)


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
def edit_minuman(request, id):
    if request.user.peran != "pemilik_restoran":
        return HttpResponseNotFound()
    minuman = Minuman.objects.get(pk=id)
    restoran = Restoran.objects.filter(user=request.user)
    if request.method == "POST":
        form = MinumanForm(request.POST, request.FILES, instance=minuman)
        if form.is_valid():
            form.save()
            return redirect("minuman:show_minuman")
    else:
        form = MinumanForm(instance=minuman)

    context = {
        "form": form,
        "minuman": minuman,
        "restoran": restoran,
    }
    return render(request, "minuman/edit/index.html", context)


@login_required(login_url="login")
def delete_minuman(request, id):
    if request.user.peran != "pemilik_restoran":
        return HttpResponseNotFound()
    minuman = Minuman.objects.get(pk=id)
    minuman.delete()
    return redirect("minuman:show_minuman")
