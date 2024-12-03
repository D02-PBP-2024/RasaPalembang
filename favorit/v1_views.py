from django.shortcuts import get_object_or_404
from favorit.forms import FavoritForm
from restoran.models import Restoran
from favorit.models import Favorit
from makanan.models import Makanan
from minuman.models import Minuman
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def api_show_favorit(request):
    """
    API endpoint to show the list of favorites for the logged-in user.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

    favorit = Favorit.objects.filter(user=request.user)
    favorit_list = [
        {
            "pk": fav.id,
            "fields": {
                "catatan": fav.catatan,
                "user": fav.user.id,
                "makanan": fav.makanan.id if fav.makanan else None,
                "minuman": fav.minuman.id if fav.minuman else None,
                "restoran": fav.restoran.id if fav.restoran else None,
            }
        }
        for fav in favorit
    ]
    return JsonResponse({"favorit": favorit_list}, status=200)

@csrf_exempt
def api_favorit_detail(request, id_favorit):
    """
    API endpoint to handle GET, PUT, and DELETE requests for a favorite item by ID.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"message": "User tidak terautentikasi."}, status=401)

    favorit = get_object_or_404(Favorit, id=id_favorit, user=request.user)

    if request.method == "GET":
        return JsonResponse({
            "id": favorit.id,
            "makanan": favorit.makanan.nama if favorit.makanan else None,
            "minuman": favorit.minuman.nama if favorit.minuman else None,
            "restoran": favorit.restoran.nama if favorit.restoran else None,
            "catatan": favorit.catatan,
        }, status=200)

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

    return JsonResponse({"error": "Favorit tidak ditemukan."}, status=405)

@csrf_exempt
def api_add_makanan_to_favorites(request, id_makanan):
    """
    API endpoint to add a makanan to the user's favorites.
    """
    if request.method == "POST":
        item = get_object_or_404(Makanan, id=id_makanan)
        favorit, created = Favorit.objects.get_or_create(user=request.user, makanan=item)
        return JsonResponse({"status": "success", "created": created}, status=200)
    return JsonResponse({"error": "Method tidak diizinkan."}, status=405)

@csrf_exempt
def api_add_minuman_to_favorites(request, id_minuman):
    """
    API endpoint to add a minuman to the user's favorites.
    """
    if request.method == "POST":
        item = get_object_or_404(Minuman, id=id_minuman)
        favorit, created = Favorit.objects.get_or_create(user=request.user, minuman=item)
        return JsonResponse({"status": "success", "created": created}, status=200)
    return JsonResponse({"error": "Method tidak diizinkan."}, status=405)

@csrf_exempt
def api_add_restoran_to_favorites(request, id_restoran):
    """
    API endpoint to add a restoran to the user's favorites.
    """
    if request.method == "POST":
        item = get_object_or_404(Restoran, id=id_restoran)
        favorit, created = Favorit.objects.get_or_create(user=request.user, restoran=item)
        return JsonResponse({"status": "success", "created": created}, status=200)
    return JsonResponse({"error": "Method tidak diizinkan."}, status=405)