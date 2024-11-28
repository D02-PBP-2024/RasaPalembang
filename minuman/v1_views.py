import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from minuman.models import Minuman


@csrf_exempt
def minuman(request):
    if request.method == "GET":
        minuman = Minuman.objects.all()
        data = serialize("json", minuman)
        return HttpResponse(data, content_type="application/json", status=200)
    else:
        return HttpResponse(status=405)


@csrf_exempt
def minuman_by_id(request, id):
    if request.method == "GET":
        try:
            minuman = Minuman.objects.get(pk=id)
            data = serialize("json", [minuman])
            return HttpResponse(data, content_type="application/json", status=200)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
    elif request.method == "PUT":
        try:
            minuman = Minuman.objects.get(pk=id)
            # TODO: Validasi pemillik minuman yang dapat mengedit
            data = json.loads(request.body)
            minuman.nama = data["nama"]
            minuman.harga = int(data["harga"])
            minuman.deskripsi = data["deskripsi"]
            # TODO: Data gambar mungkin berpotensi error (Diupdate menjadi String)
            minuman.gambar = data["gambar"]
            minuman.ukuran = data["ukuran"]
            minuman.tingkat_kemanisan = int(data["tingkat_kemanisan"])
            minuman.save()
            data = serialize("json", [minuman])
            return HttpResponse(data, content_type="application/json", status=200)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
    elif request.method == "DELETE":
        try:
            minuman = Minuman.objects.get(pk=id)
            # TODO: Validasi pemillik minuman yang dapat menghapus
            minuman.delete()
            return HttpResponse(status=200)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=405)
