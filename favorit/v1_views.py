from django.core.exceptions import ObjectDoesNotExist
from favorit.forms import FavoritForm
from restoran.models import Restoran
from favorit.models import Favorit
from makanan.models import Makanan
from minuman.models import Minuman
from django.http import JsonResponse
from favorit.utils import favorit_data
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def favorit(request):
    """
    API endpoint to show the list of favorites for the logged-in user.
    """
    
    # Memastikan user terautentikasi
    if not request.user.is_authenticated:
        return JsonResponse({"message": "User tidak terautentikasi."}, status=401)
        
    # Memastikan peran user adalah `pengulas` atau `pemilik_restoran`
    if request.user.peran not in ["pengulas", "pemilik_restoran"]:
        return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)
        
    if request.method == "GET":
        # Mengambil seluruh objek favorit
        favorit = Favorit.objects.all()

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
    if not request.user.is_authenticated:
        return JsonResponse({"message": "User tidak terautentikasi."}, status=401)
    
    # Memastikan peran user adalah `pengulas` atau `pemilik_restoran`
    if request.user.peran not in ["pengulas", "pemilik_restoran"]:
        return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

    try:
        favorit = Favorit.objects.get(id=id_favorit, user=request.user)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Favorit tidak ditemukan."}, status=404)

    if request.method == "GET":
        # Mengambil seluruh objek favorit
        favorit = Favorit.objects.all()
        # Mengembalikan data seluruh favorit
        data = []
        for m in favorit:
            data.append(favorit_data(m))
        return JsonResponse(data, safe=False, status=200)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Input tidak valid."}, status=400)

        form = FavoritForm(data, instance=favorit)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success"}, status=200)
        return JsonResponse({"error": form.errors}, status=400)

    elif request.method == "DELETE":
        favorit.delete()
        return JsonResponse({"status": "success"}, status=200)

    return JsonResponse({"error": "Favorit tidak ditemukan."}, status=404)

@csrf_exempt
def favorit_by_makanan(request, id_makanan):
    """
    API endpoint to add a makanan to the user's favorites.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"message": "User tidak terautentikasi."}, status=401)
    
    # Memastikan peran user adalah `pengulas` atau `pemilik_restoran`
    if request.user.peran not in ["pengulas", "pemilik_restoran"]:
        return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

    if request.method == "POST":
        try:
            # Mengambil objek `Makanan` menggunakan id_makanan
            item = Makanan.objects.get(pk=id_makanan)
        except ObjectDoesNotExist:
            # Menangani jika objek tidak ditemukan
            return JsonResponse({"message": "Makanan tidak ditemukan."}, status=404)

        # Membuat atau mendapatkan instance favorit
        favorit, created = Favorit.objects.get_or_create(user=request.user, makanan=item)
        return JsonResponse({"status": "success", "created": created}, status=200)
    
    return JsonResponse({"message": "Method tidak diizinkan."}, status=405)   

@csrf_exempt
def favorit_by_minuman(request, id_minuman):
    """
    API endpoint to add a minuman to the user's favorites.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"message": "User tidak terautentikasi."}, status=401)
    
    # Memastikan peran user adalah `pengulas` atau `pemilik_restoran`
    if request.user.peran not in ["pengulas", "pemilik_restoran"]:
        return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

    if request.method == "POST":
        try:
            # Coba mendapatkan objek Minuman
            item = Minuman.objects.get(pk=id_minuman)
        except ObjectDoesNotExist:
            # Tangani jika Minuman tidak ditemukan
            return JsonResponse({"message": "Minuman tidak ditemukan."}, status=404)

        # Tambahkan minuman ke favorit pengguna
        favorit, created = Favorit.objects.get_or_create(user=request.user, minuman=item)
        return JsonResponse({"status": "success", "created": created}, status=200)
    
    return JsonResponse({"error": "Method tidak diizinkan."}, status=405)    

@csrf_exempt
def favorit_by_restoran(request, id_restoran):
    """
    API endpoint to add a restoran to the user's favorites.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"message": "User tidak terautentikasi."}, status=401)
    
    # Memastikan peran user adalah `pengulas` atau `pemilik_restoran`
    if request.user.peran not in ["pengulas", "pemilik_restoran"]:
        return JsonResponse({"message": "Tindakan tidak diizinkan."}, status=403)

    if request.method == "POST":
        try:
            # Mencoba untuk mendapatkan objek Restoran berdasarkan ID
            item = Restoran.objects.get(pk=id_restoran)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Restoran tidak ditemukan."}, status=404)

        # Membuat atau mendapatkan objek Favorit
        favorit, created = Favorit.objects.get_or_create(user=request.user, restoran=item)
        return JsonResponse({"status": "success", "created": created}, status=200)

    return JsonResponse({"error": "Method tidak diizinkan."}, status=405)