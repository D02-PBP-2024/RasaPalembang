import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from forum.models import Forum
from forum.utils import forum_data
from restoran.models import Restoran


@csrf_exempt
def forum_by_restoran(request, id_restoran):
    """
    GET: Menampilkan forum yang dimiliki oleh sebuah restoran
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: -
    * Format response: List of application/json

    POST: Menambahkan forum ke sebuah restoran
    - Memerlukan login
    - Hanya role `pengulas` yang memiliki akses ke method ini
    * Format request: application/json
    * Format response: application/json
    """
    if request.method == "GET":
        try:
            restoran = Restoran.objects.get(pk=id_restoran)
            forum = Forum.objects.filter(restoran=restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)
        
        # Mengembalikan data seluruh forum dari sebuah restoran
        data = []
        for f in forum:
            data.append(forum_data(f))
        return JsonResponse(data, safe=False, status=200)
    elif request.method == "POST":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pengulas`
        if request.user.peran != "pengulas":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)
        
        # Mengambil objek restoran berdasarkan id
        try:
            restoran = Restoran.objects.get(pk=id_restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)
        
        try:
            data = json.loads(request.body)
            topik = data["topik"]
            pesan = data["pesan"]
        except json.JSONDecodeError:
            return JsonResponse({"message": "Input tidak valid."}, status=403)
        except KeyError:
            return JsonResponse({"message": "Input tidak lengkap."}, status=403)
        
        forum = Forum.objects.create(
            topik=topik,
            pesan=pesan,
            restoran=restoran,
            user=request.user,
        )
        forum.save()
        data = forum_data(forum, "Berhasil menambah forum.")
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)
