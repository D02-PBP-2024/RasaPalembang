from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from makanan.models import Kategori, Makanan
from makanan.utils import makanan_data, validasi_input
from restoran.models import Restoran


@csrf_exempt
def makanan(request):
    """
    GET: Menampilkan seluruh makanan
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: -
    * Format response: List of application/json
    """
    if request.method == "GET":
        # Mengambil seluruh objek makanan
        makanan = Makanan.objects.all()

        # Mengembalikan data seluruh makanan
        data = []
        for m in makanan:
            data.append(makanan_data(m))
        return JsonResponse(data, safe=False, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


@csrf_exempt
def makanan_by_id(request, id_makanan):
    """
    GET: Menampilkan makanan berdasarkan id
    - Tidak memerlukan login
    - Semua role memiliki hak askes ke method ini
    * Format request: -
    * Format response: application/json

    POST: Mengubah makanan menggunakan multipart/form-data
    - Memerlukan login
    - Hanya role `pemilik_restoran` dan `si pemilik makanan` yang memiliki akses ke method ini
    * Format request: multipart/form-data
    * Format response: application/json

    DELETE: Menghapus makanan
    - Memerlukan login
    - Hanya role `pemilik_restoran` dan `si pemilik makanan` yang memiliki akses ke method ini
    * Format request: -
    * Format response: application/json
    """
    
    if request.method == "GET":
        # Mengambil objek makanan berdasarkan id
        try:
            makanan = Makanan.objects.get(pk=id_makanan)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "makanan tidak ditemukan."}, status=404)

        # Mengembalikan data makanan berdasarkan id
        data = makanan_data(makanan)
        return JsonResponse(data, status=200)
    elif request.method == "POST":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pemilik_restoran`
        if request.user.peran != "pemilik_restoran":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mengambil objek makanan berdasarkan id dan restoran yang memiliki makanan tersebut
        try:
            makanan = Makanan.objects.get(pk=id_makanan)
            restoran = Restoran.objects.get(pk=makanan.restoran.id)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "makanan tidak ditemukan."}, status=404)

        # Memastikan user adalah `si pemilik makanan`
        if request.user.id != restoran.user.id:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Decode request body yang berupa multipart/form-data
        nama = request.POST.get("nama")
        harga = request.POST.get("harga")
        deskripsi = request.POST.get("deskripsi")
        gambar = request.FILES.get("gambar")
        kalori = request.POST.get("kalori")
        kategori_ids = request.POST.getlist("kategori")

        # Memastikan seluruh input lengkap kecuali gambar
        if (nama is None
                or harga is None
                or deskripsi is None
                or kalori is None
                or kategori_ids is None):
            return JsonResponse({"message": "Input tidak lengkap."}, status=400)

        # Memastikan input harga dan kalori
        message = validasi_input(harga, kalori)

        if message != "":
            return JsonResponse({"message": f"Input {message} tidak valid."}, status=400)

        # Mengubah data makanan
        makanan.nama = nama
        makanan.harga = int(harga)
        makanan.deskripsi = deskripsi
        if gambar is not None:
            makanan.gambar = gambar
        makanan.kalori = kalori

        kategori_objects = Kategori.objects.filter(pk__in=kategori_ids)
        makanan.kategori.set(kategori_objects)  # Mengaitkan kategori dengan makanan

        makanan.save()

        # Mengembalikan data makanan yang telah diubah
        data = makanan_data(makanan, "Makanan berhasil diubah.")
        return JsonResponse(data, status=200)
    elif request.method == "DELETE":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pemilik_restoran`
        if request.user.peran != "pemilik_restoran":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mengambil objek makanan berdasarkan id dan restoran yang memiliki makanan tersebut
        try:
            makanan = Makanan.objects.get(pk=id_makanan)
            restoran = Restoran.objects.get(pk=makanan.restoran.id)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "makanan tidak ditemukan."}, status=404)

        # Memastikan user adalah `si pemilik makanan`
        if request.user != restoran.user:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mengembalikan data makanan yang akan dihapus
        data = makanan_data(makanan, "makanan berhasil dihapus.")

        # Menghapus makanan
        makanan.delete()
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)

@csrf_exempt
def makanan_by_restoran(request, id_restoran):
    """
    GET: Menampilkan makanan yang dimiliki oleh sebuah restoran
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: -
    * Format response: List of application/json

    POST: Menambahkan makanan ke sebuah restoran
    - Memerlukan login
    - Hanya role `pemilik_restoran` dan `si pemilik makanan` yang memiliki akses ke method ini
    * Format request: multipart/form-data
    * Format response: application/json

    DELETE: Menghapus makanan
    - Memerlukan login
    - Hanya role `pemilik_restoran` dan `si pemilik makanan` yang memiliki akses ke method ini
    * Format request: -
    * Format response: application/json
    
    """

    if request.method == "GET":
        # Mengambil objek restoran berdasarkan id dan makanan yang dimiliki oleh restoran tersebut
        try:
            restoran = Restoran.objects.get(pk=id_restoran)
            makanan = Makanan.objects.filter(restoran=restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)

        # Mengembalikan data seluruh makanan di sebuah restoran
        data = []
        for m in makanan:
            data.append(makanan_data(m))
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

        # Memastikan user adalah `si pemilik makanan`
        if request.user.id != restoran.user.id:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Decode request body yang berupa multipart/form-data
        nama = request.POST.get("nama")
        harga = request.POST.get("harga")
        deskripsi = request.POST.get("deskripsi")
        gambar = request.FILES.get("gambar")
        kalori = request.POST.get("kalori")
        kategori_ids = request.POST.getlist("kategori")
        restoran = restoran

        # Memastikan seluruh input lengkap
        if (nama is None
                or harga is None
                or deskripsi is None
                or gambar is None
                or kalori is None
                or kategori_ids is None):
            return JsonResponse({"message": "Input tidak lengkap."}, status=400)

        # Memastikan input harga, tingkat_kemanisan, dan ukuran valid
        message = validasi_input(harga, kalori)

        if message != "":
            return JsonResponse({"message": f"Input {message} tidak valid."}, status=400)

        kategori_objects = Kategori.objects.filter(id__in=kategori_ids)

        # Menambahkan makanan baru
        makanan = Makanan.objects.create(
            nama=nama,
            harga=int(harga),
            deskripsi=deskripsi,
            gambar=gambar,
            kalori=kalori,
            restoran=restoran,
        )

        makanan.kategori.set(kategori_objects)
        makanan.save()

        # Mengembalikan data makanan yang telah ditambahkan
        data = makanan_data(makanan, "Berhasil menambah makanan.")
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)
    


