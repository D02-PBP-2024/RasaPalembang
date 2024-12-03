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
    favorit = Favorit.objects.filter(user=request.user)
    favorit_list = [
        {
            "id": fav.id,
            "makanan": fav.makanan.nama if fav.makanan else None,
            "minuman": fav.minuman.nama if fav.minuman else None,
            "restoran": fav.restoran.nama if fav.restoran else None,
            "catatan": fav.catatan,
        }
        for fav in favorit
    ]
    return JsonResponse({"favorit": favorit_list}, status=200)

@csrf_exempt
def api_favorit_detail(request, favorit_id):
    """
    API endpoint to handle GET, PUT, and DELETE requests for a favorite item by ID.
    """
    favorit = get_object_or_404(Favorit, id=favorit_id, user=request.user)

    if request.method == "GET":
        return JsonResponse({
            "id": favorit.id,
            "makanan": favorit.makanan.nama if favorit.makanan else None,
            "minuman": favorit.minuman.nama if favorit.minuman else None,
            "restoran": favorit.restoran.nama if favorit.restoran else None,
            "catatan": favorit.catatan,
        }, status=200)

    elif request.method == "PUT":
        data = json.loads(request.body)
        form = FavoritForm(data, instance=favorit)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success"}, status=200)
        return JsonResponse({"error": form.errors}, status=400)

    elif request.method == "DELETE":
        favorit.delete()
        return JsonResponse({"status": "success"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def api_add_makanan_to_favorites(request, item_id):
    """
    API endpoint to add a makanan to the user's favorites.
    """
    if request.method == "POST":
        item = get_object_or_404(Makanan, id=item_id)
        favorit, created = Favorit.objects.get_or_create(user=request.user, makanan=item)
        return JsonResponse({"status": "success", "created": created}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def api_add_minuman_to_favorites(request, item_id):
    """
    API endpoint to add a minuman to the user's favorites.
    """
    if request.method == "POST":
        item = get_object_or_404(Minuman, id=item_id)
        favorit, created = Favorit.objects.get_or_create(user=request.user, minuman=item)
        return JsonResponse({"status": "success", "created": created}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def api_add_restoran_to_favorites(request, item_id):
    """
    API endpoint to add a restoran to the user's favorites.
    """
    if request.method == "POST":
        item = get_object_or_404(Restoran, id=item_id)
        favorit, created = Favorit.objects.get_or_create(user=request.user, restoran=item)
        return JsonResponse({"status": "success", "created": created}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)