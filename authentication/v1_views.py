import json
from authentication.models import User
from authentication.utils import format_response, user_data
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register(request):
    """
    POST: Mendaftarkan user baru
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: application/json
    * Format response: application/json
    """
    if request.method == "POST":
        # Decode request body yang berupa application/json
        try:
            data = json.loads(request.body)
            nama = data["nama"]
            username = data["username"]
            password1 = data["password1"]
            password2 = data["password2"]
            peran = data["peran"]
        except json.JSONDecodeError:
            return JsonResponse(
                format_response(False, "Input tidak valid."), status=403
            )
        except KeyError:
            return JsonResponse(
                format_response(False, "Input tidak lengkap."), status=403
            )

        # Memastikan password sesuai dengan password_konfirmasi
        if password1 != password2:
            return JsonResponse(
                format_response(False, "Password tidak cocok."), status=400
            )

        # Memastikan username tersedia
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                format_response(False, "Username sudah digunakan."), status=400
            )

        # Memastikan input peran antara `pengulas` atau `pemilik_restoran`
        if peran != "pengulas" and peran != "pemilik_restoran":
            return JsonResponse(
                format_response(False, "Input peran tidak valid."), status=403
            )

        # Menambahkan user baru
        user = User.objects.create(
            nama=nama,
            username=username,
            peran=peran,
        )
        user.set_password(password1)
        user.save()

        # Memberikan user baru sesi
        auth_login(request, user)

        # Mengembalikan data user yang baru didaftarkan
        return JsonResponse(
            format_response(True, "User berhasil didaftarkan.", user_data(user)),
            status=201,
        )
    else:
        return JsonResponse(
            format_response(False, "Method tidak diizinkan."), status=405
        )


@csrf_exempt
def login(request):
    """
    POST: Login user
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: application/json
    * Format response: application/json
    """
    if request.method == "POST":
        # Decode request body yang berupa application/json
        try:
            data = json.loads(request.body)
            username = data["username"]
            password = data["password"]
        except json.JSONDecodeError:
            return JsonResponse(
                format_response(False, "Input tidak valid."), status=403
            )
        except KeyError:
            return JsonResponse(
                format_response(False, "Input tidak lengkap."), status=403
            )

        # Mengambil user dengan username=`input username` dan password=`input password`
        user = authenticate(username=username, password=password)

        # Memastikan user tersedia
        if user is None:
            return JsonResponse(format_response(False, "Login gagal."), status=401)

        # Memastikan user tidak dinonaktifkan
        if not user.is_active:
            return JsonResponse(
                format_response(False, "User dinonaktifkan."), status=401
            )

        # Memberikan user sesi
        auth_login(request, user)

        # Mengembalikan data user yang baru saja login
        data = format_response(True, "Login berhasil.", user_data(user))
        return JsonResponse(data, status=200)
    else:
        return JsonResponse(
            format_response(False, "Method tidak diizinkan."), status=405
        )


@csrf_exempt
def logout(request):
    """
    POST: Logout user
    - Memerlukan login
    - `pengulas` dan `pemilik_restoran` memiliki hak akses ke method ini
    * Format request: -
    * Format response: application/json
    """
    if request.method == "POST":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse(
                format_response(False, "User tidak terautentikasi."), status=401
            )

        # Mengembalikan data user yang baru saja logout
        data = format_response(True, "Logout berhasil.", user_data(request.user))

        # Menghapus sesi user
        auth_logout(request)
        return JsonResponse(data, status=200)
    else:
        return JsonResponse(
            format_response(False, "Method tidak diizinkan."), status=405
        )


@csrf_exempt
def profile_by_username(request, username):
    """
    GET: Menampilkan profile seorang user
    - Tidak memerlukan login
    - Semua role memiliki hak akses ke method ini
    * Format request: -
    * Format response: application/json

    POST:
    - Memerlukan login
    - `pengulas` dan `pemilik_restoran` memiliki hak akses ke method ini
    * Format request: multipart/form-data
    * Format response: application/json
    """
    if request.method == "GET":
        # Mengambil objek user dengan username sama dengan username pada url
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return JsonResponse(
                format_response(False, "User tidak ditemukan."), status=404
            )

        ulasan = None
        restoran = None
        if user.peran == "pengulas":
            # Mengambil ulasan yang ditulis oleh user
            ulasan = [
                {
                    "pk": u.pk,
                    "restoran": u.restoran.nama,
                    "nilai": u.nilai,
                    "deskripsi": u.deskripsi,
                    "created_at": u.created_at,
                }
                for u in user.ulasan_set.all()
            ]
        elif user.peran == "pemilik_restoran":
            # Mengambil restoran yang dimiliki oleh user
            restoran = [
                {
                    "pk": r.pk,
                    "nama": r.nama,
                    "jam_buka": r.jam_buka.strftime("%H:%M"),
                    "jam_tutup": r.jam_tutup.strftime("%H:%M"),
                }
                for r in user.restoran_set.all()
            ]

        # Mengembalikan data user berdasarkan username
        data = format_response(
            True, "Berhasil mendapatkan data user.", user_data(user, ulasan, restoran)
        )
        return JsonResponse(data, status=200)
    elif request.method == "POST":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse(
                format_response(False, "User tidak terautentikasi."), status=401
            )

        # Memastikan username user yang memiliki sesi sama dengan username pada url
        if request.user.username != username:
            return JsonResponse(
                format_response(False, "Tindakan tidak diizinkan."), status=401
            )

        # Mengambil objek user yang sedang memiliki sesi
        try:
            user = User.objects.get(pk=request.user.id)
        except ObjectDoesNotExist:
            return JsonResponse(
                format_response(False, "User tidak ditemukan."), status=404
            )

        # Decode request body yang berupa multipart/form-data
        nama = request.POST.get("nama")
        deskripsi = request.POST.get("deskripsi")
        foto = request.FILES.get("foto")

        # Memastikan seluruh input lengkap kecuali foto
        if nama is None or deskripsi is None:
            return JsonResponse(
                format_response(False, "Input tidak lengkap."), status=403
            )

        # Mengubah data user
        user.nama = nama
        user.deskripsi = deskripsi
        if foto is not None:
            user.foto = foto
        user.save()

        # Mengembalikan data user yang telah diubah
        data = format_response(True, "User berhasil diubah.", user_data(user))
        return JsonResponse(data, status=200)
    else:
        return JsonResponse(
            format_response(False, "Method tidak diizinkan."), status=405
        )
