import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User


@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            User.objects.get(username=data["username"])
            return JsonResponse({"Message": "Username Already Exist"}, status=400)
        except ObjectDoesNotExist:
            user = User.objects.create(
                nama=data["nama"],
                username=data["username"],
                password=data["password"],
                peran=data["peran"],
            )
            user.save()
            return JsonResponse({"Message": "User Registered Successfully"}, status=201)
    else:
        return JsonResponse({"Message": "Method Not Allowed"}, status=405)


def login(request):
    if request.method == "POST":
        # TODO: implementasi login
        pass
    else:
        return JsonResponse({"Message": "Method Not Allowed"}, status=405)

def profile_by_username(request, username):
    if request.method == "GET":
        try:
            user = User.objects.get(username=username)
            data = serialize("json", [user])
            return HttpResponse(data, content_type="application/json", status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"Message": "User Not Found"}, status=404)
    elif request.method == "POST":
        # TODO: edit profile
        pass
    else:
        return JsonResponse({"Message": "Method Not Allowed"}, status=405)