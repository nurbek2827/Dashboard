from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app1.forms.ishchi_form import Ishchi_form
from app1.models import Ishchi


@login_required(login_url="login")
def get_ishchi_delete(requests, pk=None, delete_id=None):
    if delete_id:
        root = Ishchi.objects.filter(pk=delete_id).first()
        if root:
            root.delete()
        return redirect('get_ishchi')
    if pk:
        root = Ishchi.objects.filter(id=pk).first()
        if not root:
            return redirect("get_ishchi")
        return render(requests, "ishchi/detail.html", {"root": root})
    return render(requests, "ishchi/list.html", {"root": Ishchi.objects.all().order_by('-pk')})

def add(requests):
    form = Ishchi_form(requests.POST)
    if form.is_valid():
        form.save()

        return redirect("get_ishchi")
    else:
        ctx = {
            "form": form
        }

    return render(requests, "ishchi/form.html", ctx)


def edit(requests, pk):
    try:
        root = Ishchi.objects.get(id=pk)
    except:
        return redirect('get_ishchi')
    if requests.POST:
        forms = Ishchi_form(requests.POST or None, requests.FILES or None, instance=root)
        if forms.is_valid():
            forms.save()
            return redirect("get_ishchi")
        else:
            print(forms.errors)

    form = Ishchi_form(instance=root)
    ctx = {
        "form": form
    }

    return render(requests, "ishchi/form.html", ctx)
