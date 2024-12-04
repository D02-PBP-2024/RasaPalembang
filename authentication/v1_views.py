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
            return JsonResponse({"message": "Input tidak valid."}, status=403)
        except KeyError:
            return JsonResponse({"message": "Input tidak lengkap."}, status=403)

        # Memastikan password sesuai dengan password_konfirmasi
        if password1 != password2:
            return JsonResponse({"message": "Password tidak cocok."}, status=400)

        # Memastikan username tersedia
        if User.objects.filter(username=username).exists():
            return JsonResponse({"message": "Username sudah digunakan."}, status=400)

        # Memastikan input peran antara `pengulas` atau `pemilik_restoran`
        if peran != "pengulas" and peran != "pemilik_restoran":
            return JsonResponse({"message": "Input peran tidak valid."}, status=403)

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
        data = format_response(201, "User berhasil didaftarkan.", user_data(user))
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


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
            username = request.POST["username"]
            password = request.POST["password"]
        except KeyError:
            return JsonResponse({"message": "Input tidak lengkap."}, status=403)

        # Mengambil user dengan username=`input username` dan password=`input password`
        user = authenticate(username=username, password=password)

        # Memastikan user tersedia
        if user is None:
            return JsonResponse({"message": "Login gagal."}, status=401)

        # Memastikan user tidak dinonaktifkan
        if not user.is_active:
            return JsonResponse({"message": "User dinonaktifkan."}, status=401)

        # Memberikan user sesi
        auth_login(request, user)

        # Mengembalikan data user yang baru saja login
        data = format_response(200, "Login berhasil.", user_data(user))
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


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
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Mengembalikan data user yang baru saja logout
        data = user_data(request.user, "Logout berhasil.")

        # Menghapus sesi user
        auth_logout(request)
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


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
            return JsonResponse({"message": "User tidak ditemukan."}, status=404)

        # Mengembalikan data user berdasarkan username
        data = user_data(user)
        return JsonResponse(data, status=200)
    elif request.method == "POST":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan username user yang memiliki sesi sama dengan username pada url
        if request.user.username != username:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=401)

        # Mengambil objek user yang sedang memiliki sesi
        try:
            user = User.objects.get(pk=request.user.id)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "User tidak ditemukan."}, status=404)

        # Decode request body yang berupa multipart/form-data
        nama = request.POST.get("nama")
        deskripsi = request.POST.get("deskripsi")
        foto = request.FILES.get("foto")

        # Memastikan seluruh input lengkap kecuali foto
        if nama is None or deskripsi is None:
            return JsonResponse({"message": "Input tidak lengkap."}, status=403)

        # Mengubah data user
        user.nama = nama
        user.deskripsi = deskripsi
        if foto is not None:
            user.foto = foto
        user.save()

        # Mengembalikan data user yang telah diubah
        data = user_data(user, "User berhasil diubah.")
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)
