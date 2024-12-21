from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from restoran.models import Restoran
from authentication.models import User
from restoran.utils import restoran_data
from datetime import datetime


@csrf_exempt
def restoran(request):
    """
    GET: Menampilkan seluruh restoran
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: -
    * Format response: List of application/json

    POST: Menambahkan restoran baru.
    - Memerlukan login
    - Hanya role `pemilik_restoran` yang memiliki akses ke method ini
    """
    if request.method == "GET":
        # Mengambil seluruh objek restoran
        restoran = Restoran.objects.all()

        # Mengembalikan data seluruh restoran
        data = []
        for r in restoran:
            data.append(restoran_data(r))
        return JsonResponse(data, safe=False, status=200)
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        if request.user.peran != "pemilik_restoran":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Ambil data dari form
        nama = request.POST.get("nama")
        alamat = request.POST.get("alamat")
        jam_buka = request.POST.get("jam_buka")
        jam_tutup = request.POST.get("jam_tutup")
        nomor_telepon = request.POST.get("nomor_telepon")
        gambar = request.FILES.get("gambar")

        # Validasi input
        if not nama or not alamat:
            return JsonResponse({"message": "Input tidak lengkap."}, status=400)

        # Convert jam_buka dan jam_tutup ke objek waktu jika berupa string
        try:
            jam_buka = datetime.strptime(jam_buka, "%H:%M").time()
            jam_tutup = datetime.strptime(jam_tutup, "%H:%M").time()
        except ValueError:
            return JsonResponse({"message": "Format waktu tidak valid."}, status=400)

        # Membuat restoran baru
        restoran = Restoran(
            nama=nama,
            alamat=alamat,
            jam_buka=jam_buka,
            jam_tutup=jam_tutup,
            nomor_telepon=nomor_telepon,
            gambar=gambar,
            user=request.user,
        )
        restoran.save()

        # Response
        data = restoran_data(restoran, "Restoran berhasil ditambahkan.")
        return JsonResponse(data, status=201)
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
        # Mencari restoran berdasarkan id
        try:
            restoran = Restoran.objects.get(pk=id_restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)

        # Mengembalikan data restoran
        data = restoran_data(restoran)
        return JsonResponse(data, status=200)
    
    elif request.method == "POST":
        # Memeriksa apakah user sudah terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memeriksa apakah user memiliki peran sebagai 'pemilik_restoran'
        if request.user.peran != "pemilik_restoran":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mengambil objek restoran berdasarkan id
        try:
            restoran = Restoran.objects.get(pk=id_restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)

        # Memeriksa apakah user yang sedang login adalah pemilik restoran
        if request.user.id != restoran.user.id:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mendapatkan data dari form data (POST)
        nama = request.POST.get("nama")
        alamat = request.POST.get("alamat")
        jam_buka = request.POST.get("jam_buka")
        jam_tutup = request.POST.get("jam_tutup")
        nomor_telepon = request.POST.get("nomor_telepon")
        gambar = request.FILES.get("gambar")

        # Validasi input
        if not nama or not alamat:
            return JsonResponse({"message": "Input tidak lengkap."}, status=400)

        # Memperbarui data restoran
        restoran.nama = nama
        restoran.alamat = alamat
        if jam_buka: restoran.jam_buka = jam_buka
        if jam_tutup: restoran.jam_tutup = jam_tutup
        if nomor_telepon: restoran.nomor_telepon = nomor_telepon
        if gambar: restoran.gambar = gambar
        restoran.save()

        # Mengembalikan response dengan data restoran yang berhasil diperbarui
        data = restoran_data(restoran, "Restoran berhasil diubah.")
        return JsonResponse(data, status=200)
    
    elif request.method == "DELETE":
        # Memeriksa apakah user sudah terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memeriksa apakah user memiliki peran sebagai 'pemilik_restoran'
        if request.user.peran != "pemilik_restoran":
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mengambil objek restoran berdasarkan id
        try:
            restoran = Restoran.objects.get(pk=id_restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)

        # Memeriksa apakah user yang sedang login adalah pemilik restoran
        if request.user.id != restoran.user.id:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Menghapus restoran
        restoran.delete()
        return JsonResponse({"message": "Restoran berhasil dihapus."}, status=200)
    
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)

def restoran_by_user(request, username):
    if request.method == "GET":
        try:
            user = User.objects.get(username=username)  # Mengambil user berdasarkan username
        except User.DoesNotExist:
            return JsonResponse({"message": "User tidak ditemukan."}, status=404)

        # Mendapatkan restoran yang dimiliki oleh user ini
        restoran = Restoran.objects.filter(user=user)

        if user.peran != "pemilik_restoran":
            return JsonResponse({"message": "User tidak memiliki restoran."}, status=404)

        data = []
        for r in restoran:
            data.append(restoran_data(r))
        return JsonResponse(data, safe=False, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)

@csrf_exempt
@require_POST
def get_user_flutter(request):
    try:
        if request.method == 'POST':
            if not request.user.is_authenticated:
                return JsonResponse({"status": "error", "message": "User is not authenticated"}, status=401)
            
            user = request.user
            
            profile_pic = user.foto.url if user.foto else ""

            return JsonResponse({
                'status': 'success',
                'id': user.id,
                'nama': user.nama,
                'username': user.username,
                'email': user.email,
                'peran': user.peran,
                'poin': user.poin,
                'deskripsi': user.deskripsi or "",
                'foto': profile_pic,
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    except:
        return JsonResponse({"status": "error"}, status=404)