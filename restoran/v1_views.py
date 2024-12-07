import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from minuman.models import Minuman
from minuman.utils import minuman_data, validasi_input
from forum.models import Forum
from favorit.models import Favorit
from favorit.utils import favorit_data
from restoran.views import show_restoran
from forum.utils import forum_data
from restoran.models import Restoran


@csrf_exempt
def minuman_by_restoran(request, id_restoran):
    """
    GET: Menampilkan minuman yang dimiliki oleh sebuah restoran
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: -
    * Format response: List of application/json

    POST: Menambahkan minuman ke sebuah restoran
    - Memerlukan login
    - Hanya role `pemilik_restoran` dan `si pemilik minuman` yang memiliki akses ke method ini
    * Format request: multipart/form-data
    * Format response: application/json
    """
    if request.method == "GET":
        # Mengambil objek restoran berdasarkan id dan minuman yang dimiliki oleh restoran tersebut
        try:
            restoran = Restoran.objects.get(pk=id_restoran)
            minuman = Minuman.objects.filter(restoran=restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)

        # Mengembalikan data seluruh minuman di sebuah restoran
        data = []
        for m in minuman:
            data.append(minuman_data(m))
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

        # Memastikan user adalah `si pemilik minuman`
        if request.user.id != restoran.user.id:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Decode request body yang berupa multipart/form-data
        nama = request.POST.get("nama")
        harga = request.POST.get("harga")
        deskripsi = request.POST.get("deskripsi")
        gambar = request.FILES.get("gambar")
        ukuran = request.POST.get("ukuran")
        tingkat_kemanisan = request.POST.get("tingkat_kemanisan")
        restoran = restoran

        # Memastikan seluruh input lengkap
        if (nama is None
                or harga is None
                or deskripsi is None
                or gambar is None
                or ukuran is None
                or tingkat_kemanisan is None):
            return JsonResponse({"message": "Input tidak lengkap."}, status=400)

        # Memastikan input harga, tingkat_kemanisan, dan ukuran valid
        message = validasi_input(harga, ukuran, tingkat_kemanisan)

        if message != "":
            return JsonResponse({"message": f"Input {message} tidak valid."}, status=400)

        # Menambahkan minuman baru
        minuman = Minuman.objects.create(
            nama=nama,
            harga=int(harga),
            deskripsi=deskripsi,
            gambar=gambar,
            ukuran=ukuran,
            tingkat_kemanisan=int(tingkat_kemanisan),
            restoran=restoran,
        )
        minuman.save()

        # Mengembalikan data minuman yang telah ditambahkan
        data = minuman_data(minuman, "Berhasil menambah minuman.")
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


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


@csrf_exempt
def favorit_by_restoran(request, id_restoran):
    if request.method == "POST":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pemilik_restoran`
        if request.user.peran != "pemilik_restoran":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)
        
        # Memastikan peran user adalah `pengulas`
        if request.user.peran != "pengulas":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mengambil objek restoran berdasarkan id
        try:
            restoran = Restoran.objects.get(pk=id_restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)
        
        # Mengembalikan data restoran yang telah ditambahkan
        data = show_restoran(restoran, "Berhasil menambah restoran.")
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)