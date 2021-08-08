from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from rakuten.forms import RakutenForm
from rakuten.models import Rakuten

def top(request):
    rakutens = Rakuten.objects.all()
    context = {"rakutens": rakutens}
    return render(request, "rakuten/top.html", context)


@login_required
def rakuten_new(request):
    if request.method == 'POST':
        form = RakutenForm(request.POST)
        if form.is_valid():
            rakuten = form.save(commit=False)
            rakuten.created_by = request.user
            rakuten.save()
            return redirect(rakuten_detail, rakuten_id=rakuten.pk)
    else:
        form = RakutenForm()
    return render(request, "rakuten/rakuten_new.html", {'form': form})


@login_required
def rakuten_edit(request, rakuten_id):
    rakuten = get_object_or_404(Rakuten, pk=rakuten_id)
    if rakuten.created_by_id != request.user.id:
        return HttpResponseForbidden("このスニペットの編集は許可されていません。")

    if request.method == "POST":
        form = RakutenForm(request.POST, instance=rakuten)
        if form.is_valid():
            form.save()
            return redirect('rakuten_detail', rakuten_id=rakuten_id)
    else:
        form = RakutenForm(instance=rakuten)
    return render(request, 'rakuten/rakuten_edit.html', {'form': form})


def rakuten_detail(request, rakuten_id):
    rakuten = get_object_or_404(Rakuten, pk=rakuten_id)
    return render(request, 'rakuten/rakuten_detail.html',
                  {'rakuten': rakuten})


