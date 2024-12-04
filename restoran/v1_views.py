from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from restoran.models import Restoran
from authentication.models import User
from restoran.utils import restoran_data, validasi_input


@csrf_exempt
def restoran(request):
    """
    GET: Menampilkan seluruh restoran
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: -
    * Format response: List of application/json
    """
    if request.method == "GET":
        # Mengambil seluruh objek restoran
        restoran = Restoran.objects.all()

        # Mengembalikan data seluruh restoran
        data = [restoran_data(r) for r in restoran]
        return JsonResponse(data, safe=False, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


@csrf_exempt
def restoran_by_id(request, id_restoran):
    """
    GET: Menampilkan restoran berdasarkan id
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: -
    * Format response: application/json

    POST: Mengubah restoran menggunakan multipart/form-data
    - Memerlukan login
    - Hanya role `pemilik_restoran` yang memiliki akses ke method ini
    * Format request: multipart/form-data
    * Format response: application/json

    DELETE: Menghapus restoran
    - Memerlukan login
    - Hanya role `pemilik_restoran` yang memiliki akses ke method ini
    * Format request: -
    * Format response: application/json
    """
    if request.method == "GET":
        try:
            restoran = Restoran.objects.get(pk=id_restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)

        data = restoran_data(restoran)
        return JsonResponse(data, status=200)
    
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        if request.user.peran != "pemilik_restoran":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        try:
            restoran = Restoran.objects.get(pk=id_restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)

        if request.user.id != restoran.user.id:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Decode request body yang berupa multipart/form-data
        nama = request.POST.get("nama")
        alamat = request.POST.get("alamat")
        jam_buka = request.POST.get("jam_buka")
        jam_tutup = request.POST.get("jam_tutup")
        nomor_telepon = request.POST.get("nomor_telepon")
        gambar = request.FILES.get("gambar")

        # Validasi input
        if not nama or not alamat:
            return JsonResponse({"message": "Input tidak lengkap."}, status=400)

        restoran.nama = nama
        restoran.alamat = alamat
        if jam_buka: restoran.jam_buka = jam_buka
        if jam_tutup: restoran.jam_tutup = jam_tutup
        if nomor_telepon: restoran.nomor_telepon = nomor_telepon
        if gambar: restoran.gambar = gambar
        restoran.save()

        data = restoran_data(restoran, "Restoran berhasil diubah.")
        return JsonResponse(data, status=200)
    
    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        if request.user.peran != "pemilik_restoran":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        try:
            restoran = Restoran.objects.get(pk=id_restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)

        if request.user.id != restoran.user.id:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        restoran.delete()
        return JsonResponse({"message": "Restoran berhasil dihapus."}, status=200)
    
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


@csrf_exempt
def restoran_by_user(request, username):
    """
    GET: Menampilkan restoran berdasarkan username
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: -
    * Format response: application/json
    """
    if request.method == "GET":
        try:
            user = User.objects.get(username=username)
            restoran = Restoran.objects.filter(user=user)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)

        data = [restoran_data(r) for r in restoran]
        return JsonResponse(data, safe=False, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)
