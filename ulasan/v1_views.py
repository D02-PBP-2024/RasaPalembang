from django.core.exceptions import ObjectDoesNotExist
from authentication.models import User
from restoran.models import Restoran
from ulasan.utils import ulasan_data, validasi_input
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ulasan.models import Ulasan


@csrf_exempt
def ulasan_by_id(request, id_ulasan):
    """
    POST: Mengubah ulasan menggunakan multipart/form-data
    - Memerlukan login
    - Hanya role `pengulas` yang memiliki akses ke method ini
    * Format request: multipart/form-data
    * Format response: application/json

    DELETE: Menghapus ulasan
    - Memerlukan login
    - Hanya role `pengulas` yang memiliki akses ke method ini
    * Format request: -
    * Format response: application/json
    """
    if request.method == "POST":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pengulas`
        if request.user.peran != "pengulas":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mengambil objek ulasan berdasarkan id
        try:
            ulasan = Ulasan.objects.get(pk=id_ulasan)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Ulasan tidak ditemukan."}, status=404)

        # Memastikan user adalah `si pemilik ulasan`
        if request.user.id != ulasan.user.id:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Decode request body yang berupa multipart/form-data
        nilai = request.POST.get("nilai")
        deskripsi = request.POST.get("deskripsi")

        # Memastikan seluruh input lengkap kecuali gambar
        if nilai is None or deskripsi is None:
            return JsonResponse({"message": "Input tidak lengkap."}, status=400)

        # Memastikan input harga, tingkat_kemanisan, dan ukuran valid
        message = validasi_input(nilai)

        if message != "":
            return JsonResponse(
                {"message": f"Input {message} tidak valid."}, status=400
            )

        # Mengubah data ulasan
        ulasan.nilai = nilai
        ulasan.deskripsi = deskripsi
        ulasan.save()

        # Mengembalikan data ulasan yang telah diubah
        data = ulasan_data(ulasan, "Ulasan berhasil diubah.")
        return JsonResponse(data, status=200)
    elif request.method == "DELETE":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pengulas`
        if request.user.peran != "pengulas":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mengambil objek ulasan berdasarkan id yang memiliki ulasan tersebut
        try:
            ulasan = Ulasan.objects.get(pk=id_ulasan)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Ulasan tidak ditemukan."}, status=404)

        # Memastikan user adalah `si pemilik ulasan`
        if request.user != ulasan.user:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mengembalikan data ulasan yang akan dihapus
        data = ulasan_data(ulasan, "Ulasan berhasil dihapus.")

        # Menghapus ulasan
        ulasan.delete()
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


@csrf_exempt
def ulasan_by_restoran(request, id_restoran):
    """
    GET: Menampilkan ulasan berdasarkan restoran
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: -
    * Format response: application/json

    POST: Menambahkan ulasan
    - Memerlukan login
    - Hanya role `pengulas` yang memiliki akses ke method ini
    * Format request: application/json
    * Format response: application/json
    """

    if request.method == "GET":
        # Mengambil objek restoran berdasarkan id dan ulasan yang dimiliki oleh restoran tersebut
        try:
            restoran = Restoran.objects.get(pk=id_restoran)
            ulasan = Ulasan.objects.filter(restoran=restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)

        # Mengembalikan data seluruh ulasan di sebuah restoran
        data = []
        for m in ulasan:
            data.append(ulasan_data(m))
        return JsonResponse(data, safe=False, status=200)
    elif request.method == "POST":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pemilik_restoran`
        if request.user.peran != "pemilik_restoran":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mengambil objek restoran berdasarkan id
        try:
            restoran = Restoran.objects.get(pk=id_restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)

        # Memastikan user adalah `si pemilik ulasan`
        if request.user.id != restoran.user.id:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Decode request body yang berupa multipart/form-data
        nilai = request.POST.get("nilai")
        deskripsi = request.POST.get("deskripsi")
        restoran = restoran

        # Memastikan seluruh input lengkap
        if nilai is None or deskripsi is None:
            return JsonResponse({"message": "Input tidak lengkap."}, status=400)

        # Memastikan input harga, tingkat_kemanisan, dan ukuran valid
        message = validasi_input(nilai)

        if message != "":
            return JsonResponse(
                {"message": f"Input {message} tidak valid."}, status=400
            )

        # Menambahkan ulasan baru
        ulasan = Ulasan.objects.create(
            nilai=nilai,
            deskripsi=deskripsi,
            restoran=restoran,
            user=request.user,
        )
        ulasan.save()

        # Mengembalikan data ulasan yang telah ditambahkan
        data = ulasan_data(ulasan, "Berhasil menambah ulasan.")
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)
