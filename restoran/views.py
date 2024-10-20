from django.shortcuts import render, redirect

from restoran.forms import RestoranForm


# Create your views here.
def tambah_restoran(request):
    if request.method == "POST":
        form = RestoranForm(request.POST)
        if form.is_valid():
            restoran = form.save(commit=False)
            restoran.save()
            return redirect("minuman:show_minuman")
    else:
        form = RestoranForm()

    context = {
        "form": form,
    }
    return render(request, "main.html", context)
