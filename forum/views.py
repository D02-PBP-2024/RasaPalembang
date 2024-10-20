from django.shortcuts import render, redirect
from forum.models import Forum, Balasan
from forum.forms import ForumForm, BalasanForm

def show_forum(request):
    forum = Forum.objects.all()
    context = {"forum": forum}
    return render(request, "forum/index.html", context)

def show_forum_by_id(request, id):
    form = ForumForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        forum = form.save(commit=False)
        forum = id
        forum.save()
        return redirect('forum:show_forum_by_id')

    context = {'form': form}
    return render(request, 'forum_by_id/index.html', context)


def balas(request, id):
    form = BalasanForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        balasan = form.save(commit=False)
        balasan = id
        balasan.save()
        return redirect('forum:show_forum')

    context = {'form': form}
    return render(request, 'balas/index.html', context)


def create_forum(request):
    form = ForumForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        topik = form.save(commit=False)
        topik = request.user
        topik.save()
        return redirect('forum:show_forum')

    context = {'form': form}
    return render(request, 'create/index.html', context)


