from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from forum.models import Forum, Balasan
from forum.forms import ForumForm, BalasanForm
from restoran.models import Restoran
from django.views.decorators.http import require_POST
from django.core import serializers


def show_forum(request, id_restoran):
    forum = Forum.objects.filter(restoran=id_restoran).select_related("user")
    restoran = Restoran.objects.get(pk=id_restoran)
    context = {
        "forum": forum,
        "restoran": restoran
    }
    
    return render(request, "forum/forum_all/index.html", context)


def show_forum_by_id(request, id_restoran, id_forum):
    forum = Forum.objects.get(pk=id_forum)
    balasan = Balasan.objects.filter(forum=id_forum)
    context = {
        "forum": forum,
        "balasan": balasan,
    }
    return render(request, "forum/forum_by_id/index.html", context)


@login_required(login_url="login")
def create_forum(request, id_restoran):
    restoran = Restoran.objects.get(pk=id_restoran)
    form = ForumForm(request.POST or None)

    if request.user.peran != 'pengulas':
        return redirect('forum:show_forum', id_restoran=restoran.id)

    if form.is_valid() and request.method == "POST":
        topik = form.save(commit=False)
        topik.user = request.user
        topik.restoran = restoran
        topik.save()
        return redirect('forum:show_forum', id_restoran=restoran.id)
    
    request.user.poin += 5
    request.user.save()

    context = {'form': form}
    return render(request, 'forum/tambah/index.html', context)


@login_required(login_url="login")
def balas(request, id_restoran, id_forum):
    restoran = Restoran.objects.get(pk=id_restoran)
    forum = Forum.objects.get(pk=id_forum)
    form = BalasanForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        balasan = form.save(commit=False)
        balasan.forum = forum
        balasan.user = request.user
        balasan.save()
        return redirect('forum:show_forum_by_id', id_restoran=restoran.id, id_forum=forum.id)

    request.user.poin += 3
    request.user.save()

    context = {
        'form': form,
        'forum': forum,
    }
    return render(request, 'forum/balas/index.html', context)


@login_required(login_url="login")
def edit_forum(request, id_restoran, id_forum):
    forum = Forum.objects.get(pk=id_forum)
    form = ForumForm(request.POST, instance=forum)
    restoran = Restoran.objects.get(pk=id_restoran)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('forum:show_forum', id_restoran=restoran.id)
        
    context = {"forum": forum}
    return render(request, 'edit/edit_forum.html', context)


@login_required(login_url="login")
def delete_forum(request, id_restoran, id_forum):
    forum = Forum.objects.get(pk=id_forum)
    restoran = Restoran.objects.get(pk=id_restoran)

    forum.delete()
    return redirect('forum:show_forum', id_restoran=restoran.id)


@login_required(login_url="login")
def edit_balasan(request, id_restoran, id_forum, id_balasan):
    forum = Forum.objects.get(pk=id_forum)
    restoran = Restoran.objects.get(pk=id_restoran)
    balasan = Balasan.objects.get(pk=id_balasan)
    form = BalasanForm(request.POST, instance=balasan)

    if request.user.peran != 'pengulas':
        return redirect('forum:show_forum_by_id', id_restoran=restoran.id, id_forum=forum.id)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('forum:show_forum_by_id', id_restoran=restoran.id, id_forum=forum.id)

    context = {"balasan": balasan}
    return render(request, "edit/edit_balasan.html", context)


@login_required(login_url="login")
def delete_balasan(request, id_restoran, id_forum, id_balasan):
    forum = Forum.objects.get(pk=id_forum)
    restoran = Restoran.objects.get(pk=id_restoran)
    balasan = Balasan.objects.get(pk=id_balasan)

    if request.user.peran != 'pengulas':
        return redirect('forum:show_forum_by_id', id_restoran=restoran.id, id_forum=forum.id)

    balasan.delete()
    return redirect('forum:show_forum_by_id', id_restoran=restoran.id, id_forum=forum.id)


@require_POST
def balas_ajax(request, id_restoran, id_forum):
    pesan = request.POST.get("pesan")
    user = request.user
    forum = request.POST.get("forum")

    new_balasan = Balasan(user=user, pesan=pesan, forum=forum)
    print(pesan)
    print(forum)
    new_balasan.save()

    return HttpResponse(b"CREATED", status=201)

def show_balasan(request, id_restoran, id_forum):
    data = Balasan.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
