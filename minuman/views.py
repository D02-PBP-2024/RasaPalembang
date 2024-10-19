from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from minuman.models import Minuman
from minuman.forms import MinumanForm


# Create your views here.
def show_minuman(request):
    minuman = Minuman.objects.all()
    context = {"minuman": minuman}
    return render(request, "minuman/index.html", context)


def show_minuman_by_id(request, id):
    # minuman = Minuman.objects.get(pk=id)
    context = {
        # "minuman": minuman,
        "id": id,
    }
    return render(request, "minuman_by_id/index.html", context)


def create_minuman(request):
    if request.method == "POST":
        form = MinumanForm(request.POST, request.FILES)
        if form.is_valid():
            minuman = form.save(commit=False)
            # minuman.restoran = request.restoran
            minuman.save()
            return redirect("minuman:show_minuman")
    else:
        form = MinumanForm()

    context = {"form": form}
    return render(request, "create/index.html", context)


def edit_minuman(request, id):
    # minuman = Minuman.objects.get(pk=id)
    context = {
        # 'minuman': minuman,
        'id': id,
    }
    return render(request, "edit/index.html", context)


def delete_minuman(request, id):
    # minuman = Minuman.objects.get(pk=id)

    return HttpResponseRedirect(reverse("minuman:show_minuman"))
