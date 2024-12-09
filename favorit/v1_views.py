import json
from django.core.exceptions import ObjectDoesNotExist
from favorit.forms import FavoritForm
from restoran.models import Restoran
from favorit.models import Favorit
from makanan.models import Makanan
from minuman.models import Minuman
from django.http import JsonResponse
from favorit.utils import favorit_data
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def favorit(request):
    """
    API endpoint to show the list of favorites for the logged-in user.
    """
    if request.method == "GET":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pengulas` atau `pemilik_restoran`
        if request.user.peran not in ["pengulas", "pemilik_restoran"]:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        # Mengambil seluruh objek favorit
        favorit = Favorit.objects.filter(user=request.user)

        # Mengembalikan data seluruh favorit
        data = []
        for m in favorit:
            data.append(favorit_data(m))
        return JsonResponse(data, safe=False, status=200)
    else:
        return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


@csrf_exempt
def favorit_by_id(request, id_favorit):
    """
    API endpoint to handle GET, PUT, and DELETE requests for a favorite item by ID.
    """
    if request.method == "GET":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

            # Memastikan peran user adalah `pengulas` atau `pemilik_restoran`
        if request.user.peran not in ["pengulas", "pemilik_restoran"]:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        try:
            favorit = Favorit.objects.get(id=id_favorit, user=request.user)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Favorit tidak ditemukan."}, status=404)

        # Mengembalikan data seluruh favorit
        data = favorit_data(favorit)
        return JsonResponse(data, status=200)

    elif request.method == "PUT":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pengulas` atau `pemilik_restoran`
        if request.user.peran not in ["pengulas", "pemilik_restoran"]:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Input tidak valid."}, status=400)

        try:
            favorit = Favorit.objects.get(id=id_favorit, user=request.user)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Favorit tidak ditemukan."}, status=404)

        form = FavoritForm(data, instance=favorit)
        if form.is_valid():
            form.save()

            data = favorit_data(favorit)
            return JsonResponse(data, status=200)
        return JsonResponse({"message": form.errors}, status=400)

    elif request.method == "DELETE":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

            # Memastikan peran user adalah `pengulas` atau `pemilik_restoran`
        if request.user.peran not in ["pengulas", "pemilik_restoran"]:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        try:
            favorit = Favorit.objects.get(id=id_favorit, user=request.user)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Favorit tidak ditemukan."}, status=404)

        data = favorit_data(favorit)

        favorit.delete()
        return JsonResponse(data, status=200)

    return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


@csrf_exempt
def favorit_by_makanan(request, id_makanan):
    """
    API endpoint to add a makanan to the user's favorites.
    """
    if request.method == "POST":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pengulas` atau `pemilik_restoran`
        if request.user.peran not in ["pengulas", "pemilik_restoran"]:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        try:
            # Mengambil objek `Makanan` menggunakan id_makanan
            item = Makanan.objects.get(pk=id_makanan)
        except ObjectDoesNotExist:
            # Menangani jika objek tidak ditemukan
            return JsonResponse({"message": "Makanan tidak ditemukan."}, status=404)

        # Membuat atau mendapatkan instance favorit
        favorit, created = Favorit.objects.get_or_create(user=request.user, makanan=item)

        if not created:
            return JsonResponse({"message": "Makanan sudah ditambahkan."}, status=400)

        data = favorit_data(favorit)
        return JsonResponse(data, status=201)

    return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


@csrf_exempt
def favorit_by_minuman(request, id_minuman):
    """
    API endpoint to add a minuman to the user's favorites.
    """
    if request.method == "POST":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

            # Memastikan peran user adalah `pengulas` atau `pemilik_restoran`
        if request.user.peran not in ["pengulas", "pemilik_restoran"]:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        try:
            # Coba mendapatkan objek Minuman
            item = Minuman.objects.get(pk=id_minuman)
        except ObjectDoesNotExist:
            # Tangani jika Minuman tidak ditemukan
            return JsonResponse({"message": "Minuman tidak ditemukan."}, status=404)

        # Tambahkan minuman ke favorit pengguna
        favorit, created = Favorit.objects.get_or_create(user=request.user, minuman=item)

        if not created:
            return JsonResponse({"message": "Minuman sudah ditambahkan."}, status=400)

        data = favorit_data(favorit)
        return JsonResponse(data, status=201)

    return JsonResponse({"message": "Method tidak diizinkan."}, status=405)


@csrf_exempt
def favorit_by_restoran(request, id_restoran):
    """
    API endpoint to add a restoran to the user's favorites.
    """
    if request.method == "POST":
        # Memastikan user terautentikasi
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

        # Memastikan peran user adalah `pengulas` atau `pemilik_restoran`
        if request.user.peran not in ["pengulas", "pemilik_restoran"]:
            return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

        try:
            # Mencoba untuk mendapatkan objek Restoran berdasarkan ID
            item = Restoran.objects.get(pk=id_restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Restoran tidak ditemukan."}, status=404)

        # Membuat atau mendapatkan objek Favorit
        favorit, created = Favorit.objects.get_or_create(user=request.user, restoran=item)

        if not created:
            return JsonResponse({"message": "Restoran sudah ditambahkan."}, status=400)

        data = favorit_data(favorit)
        return JsonResponse(data, status=201)

    return JsonResponse({"message": "Method tidak diizinkan."}, status=405)
