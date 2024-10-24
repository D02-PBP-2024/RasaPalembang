from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from restoran.models import Restoran
from django.http import JsonResponse
from ulasan.forms import UlasanForm
from ulasan.models import Ulasan


def ulasan(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    ulasan = Ulasan.objects.filter(restoran=restoran).select_related("user")

    ulasan_data = []
    for u in ulasan:
        ulasan_data.append(
            {
                "id": u.id,
                "created_at": u.created_at,
                "nilai": u.nilai,
                "deskripsi": u.deskripsi,
                "user": {
                    "id": u.user.id,
                    "username": u.user.username,
                    "nama": u.user.nama,
                    "foto": u.user.foto.url if u.user.foto else "/static/images/avatar.png",
                    "poin": u.user.poin,
                },
            }
        )

    return JsonResponse(ulasan_data, safe=False)


@login_required(login_url="/login")
def tambah_ulasan(request, id):
    nilai = request.POST.get("nilai")
    deskripsi = strip_tags(request.POST.get("deskripsi"))
    user = request.user
    restoran = restoran = get_object_or_404(Restoran, id=id)

    ulasan = Ulasan(
        nilai=nilai,
        deskripsi=deskripsi,
        user=user,
        restoran=restoran,
    )
    ulasan.save()

    user.poin += 5
    user.save()

    return HttpResponse(b"Berhasil menambah ulasan.", status=201)


@login_required(login_url="/login")
def ubah_ulasan(request, id):
    if request.method == "POST":
        restoran = get_object_or_404(Restoran, id=id)
        ulasan = get_object_or_404(Ulasan, user=request.user, restoran=restoran)
        form = UlasanForm(request.POST, instance=ulasan)
        if form.is_valid():
            form.save()
            return HttpResponse(b"UPDATED", status=200)


@login_required(login_url="/login")
def hapus_ulasan(request, id):
    restoran = get_object_or_404(Restoran, id=id)
    ulasan = get_object_or_404(Ulasan, user=request.user, restoran=restoran)
    ulasan.delete()
    return HttpResponseRedirect("/restoran/" + str(id) + "/")
