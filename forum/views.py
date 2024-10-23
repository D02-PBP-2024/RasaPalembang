from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from forum.models import Forum, Balasan
from forum.forms import ForumForm, BalasanForm
from restoran.models import Restoran


def show_forum(request, id_restoran):
    forum = Forum.objects.filter(restoran=id_restoran)
    restoran = Restoran.objects.get(pk=id_restoran)
    context = {
        "forum": forum,
        "restoran": restoran,
        }
    return render(request, "forum/forum_all/index.html", context)


def show_forum_by_id(request, id_restoran, id_forum):
    forum = Forum.objects.get(pk=id_forum)
    balasan = Balasan.objects.filter(forum=id_forum).order_by("-vote")
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

    context = {'form': form}
    return render(request, 'forum/tambah/index.html', context)


@login_required(login_url="login")
def balas(request, id_restoran, id_forum):
    restoran = Restoran.objects.get(pk=id_restoran)
    forum = Forum.objects.get(pk=id_forum)
    form = BalasanForm(request.POST or None)

    if request.user.peran != 'Pengulas':
        return redirect('forum:show_forum_by_id', id_restoran=restoran.id, id_forum=forum.id)

    if form.is_valid() and request.method == "POST":
        balasan = form.save(commit=False)
        balasan.forum = forum
        balasan.user = request.user
        balasan.save()
        return redirect('forum:show_forum_by_id', id_restoran=restoran.id, id_forum=forum.id)

    context = {
        'form': form,
        'forum': forum,
        }
    return render(request, 'forum/balas/index.html', context)


@login_required(login_url="login")
def delete_forum(request, id_restoran, id_forum):
    forum = Forum.objects.get(pk=id_forum)
    restoran = Restoran.objects.get(pk=id_restoran)

    forum.delete()
    return redirect('forum:show_forum', id_restoran=restoran.id)

@login_required(login_url="login")
def delete_balasan(request, id_restoran, id_forum, id_balasan):
    forum = Forum.objects.get(pk=id_forum)
    restoran = Restoran.objects.get(pk=id_restoran)
    balasan = Balasan.objects.get(pk=id_balasan)

    if request.user.peran != 'Pengulas':
        return redirect('forum:show_forum_by_id', id_restoran=restoran.id, id_forum=forum.id)

    balasan.delete()
    return redirect('forum:show_forum_by_id', id_restoran=restoran.id, id_forum=forum.id)
