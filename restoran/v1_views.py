import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from minuman.models import Minuman
from restoran.models import Restoran


@csrf_exempt
def minuman_by_restoran(request, id):
    if request.method == "GET":
        try:
            restoran = Restoran.objects.get(pk=id)
            minuman = Minuman.objects.filter(restoran=restoran)
            data = serialize("json", minuman)
            return HttpResponse(data, content_type="application/json", status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"Message": "Restoran Not Found"}, status=404)
    elif request.method == "POST":
        try:
            # TODO (untuk syauqi): Validasi pemillik restoran yang dapat menambah
            restoran = Restoran.objects.get(pk=id)
            data = json.loads(request.body)
            minuman = Minuman.objects.create(
                restoran=restoran,
                nama=data["nama"],
                harga=int(data["harga"]),
                deskripsi=data["deskripsi"],
                # TODO (untuk syauqi): Data gambar mungkin berpotensi error (Ditambah sebagai String)
                gambar=data["gambar"],
                ukuran=data["ukuran"],
                tingkat_kemanisan=int(data["tingkat_kemanisan"]),
            )
            minuman.save()
            return JsonResponse({"Message": "Minuman Created Successfully"}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"Message": "Restoran Not Found"}, status=404)
    else:
        return JsonResponse({"Message": "Restoran Not Found"}, status=404)
