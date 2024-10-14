from django.shortcuts import render
from minuman.models import Minuman


def show_minuman(request):
    minuman = Minuman.objects.all()
    context = {'minuman': minuman}
    return render(request, 'minuman.html', context)


def show_minuman_by_id(request, id):
    minuman = Minuman.objects.filter(pk=id)
    context = {'minuman': minuman}
    return render(request, 'minuman_by_id.html', context)
