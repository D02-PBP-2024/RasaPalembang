import json
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User


@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        nama = data["nama"]
        username = data["username"]
        password = data["password"]
        password_konfirmasi = data["password_konfirmasi"]
        peran = data["peran"]

        if password != password_konfirmasi:
            return JsonResponse({"message": "Password tidak cocok."}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"message": "Username sudah digunakan."}, status=400)

        # TODO: password tidak mau terenkripsi (hash)
        user = User.objects.create(
            nama=nama,
            username=username,
            password=password,
            peran=peran,
        )
        user.save()

        data = user_data(user)
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({"message": "Login gagal."}, status=401)

        if not user.is_active:
            return JsonResponse({"message": "User dinonaktifkan."}, status=401)

        auth_login(request, user)

        data = user_data(user)
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


@csrf_exempt
def logout(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        auth_logout(request)
        return JsonResponse({"message": "Logout berhasil."}, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


@csrf_exempt
def profile_by_username(request, username):
    if request.method == "GET":
        try:
            user = User.objects.get(username=username)
            data = user_data(user)
            return JsonResponse(data, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "User tidak ditemukan."}, status=404)
    elif request.method == "PUT":
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        if request.user.username != username:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=401)

        data = json.loads(request.body)
        nama = data["nama"]
        deskripsi = data["deskripsi"]
        foto = data["foto"]

        try:
            user = User.objects.get(pk=request.user.id)
            user.nama = nama
            user.deskripsi = deskripsi
            # TODO: Data gambar mungkin berpotensi error (Belum menerima file)
            user.foto = foto
            user.save()

            data = user_data(user)
            return JsonResponse(data, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "User tidak ditemukan."}, status=404)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


def user_data(user):
    data = {
        "pk": user.pk,
        "fields": {
            "username": user.username,
            "nama": user.nama,
            "deskripsi": user.deskripsi,
            "peran": user.peran,
            "foto": user.foto.url if user.foto else "",
            "poin": user.poin,
            "date_joined": user.date_joined,
        }
    }
    return data
