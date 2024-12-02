import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from forum.models import Forum, Balasan
from forum.utils import forum_data, balasan_data


@csrf_exempt
def forum_by_id(request, id_forum):
    """
    GET: Menampilkan forum berdasarkan id
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: -
    * Format response: application/json

    PUT: Mengubah forum menggunakan application/json
    - Memerlukan login
    - Hanya role `pengulas` dan `si pemilik forum` yang memiliki akses ke method ini
    * Format request: application/json
    * Format response: application/json

    DELETE: Menghapus forum
    - Memerlukan login
    - Hanya role `pengulas` dan `si pemilik forum` yang memiliki akses ke method ini
    * Format request: -
    * Format response: application/json
    """
    if request.method == "GET":
        try:
            forum = Forum.objects.get(pk=id_forum)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Forum tidak ditemukan."}, status=404)
        
        data = forum_data(forum)
        return JsonResponse(data, status=200)
    elif request.method == "PUT":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pengulas`
        if request.user.peran != "pengulas":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)
        
        try:
            forum = Forum.objects.get(pk=id_forum)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Forum tidak ditemukan."}, status=404)
        
        try:
            data = json.loads(request.body)
            topik = data["topik"]
            pesan = data["pesan"]

        except json.JSONDecodeError:
            return JsonResponse({"message": "Input tidak valid."}, status=403)
        except KeyError:
            return JsonResponse({"message": "Input tidak lengkap."}, status=403)
        
        # Memastikan user adalah `si pemilik forum`
        if request.user != forum.user:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)
        
        forum.topik = topik
        forum.pesan = pesan
        forum.save()
        data = forum_data(forum, "Forum berhasil diubah.")
        return JsonResponse(data, status=200)
    elif request.method == "DELETE":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pengulas`
        if request.user.peran != "pengulas":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mengambil objek forum berdasarkan id
        try:
            forum = Forum.objects.get(pk=id_forum)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Forum tidak ditemukan."}, status=404)

        # Memastikan user adalah `si pemilik forum`
        if request.user != forum.user:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mengembalikan data forum yang akan dihapus
        data = forum_data(forum, "Forum berhasil dihapus.")

        # Menghapus forum
        forum.delete()
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)
    

@csrf_exempt
def balasan_forum(request, id_forum):
    """
    GET: Menampilkan balasan berdasarkan id
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: -
    * Format response: application/json

    POST: Menambah balasan menggunakan application/json
    - Memerlukan login
    - Hanya role `pengulas` dan `pemilik_restoran` yang memiliki akses ke method ini
    * Format request: application/json
    * Format response: application/json
    """
    if request.method == "GET":
        try:
            forum = Forum.objects.get(pk=id_forum)
            balasan = Balasan.objects.filter(forum=forum)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Forum tidak ditemukan."}, status=404)
        
        # Mengembalikan data seluruh balasan dari sebuah forum
        data = []
        for b in balasan:
            data.append(balasan_data(b))
        return JsonResponse(data, safe=False, status=200)
    elif request.method == "POST":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pemilik_restoran` atau `pengulas`
        if request.user.peran != "pemilik_restoran" and request.user.peran != "pengulas":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)
        
        # Mengambil objek forum berdasarkan id
        try:
            forum = Forum.objects.get(pk=id_forum)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Forum tidak ditemukan."}, status=404)
        
        try:
            data = json.loads(request.body)
            pesan = data["pesan"]
        except json.JSONDecodeError:
            return JsonResponse({"message": "Input tidak valid."}, status=403)
        except KeyError:
            return JsonResponse({"message": "Input tidak lengkap."}, status=403)
        
        balasan = Balasan.objects.create(
            pesan=pesan,
            forum=forum,
            user=request.user,
        )
        balasan.save()
        data = balasan_data(balasan, "Berhasil menambah balasan.")
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


@csrf_exempt
def balasan_by_id(request, id_balasan):
    """
    PUT: Mengubah balasan menggunakan application/json
    - Memerlukan login
    - Hanya role `pengulas` atau `pemilik_restoran`, serta `si pemilik balasan` yang memiliki akses ke method ini
    * Format request: application/json
    * Format response: application/json

    DELETE: Menghapus balasan
    - Memerlukan login
    - Hanya role `pengulas` atau `pemilik_restoran`, serta `si pemilik balasan` yang memiliki akses ke method ini
    * Format request: -
    * Format response: application/json
    """
    if request.method == "PUT":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pemilik_restoran` atau `pengulas`
        if request.user.peran != "pemilik_restoran" and request.user.peran != "pengulas":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)
        
        try:
            balasan = Balasan.objects.get(pk=id_balasan)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Balasan tidak ditemukan."}, status=404)
        
        # Memastikan user adalah `si pemilik balasan`
        if request.user != balasan.user:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)
        
        try:
            data = json.loads(request.body)
            pesan = data["pesan"]
        except json.JSONDecodeError:
            return JsonResponse({"message": "Input tidak valid."}, status=403)
        except KeyError:
            return JsonResponse({"message": "Input tidak lengkap."}, status=403)
        
        balasan.pesan = pesan
        balasan.save()
        data = balasan_data(balasan, "Balasan berhasil diubah.")
        return JsonResponse(data, status=200)
    elif request.method == "DELETE":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pemilik_restoran` atau `pengulas`
        if request.user.peran != "pemilik_restoran" and request.user.peran != "pengulas":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        try:
            balasan = Balasan.objects.get(pk=id_balasan)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Balasan tidak ditemukan."}, status=404)
        
        # Memastikan user adalah `si pemilik balasan`
        if request.user != balasan.user:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)
        
        # Mengembalikan data balasan yang akan dihapus
        data = balasan_data(balasan, "Balasan berhasil dihapus.")

        balasan.delete()
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)
    