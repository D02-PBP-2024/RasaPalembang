import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from forum.models import Forum, Balasan

@csrf_exempt
def forum_by_id(request, id_forum):
    if request.method == "GET":
        try:
            forum = Forum.objects.get(pk=id_forum)
            data = serialize("json", [forum])
            return HttpResponse(data, content_type="application/json", status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"Message": "Forum Not Found"}, status=404)
    elif request.method == "PUT":
        try:
            forum = Forum.objects.get(pk=id_forum)
            # TODO: Validasi pemilik balasan yang dapat mengedit
            data = json.loads(request.body)
            forum.topik = data["topik"]
            forum.pesan = data["pesan"]
            forum.save()
            return JsonResponse({"Message": "Forum Updated Successfully"}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"Message": "Forum Not Found"}, status=404)
    elif request.method == "DELETE":
        try:
            forum = Forum.objects.get(pk=id_forum)
            # TODO: Validasi pemillik forum yang dapat menghapus
            forum.delete()
            return JsonResponse({"Message": "Forum Deleted Successfully"}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"Message": "Forum Not Found"}, status=404)
    else:
        return JsonResponse({"Message": "Method Not Allowed"}, status=405)
    

@csrf_exempt
def balasan_forum(request, id_forum):
    if request.method == "GET":
        try:
            balasan = Balasan.objects.filter(forum=id_forum).order_by("tanggal_posting")
            data = serialize("json", balasan)
            return HttpResponse(data, content_type="application/json", status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"Message": "Balasan Not Found"}, status=404)
    elif request.method == "POST":
        try:
            # TODO : Validasi login required yang dapat menambah
            restoran = Forum.objects.get(pk=id)
            data = json.loads(request.body)
            balasan = Balasan.objects.create(
                restoran=restoran,
                pesan = data["pesan"],
            )
            balasan.save()
            return JsonResponse({"Message": "Balasan Created Successfully"}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"Message": "Balasan Not Found"}, status=404)
    else:
        return JsonResponse({"Message": "Method Not Allowed"}, status=405)
    

def balasan_by_id(request, id_balasan):
    if request.method == "PUT":
        try:
            balasan = Balasan.objects.get(pk=id_balasan)
            # TODO: Validasi pemilik balasan yang dapat mengedit
            data = json.loads(request.body)
            balasan.pesan = data["pesan"]
            balasan.save()
            return JsonResponse({"Message": "Balasan Updated Successfully"}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"Message": "Balasan Not Found"}, status=404)
    elif request.method == "DELETE":
        try:
            balasan = Balasan.objects.get(pk=id_balasan)
            # TODO: Validasi pemillik balasan yang dapat menghapus
            balasan.delete()
            return JsonResponse({"Message": "Balasan Deleted Successfully"}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"Message": "Balasan Not Found"}, status=404)
    else:
        return JsonResponse({"Message": "Method Not Allowed"}, status=405)